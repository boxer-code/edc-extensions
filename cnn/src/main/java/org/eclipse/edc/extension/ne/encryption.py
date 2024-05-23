import requests
# import pickle
from base64 import b64encode
from flask import *
from torchvision import datasets
import torchvision.transforms as transforms

import defs as s
from App import *
from App_decryption import *


def encrypt():
    response = requests.get("http://localhost:8181/api/data")

    vecs = []

    try:
        if s.model != None:
            pass
    except AttributeError as e:
        "<p>Data has to be set first! Please perform /data!</p>"

    test_data = datasets.MNIST('data', train=False, download=True, transform=transforms.ToTensor())
    test_loader = torch.utils.data.DataLoader(test_data, batch_size=1, shuffle=True)

    with open('kernel.txt', 'r') as file:
        json_data = file.read()
    kern = json.loads(json_data)
    print(kern)
    kernel = kern["kernel_shape"]
    stride = kern["stride"]

    s.enc, s.windows_nb, s.data, s.target = encrypt_data(kernel, stride, s.context, test_loader)
    encrypted =[]
    count = 0
    for enc in s.enc:
        vec = enc.serialize()
        vec_new = b64encode(vec).decode()
        encrypted.append(vec_new)
        #if count == 2:
        #    break

    ser_ctx = b64encode(s.context.serialize()).decode()
    global ctx
    ctx = ser_ctx
    global encvector
    encvector = encrypted
    global data
    data = encrypted
    global windows
    windows = s.windows_nb
    print("Sucessfully encrypted and ready to be send!")
    return data

context.global_scale = pow(2, bits_scale)
result = encrypt()
