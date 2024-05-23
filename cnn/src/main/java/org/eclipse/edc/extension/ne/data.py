import tenseal as ts
from flask import *

import defs as s
from App import *
from App_decryption import *


def data():
    print("Received Data Request!")

    ## Encryption Parameters

    # controls precision of the fractional part
    bits_scale = 26

    # Create TenSEAL context
    s.context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[31, bits_scale, bits_scale, bits_scale, bits_scale, bits_scale, bits_scale, 31]
    )

    # set the scale
    s.context.global_scale = pow(2, bits_scale)
    print(s.context.global_scale)
    # galois keys are required to do ciphertext rotations
    s.context.generate_galois_keys()
    return "<p>Sucessfully started Encryption!</p>"

data()
