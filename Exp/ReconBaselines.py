import os
import pandas as pd
import wandb
from tqdm import tqdm
import copy
import matplotlib.pyplot as plt

# Trainer
from Exp.Trainer import Trainer
from Exp.Tester import Tester

# models
from models.MLP import MLP

# others
import torch
import torch.nn.functional as F
import numpy as np

from utils.metrics import get_summary_stats
from utils.ema import EMAUpdater
from utils.tools import plot_interval
from utils.loss import soft_f1_loss, FocalLoss

class MLP_Trainer(Trainer):
    def __init__(self, args, logger, train_loader):
        super(MLP_Trainer, self).__init__(
            args=args,
            logger=logger,
            train_loader=train_loader
        )

        self.model = MLP(
            seq_len=args.window_size,
            num_channels=args.num_channels,
            latent_space_size=args.model.latent_dim,
        ).to(self.args.device)

        self.optimizer = torch.optim.Adam(params=self.model.parameters(), lr=args.lr)


    def train(self):
        wandb.watch(self.model, log="all", log_freq=100)

        train_iterator = tqdm(
            range(1, self.args.epochs + 1),
            total=self.args.epochs,
            desc="training epochs",
            leave=True
        )

        best_train_stats = None
        for epoch in train_iterator:
            # train
            train_stats = self.train_epoch()
            self.logger.info(f"epoch {epoch} | train_stats: {train_stats}")
            self.checkpoint(os.path.join(self.args.checkpoint_path, f"epoch{epoch}.pth"))

            if best_train_stats is None or train_stats < best_train_stats:
                self.logger.info(f"Saving best results @epoch{epoch}")
                self.checkpoint(os.path.join(self.args.checkpoint_path, f"best.pth"))
                best_train_stats = train_stats


    def train_epoch(self):
        self.model.train()
        log_freq = len(self.train_loader) // self.args.log_freq
        train_summary = 0.0
        for i, batch_data in enumerate(self.train_loader):
            train_log = self._process_batch(batch_data)
            if (i+1) % log_freq == 0:
                self.logger.info(f"{train_log}")
                wandb.log(train_log)
            train_summary += train_log["summary"]
        train_summary /= len(self.train_loader)
        return train_summary


    def _process_batch(self, batch_data) -> dict:
        X = batch_data[0].to(self.args.device)
        B, L, C = X.shape

        # recon
        Xhat = self.model(X)

        # optimize
        self.optimizer.zero_grad()
        loss = F.mse_loss(Xhat, X)
        loss.backward()
        self.optimizer.step()

        out = {
            "recon_loss": loss.item(),
            "summary": loss.item(),
        }
        return out



