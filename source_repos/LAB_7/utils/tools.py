import os
import numpy as np
import torch
import matplotlib.pyplot as plt

class EarlyStopping:
    def __init__(self, patience=7, verbose=False, delta=0):
        self.patience = patience
        self.verbose = verbose
        self.delta = delta
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.inf

    def __call__(self, val_loss, model, path):
        score = -val_loss
        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model, path)
        elif score < self.best_score + self.delta:
            self.counter += 1
            if self.verbose:
                print(f"EarlyStopping counter: {self.counter} out of {self.patience}")
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.save_checkpoint(val_loss, model, path)
            self.counter = 0

    def save_checkpoint(self, val_loss, model, path):
        os.makedirs(path, exist_ok=True)
        torch.save(model.state_dict(), os.path.join(path, "checkpoint.pth"))
        self.val_loss_min = val_loss

def adjust_learning_rate(optimizer, epoch, args):
    if hasattr(args, "learning_rate"):
        lr = args.learning_rate * (0.5 ** max(epoch - 1, 0))
        for param_group in optimizer.param_groups:
            param_group["lr"] = lr
        print(f"Updating learning rate to {lr}")

def visual(true, preds=None, name='./pic/test.pdf'):
    os.makedirs(os.path.dirname(name), exist_ok=True)
    plt.figure()
    plt.plot(true, label='GroundTruth')
    if preds is not None:
        plt.plot(preds, label='Prediction')
    plt.legend()
    plt.savefig(name, bbox_inches='tight')
    plt.close()
