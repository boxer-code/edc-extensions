import tenseal as ts
import torch
from torchvision import datasets
import torchvision.transforms as transforms
import numpy as np
import defs as s

def encrypt_data(kernel_shape, stride, context, test_loader):
    enc_windows = []
    data_n = []
    enc_values=[]
    target_n = []
    count = 0
    context.global_scale = pow(2, bits_scale)
    for data, target in test_loader: # Encoding and encryption
        data_n.append(data)
        target_n.append(target)
        x_enc, windows_nb = ts.im2col_encoding(
            context, data.view(28, 28).tolist(), kernel_shape[0],
            kernel_shape[1], stride
        )
        enc_windows.append(windows_nb)
        enc_values.append(x_enc)
        print("Encrypted " + str(count) + " from 500 vectors")
        count += 1
        if count >= 500:
            break
    return enc_values, enc_windows, data_n, target_n

def decrypt(context, model, data_n, target_n, criterion, kernel_shape, stride):
    test_loss = 0.0
    class_correct = list(0. for i in range(10))
    class_total = list(0. for i in range(10))
    loop = 0
    data_zipped = zip(data_n, target_n)
    for data, target in data_zipped:
        print(len(enc_learned))
        enc_o = enc_learned[loop]
        print(enc_o)
        output = enc_o.decrypt()
        output = torch.tensor(output).view(1, -1)
        print(output)
        print(data)
        loss = criterion(output, target)
        test_loss += loss.item()
        _, pred = torch.max(output, 1)
        correct = np.squeeze(pred.eq(target.data.view_as(pred)))
        label = target.data[0]
        class_correct[label] += correct.item()
        class_total[label] += 1

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

#kernel_shape = model.conv1.kernel_size
#stride = model.conv1.stride[0]

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

