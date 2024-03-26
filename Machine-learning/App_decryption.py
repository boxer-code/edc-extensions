import tenseal as ts
import torch
from torchvision import datasets
import torchvision.transforms as transforms
import numpy as np
from test import *
from training import *

def decrypt_test(data, target, enc_l, criterion):
     # initialize lists to monitor test loss and accuracy
    test_loss = 0.0
    class_correct = list(0. for i in range(10))
    class_total = list(0. for i in range(10))
    loop = 0
    zipped_data = zip(data,target)
    for data,target in zipped_data:
        print("Verschlüsselte Daten")
        enc_data = enc_l[loop]
        print(enc_data)
        print("Data bereitgestellt")
        print(target)
        output = enc_data.decrypt()
        output = torch.tensor(output).view(1, -1)

        # compute loss
        loss = criterion(output, target)
        test_loss += loss.item()
            
        # convert output probabilities to predicted class
        _, pred = torch.max(output, 1)
        # compare predictions to true label
        correct = np.squeeze(pred.eq(target.data.view_as(pred)))
        # calculate test accuracy for each object class
        label = target.data[0]
        class_correct[label] += correct.item()
        class_total[label] += 1

        loop += 1
        # calculate and print avg test loss
    test_loss = test_loss / sum(class_total)
    f = open("result.txt", "a")
    f.write(f'Test Loss: {test_loss:.6f}\n')

    for label in range(10):
        f.write(
            f'Test Accuracy of {label}: {int(100 * class_correct[label] / class_total[label])}% '
            f'({int(np.sum(class_correct[label]))}/{int(np.sum(class_total[label]))})'
        )

    f.write(
        f'\nTest Accuracy (Overall): {int(100 * np.sum(class_correct) / np.sum(class_total))}% ' 
        f'({int(np.sum(class_correct))}/{int(np.sum(class_total))})'
    )
    f.close()
