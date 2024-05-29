import json
from base64 import b64decode
from flask import *
import torch
import numpy as np

import defs as s
from App import *
from App_decryption import *


def enc():
    #Verschlüsselte Ergebnisse vom Service
    datei = open('result.txt','r')
    data = json.load(datei)
    enc = data['learned_data']
    #Kontext dekodieren
    vectors = []
    #Jeden Vektor wieder b64 dekodieren
    for d in enc:
        ck_vector = b64decode(d)
        vectors.append(ck_vector)
    ctx = b64decode(data['context'])
    #Kontext deserialisieren
    ctx_d = ts.context_from(ctx)
    enc_d= []
    #Rekonstruieren der Vektoren
    for vec in vectors:
        enc_vec = ts.ckks_vector_from(s.context, vec)
        enc_d.append(enc_vec)
    decrypt_test(s.data, s.target, enc_d, criterion)
    return ("<p>Sucessfully encrypted and tested!</p>")

criterion = torch.nn.CrossEntropyLoss()
enc()