class MLP_Tester(Tester):
    def __init__(self, args, logger, train_loader, test_loader):
        super(MLP_Tester, self).__init__(
            args=args,
            logger=logger,
            train_loader=train_loader,
            test_loader=test_loader
        )

        self.model = MLP(
            seq_len=args.window_size,
            num_channels=args.num_channels,
            latent_space_size=args.model.latent_dim,
        ).to(self.args.device)

        self.load_trained_model()
        self.prepare_stats()


    def load_trained_model(self):
        self.load(os.path.join(self.args.checkpoint_path, f"best.pth"))


    def prepare_stats(self):
        '''
        prepare 95, 99, 100 threshold of train errors.
        prepare test errors, gt, and best threshold with test errors to check optimal bound of offline approaches.
        '''
        # train
        train_error_pt_path = os.path.join(self.args.output_path, "train_errors.pt")
        if self.args.load_previous_error and os.path.isfile(train_error_pt_path):
            self.logger.info("train_errors.pt file exists, loading...")
            with open(train_error_pt_path, 'rb') as f:
                train_errors = torch.load(f)
                train_errors.to(self.args.device)
            self.logger.info(f"{train_errors.shape}")
        else:
            self.logger.info("train_errors.pt file does not exist, calculating...")
            train_errors = self.calculate_recon_errors(self.train_loader).mean(dim=2)  # (B, L, C) => (B, L)
            self.logger.info("saving train_errors.pt...")
            with open(train_error_pt_path, 'wb') as f:
                torch.save(train_errors, f)

        # test
        test_error_pt_path = os.path.join(self.args.output_path, "test_errors.pt")
        if self.args.load_previous_error and os.path.isfile(test_error_pt_path):
            self.logger.info("test_errors.pt file exists, loading...")
            with open(test_error_pt_path, 'rb') as f:
                test_errors = torch.load(f)
                test_errors.to(self.args.device)
            self.logger.info(f"{test_errors.shape}")
        else:
            self.logger.info("test_errors.pt file does not exist, calculating...")
            test_errors = self.calculate_recon_errors(self.test_loader).mean(dim=2)  # (B, L, C) => (B, L)
            self.logger.info("saving test_errors.pt...")
            with open(test_error_pt_path, 'wb') as f:
                torch.save(test_errors, f)

        # test errors (T=B*L, C) and ground truth
        self.test_errors = test_errors.reshape(-1).detach().cpu().numpy()
        self.gt = self.test_loader.dataset.y

        # thresholds
        self.th_q95 = torch.quantile(train_errors, 0.95).item()
        self.th_q99 = torch.quantile(train_errors, 0.99).item()
        self.th_q100 = torch.max(train_errors).item()
        self.th_best_static = self.get_best_static_threshold(gt=self.gt, anomaly_scores=self.test_errors)


    @torch.no_grad()
    def calculate_recon_errors(self, dataloader):
        '''
        :return:  returns (B, L, C) recon loss tensor
        '''
        it = tqdm(
            dataloader,
            total=len(dataloader),
            desc="calculating reconstruction errors",
            leave=True
        )
        recon_errors = []
        for i, batch_data in enumerate(it):
            X = batch_data[0].to(self.args.device)
            B, L, C = X.shape
            Xhat = self.model(X)
            recon_error = F.mse_loss(Xhat, X, reduction='none')
            recon_errors.append(recon_error)
        recon_errors = torch.cat(recon_errors, axis=0)
        return recon_errors


    def infer(self, mode, cols):
        result_df = pd.DataFrame(columns=cols)
        gt = self.test_loader.dataset.y

        if mode == "offline":
            result_df = self.offline_inference(cols=cols)
            self.logger.info(f"{mode} \n {result_df.to_string()}")
            return result_df

        # supervised (label)
        elif mode == "online_label_bce_seq":
            pred = self.online_label(self.test_loader, self.th_q95, cls_loss="bce")
            result = get_summary_stats(gt, pred)
        elif mode == "online_label_focal_seq":
            pred = self.online_label(self.test_loader, self.th_q95, cls_loss="focal")
            result = get_summary_stats(gt, pred)
        elif mode == "online_label_bce_joint":
            pred = self.online_label_jointly(self.test_loader, self.th_q95, cls_loss="bce")
            result = get_summary_stats(gt, pred)
        elif mode == "online_label_focal_joint":
            pred = self.online_label_jointly(self.test_loader, self.th_q95, cls_loss="focal")
            result = get_summary_stats(gt, pred)

        # unsupervised (us)
        elif mode == "online_us_bce_seq":
            pred = self.online_us(self.test_loader, self.th_q95, cls_loss="bce")
            result = get_summary_stats(gt, pred)
        elif mode == "online_us_focal_seq":
            pred = self.online_us(self.test_loader, self.th_q95, cls_loss="focal")
            result = get_summary_stats(gt, pred)
        elif mode == "online_us_bce_joint":
            pred = self.online_us_jointly(self.test_loader, self.th_q95, cls_loss="bce")
            result = get_summary_stats(gt, pred)
        elif mode == "online_us_focal_joint":
            pred = self.online_us_jointly(self.test_loader, self.th_q95, cls_loss="focal")
            result = get_summary_stats(gt, pred)

        wandb.log(result)
        result = pd.DataFrame([result], index=[mode], columns=result_df.columns)
        self.logger.info(f"{mode} \n {result.to_string()}")
        result_df = result_df.append(result)
        return result_df


    def offline_inference(self, cols):
        result_df = pd.DataFrame(columns=cols)

        q95_result = get_summary_stats(self.gt, self.test_errors > self.th_q95)
        q99_result = get_summary_stats(self.gt, self.test_errors > self.th_q99)
        q100_result = get_summary_stats(self.gt, self.test_errors > self.th_q100)
        best_static_result = get_summary_stats(self.gt, self.test_errors > self.th_best_static)

        result_df = result_df.append(pd.DataFrame([q95_result], index=["Q95"], columns=result_df.columns))
        result_df = result_df.append(pd.DataFrame([q99_result], index=["Q99"], columns=result_df.columns))
        result_df = result_df.append(pd.DataFrame([q100_result], index=["Q100"], columns=result_df.columns))
        result_df = result_df.append(pd.DataFrame([best_static_result], index=["BEST"], columns=result_df.columns))

        # plot results w/o TTA
        plt.figure(figsize=(20, 6))
        plt.plot(self.test_errors, color="blue", label="anomaly score w/o online learning")
        plt.axhline(self.th_q95, color="C1", label="Q95 threshold")
        plt.axhline(self.th_q99, color="C2", label="Q99 threshold")
        plt.axhline(self.th_q100, color="C3", label="Q100 threshold")
        plt.axhline(self.th_best_static, color="C4", label="threshold w/ test data")
        plt.legend()
        plot_interval(plt, self.gt)
        plt.savefig(os.path.join(self.args.plot_path, f"{self.args.exp_id}_woTTA.png"))
        wandb.log({"woTTA": wandb.Image(plt)})
        return result_df


    def online_us(self, dataloader, init_thr, cls_loss="bce"):
        self.load_trained_model() # reset

        it = tqdm(
            dataloader,
            total=len(dataloader),
            desc="inference",
            leave=True
        )

        thr = torch.tensor(init_thr, requires_grad=True)

        TT_optimizer = torch.optim.SGD([p for p in self.model.parameters()], lr=self.args.ttlr)
        TH_optimizer = torch.optim.SGD([thr], self.args.thlr)

        loss_fn = torch.nn.BCELoss() if cls_loss == "bce" else FocalLoss()

        Xs, Xhats = [], []
        preds = []
        As, thrs = [], []

        for i, batch_data in enumerate(it):
            X = batch_data[0].to(self.args.device)
            B, L, C = X.shape

            Xhat = self.model(X)
            E = F.mse_loss(Xhat, X, reduction='none')
            A = E.mean(dim=2)
            ytilde = (A > thr).float()
            pred = ytilde

            # log model outputs
            Xs.append(X)
            Xhats.append(Xhat.clone().detach())
            As.append(A.clone().detach())
            preds.append(pred.clone().detach())
            thrs.append(thr.clone().detach().item())

            # learn new-normals
            TT_optimizer.zero_grad()
            mask = (ytilde == 0)
            recon_loss = (A * mask).mean()
            recon_loss.backward()
            TT_optimizer.step()

            # update threshold
            TH_optimizer.zero_grad()
            Xhat = self.model(X)
            E = F.mse_loss(Xhat, X, reduction='none')
            A = E.mean(dim=2)
            yhat = torch.sigmoid((A - thr))
            cls_loss = loss_fn(yhat, ytilde.float())
            cls_loss.backward()
            TH_optimizer.step()

        # outputs
        Xs = torch.cat(Xs, axis=0).detach().cpu().numpy()
        Xhats = torch.cat(Xhats, axis=0).detach().cpu().numpy()
        anoscs = torch.cat(As, axis=0).reshape(-1).detach().cpu().numpy()
        thrs = np.repeat(np.array(thrs), self.args.window_size * self.args.eval_batch_size)
        preds = torch.cat(preds).reshape(-1).detach().cpu().numpy().astype(int)

        # save plots
        ## anomaly scores
        if self.args.plot_anomaly_scores:
            self.logger.info("Plotting anomaly scores...")
            plt.figure(figsize=(20, 6), dpi=500)
            plt.title(f"online_us_bce_{self.args.dataset}")
            plt.plot(self.test_errors, color="blue", label="anomaly score w/o online learning")
            plt.plot(anoscs, color="green", label="anomaly score w/ online learning")
            plt.axhline(self.th_q95, color="purple", label="train 95% threshold")
            plt.plot(thrs, color="black", label="dynamic threshold")

            plot_interval(plt, self.gt)
            plot_interval(plt, preds, facecolor="gray", alpha=1)
            plt.legend()
            plt.savefig(os.path.join(self.args.plot_path, f"{self.args.exp_id}_wTTA.png"))
            wandb.log({"wTTA": wandb.Image(plt)})

        ## reconstruction status
        if self.args.plot_recon_status:
            self.logger.info("Plotting reconstruction status...")

            for c in range(self.args.num_channels):
                B, L, C = Xhats.shape
                title = f"{self.args.exp_id}_wTTA_recon_ch{c}"

                plt.figure(figsize=(20, 6), dpi=500)
                plt.title(f"{title}")
                plt.plot(Xs[:, c], color="black", label="gt")
                plt.plot(Xhats[:, :, c].reshape(-1), linewidth=0.5, color="green", label="reconed w/ online learning")
                plt.legend()
                plot_interval(plt, self.gt)
                plt.savefig(os.path.join(self.args.plot_path, f"{title}.png"))
                wandb.log({f"{title}": wandb.Image(plt)})

        return preds


    def online_us_jointly(self, dataloader, init_thr, cls_loss="bce"):
        self.load_trained_model() # reset

        it = tqdm(
            dataloader,
            total=len(dataloader),
            desc="inference",
            leave=True
        )

        thr = torch.tensor(init_thr, requires_grad=True)

        TT_optimizer = torch.optim.SGD([thr]+[p for p in self.model.parameters()], lr=self.args.ttlr)

        loss_fn = torch.nn.BCELoss() if cls_loss == "bce" else FocalLoss()

        preds = []
        for i, batch_data in enumerate(it):
            X = batch_data[0].to(self.args.device)
            B, L, C = X.shape

            Xhat = self.model(X)
            E = F.mse_loss(Xhat, X, reduction='none')
            A = E.mean(dim=2)
            ytilde = (A > thr)
            pred = ytilde
            preds.append(pred.clone().detach())

            # learn new-normals and update threshold
            TT_optimizer.zero_grad()
            mask = (ytilde == 0)
            yhat = torch.sigmoid((A - thr))
            cls_loss = loss_fn(yhat, ytilde.float())
            recon_loss = (A * mask).mean()
            loss = recon_loss + self.args.cls_lambda * cls_loss
            loss.backward()
            TT_optimizer.step()

        preds = torch.cat(preds).reshape(-1).detach().cpu().numpy()
        return preds


    def online_label(self, dataloader, init_thr, cls_loss="bce"):
        self.load_trained_model() # reset

        it = tqdm(
            dataloader,
            total=len(dataloader),
            desc="inference",
            leave=True
        )

        thr = torch.tensor(init_thr, requires_grad=True)

        TT_optimizer = torch.optim.SGD([p for p in self.model.parameters()], lr=self.args.ttlr)
        TH_optimizer = torch.optim.SGD([thr], self.args.thlr)

        loss_fn = torch.nn.BCELoss() if cls_loss == "bce" else FocalLoss()

        preds = []
        for i, batch_data in enumerate(it):
            X = batch_data[0].to(self.args.device)
            y = batch_data[1].to(self.args.device)
            B, L, C = X.shape

            Xhat = self.model(X)
            E = F.mse_loss(Xhat, X, reduction='none')
            A = E.mean(dim=2)
            pred = (A > thr)
            preds.append(pred)

            # learn new-normals
            TT_optimizer.zero_grad()
            mask = (y == 0)
            recon_loss = (A * mask).mean()
            recon_loss.backward()
            TT_optimizer.step()

            # update threshold
            TH_optimizer.zero_grad()
            Xhat = self.model(X)
            E = F.mse_loss(Xhat, X, reduction='none')
            A = E.mean(dim=2)
            yhat = torch.sigmoid((A - thr))
            cls_loss = loss_fn(yhat, y.float())
            cls_loss.backward()
            TH_optimizer.step()

        preds = torch.cat(preds).reshape(-1).detach().cpu().numpy()
        return preds


    def online_label_jointly(self, dataloader, init_thr, cls_loss="bce"):
        self.load_trained_model() # reset

        it = tqdm(
            dataloader,
            total=len(dataloader),
            desc="inference",
            leave=True
        )

        thr = torch.tensor(init_thr, requires_grad=True)

        TT_optimizer = torch.optim.SGD([thr]+[p for p in self.model.parameters()], lr=self.args.ttlr)
        loss_fn = torch.nn.BCELoss() if cls_loss == "bce" else FocalLoss()

        preds = []
        for i, batch_data in enumerate(it):
            X = batch_data[0].to(self.args.device)
            y = batch_data[1].to(self.args.device)
            B, L, C = X.shape

            Xhat = self.model(X)
            E = F.mse_loss(Xhat, X, reduction='none')
            A = E.mean(dim=2)
            pred = (A > thr)
            preds.append(pred)

            # learn new-normals and update threshold
            TT_optimizer.zero_grad()

            mask = (y == 0)
            recon_loss = (A * mask).mean()
            yhat = torch.sigmoid((A - thr))
            cls_loss = loss_fn(yhat, y.float())

            loss = recon_loss + self.args.cls_lambda * cls_loss
            loss.backward()
            TT_optimizer.step()

        preds = torch.cat(preds).reshape(-1).detach().cpu().numpy()
        return preds
