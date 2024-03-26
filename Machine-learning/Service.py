from EncConvNet import *
import tenseal as ts
import torch
from torchvision import datasets
import torchvision.transforms as transforms
import numpy as np
from test import *
from training import *

def enc_test(enc, enc_model, windows_nb):
    # initialize lists to monitor test loss and accuracy
    test_loss = 0.0
    class_correct = list(0. for i in range(10))
    class_total = list(0. for i in range(10))
    enc_learn = []
    excepted = len(enc)
    present = 0

    #Verschlüsselung der Daten
    for data, window in zip(enc, windows_nb):
        # Encrypted evaluation

        enc_output = enc_model(data, window)
        enc_learn.append(enc_output)
        print(f"{present} / {excepted}")
        present += 1
        if present >= 500:
            break
    return enc_learn
