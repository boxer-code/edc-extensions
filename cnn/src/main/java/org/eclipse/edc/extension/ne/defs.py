import tenseal as ts

bits_scale = 26
model = None
enc = None
data = []
target = []
context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[31, bits_scale, bits_scale, bits_scale, bits_scale, bits_scale, bits_scale, 31]
    )
windows_nb = None
image_number = 0
encrypt_result = None
