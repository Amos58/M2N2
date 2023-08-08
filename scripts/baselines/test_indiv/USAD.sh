#!/bin/bash
# USAD
echo "gpu $1"
for SEED in 2021 2022 2023 2024 2025
do
  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=SWaT save_roc_curve=True window_size=12 stride=12 eval_stride=12 batch_size=64 eval_batch_size=64 scaler=minmax model=USAD normalization=None model.latent_dim=40 infer_options=["offline"] thresholding=off_f1_best  &&
  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=WADI window_size=10 stride=10 eval_stride=10 batch_size=64 eval_batch_size=64 scaler=minmax model=USAD normalization=None  model.latent_dim=40 infer_options=["offline"] thresholding=off_f1_best  &&
  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=SMD +dataset_id=machine-1-4 save_roc_curve=True window_size=5 stride=5 eval_stride=5 batch_size=8 eval_batch_size=8 scaler=minmax model=USAD normalization=None model.latent_dim=38 infer_options=["offline"] thresholding=off_f1_best  &&
  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=SMD +dataset_id=machine-2-1 save_roc_curve=True window_size=5 stride=5 eval_stride=5 batch_size=8 eval_batch_size=8 scaler=minmax model=USAD normalization=None model.latent_dim=38 infer_options=["offline"] thresholding=off_f1_best
  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=MSL +dataset_id=P-15 save_roc_curve=True window_size=5 stride=5 eval_stride=5 batch_size=8 eval_batch_size=8 scaler=minmax model=USAD normalization=None model.latent_dim=33 infer_options=["offline"] thresholding=off_f1_best  &&
  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=SMAP +dataset_id=T-3 save_roc_curve=True window_size=5 stride=5 eval_stride=5 batch_size=8 eval_batch_size=8 scaler=minmax model=USAD normalization=None model.latent_dim=33 infer_options=["offline"] thresholding=off_f1_best  &&
  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=CreditCard save_roc_curve=True window_size=12 stride=12 eval_stride=12 batch_size=64 eval_batch_size=64 scaler=minmax model=USAD normalization=None model.latent_dim=40 infer_options=["offline"] thresholding=off_f1_best  &&
  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=yahoo +dataset_id=real_20 save_roc_curve=True window_size=5 stride=5 eval_stride=5 batch_size=8 eval_batch_size=8 scaler=minmax model=USAD normalization=None model.latent_dim=40 infer_options=["offline"] thresholding=off_f1_best &&
  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=yahoo +dataset_id=real_55 save_roc_curve=True window_size=5 stride=5 eval_stride=5 batch_size=8 eval_batch_size=8 scaler=minmax model=USAD normalization=None model.latent_dim=40 infer_options=["offline"] thresholding=off_f1_best
done
