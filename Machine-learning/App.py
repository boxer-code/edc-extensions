import tenseal as ts
import torch
from torchvision import datasets
import torchvision.transforms as transforms
import numpy as np
from EncConvNet import *
import state as s

def encrypt_data(model, context, test_loader):
    enc_values = []
    enc_windows = []
    data_n = []
    target_n = []
    count = 0
    for data, target in test_loader: # Encoding and encryption
        data_n.append(data)
        target_n.append(target)
        x_enc, windows_nb = ts.im2col_encoding(
            context, data.view(28, 28).tolist(), kernel_shape[0],
            kernel_shape[1], stride
        )
        enc_windows.append(windows_nb)

        enc_channels = []
        for kernel, bias in zip(model.conv1_weight, model.conv1_bias):
            y = x_enc.conv2d_im2col(kernel, windows_nb) + bias
            enc_channels.append(y)
        enc_x = ts.CKKSVector.pack_vectors(enc_channels)
        enc_values.append(enc_x)
        print("Enrypted ", count, "  vectors from 500")
        count += 1
        if count >= 500:
            break
    return enc_values, windows_nb, data_n, target_n

def decrypt(context, model, data_n, target_n, criterion, kernel_shape, stride):
    # initialize lists to monitor test loss and accuracy
    test_loss = 0.0
    class_correct = list(0. for i in range(10))
    class_total = list(0. for i in range(10))
    loop = 0
    data_zipped = zip(data_n, target_n)
    #Verschlüsselung der Daten
    for data, target in data_zipped:

        print(len(enc_learned))
        enc_o = enc_learned[loop]
        print(enc_o)
            # Decryption of result
        output = enc_o.decrypt()
        output = torch.tensor(output).view(1, -1)
        print(output)
        print(data)
            # compute loss
        loss = criterion(output, target)
        test_loss += loss.item()
            
            # convert output probabilities to predicted class
        _, pred = torch.max(output, 1)
            # compare predictions to true label
        correct = np.squeeze(pred.eq(target.data.view_as(pred)))
            # calculate test accuracy for each object class
        label = target.data[0]
        print("label")
        print(label)
        class_correct[label] += correct.item()
        class_total[label] += 1
        loop += 1
        if loop >= 50:
            break

        # calculate and print avg test loss
    test_loss = test_loss / sum(class_total)
    print(f'Test Loss: {test_loss:.6f}\n')

    for label in range(10):
        if (class_total[label]> 0):
            print(
                f'Test Accuracy of {label}: {int(100 * class_correct[label] / class_total[label])}% '
                f'({int(np.sum(class_correct[label]))}/{int(np.sum(class_total[label]))})'
            )

    print(
        f'\nTest Accuracy (Overall): {int(100 * np.sum(class_correct) / np.sum(class_total))}% ' 
        f'({int(np.sum(class_correct))}/{int(np.sum(class_total))})'
    )


kernel_shape = model.conv1.kernel_size
stride = model.conv1.stride[0]

## Encryption Parameters

# controls precision of the fractional part
bits_scale = 26

# Create TenSEAL context
context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=8192,
    coeff_mod_bit_sizes=[31, bits_scale, bits_scale, bits_scale, bits_scale, bits_scale, bits_scale, 31]
)

# set the scale
context.global_scale = pow(2, bits_scale)

# galois keys are required to do ciphertext rotations
context.generate_galois_keys()

