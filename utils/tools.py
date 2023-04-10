import torch
import numpy as np
import random
import pandas as pd
from torch.autograd import Variable

def SEED_everything(SEED):
    torch.manual_seed(SEED)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(SEED)
    random.seed(SEED)

def set_requires_grad(model, val):
    for p in model.parameters():
        p.requires_grad = val

def read_xlsx_and_convert_to_csv(path):
    excelFile = pd.read_excel(path, skiprows=[0])
    filename = path[:-5]
    excelFile.to_csv(f"{filename}.csv", index=None, header=True)


def to_var(x, volatile=False):
    if torch.cuda.is_available():
        x = x.cuda()
    return Variable(x, volatile=volatile)


def plot_interval(ax, interval, facecolor="red", alpha=0.5):
    s, e = None, None
    n = len(interval)
    for i in range(n):
        if interval[i] == 1 and s is None:
            s = i
        elif interval[i] == 0 and s is not None:
            e = i - 1
            if (e - s) > 0:
                ax.axvspan(s, e, facecolor=facecolor, alpha=alpha)
            else:
                ax.axvspan(s-0.5, s+0.5, facecolor=facecolor, alpha=alpha)
            s, e = None, None

    if s is not None:
        if (n - 1 - s) > 0:
            ax.axvspan(s, n-1, facecolor=facecolor, alpha=alpha)
        else:
            ax.axvspan(s - 0.5, s + 0.5, facecolor=facecolor, alpha=alpha)


def set_requires_grad(model, val):
    for p in model.parameters():
        p.requires_grad = val


if __name__ == "__main__":
    print("*")
    read_xlsx_and_convert_to_csv("../data/SWaT/SWaT_Dataset_Attack_v0.xlsx")
    print("*")
    read_xlsx_and_convert_to_csv("../data/SWaT/SWaT_Dataset_Normal_v0.xlsx")
    print("*")
    read_xlsx_and_convert_to_csv("../data/SWaT/SWaT_Dataset_Normal_v1.xlsx")
    print("*")