import torch
from torchvision import datasets
import torchvision.transforms as transforms
import pickle
import numpy as np
import convnet as co
import io
from base64 import b64encode
import tenseal as ts

#torch.manual_seed(73)

train_data = datasets.MNIST('data', train=True, download=True, transform=transforms.ToTensor())
test_data = datasets.MNIST('data', train=False, download=True, transform=transforms.ToTensor())

batch_size = 64

train_loader = torch.utils.data.DataLoader(train_data, batch_size=batch_size, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_data, batch_size=batch_size, shuffle=True)


def train(model, train_loader, criterion, optimizer, n_epochs=10):
    # model in training mode
    model.train()
    for epoch in range(1, n_epochs + 1):

        train_loss = 0.0
        for data, target in train_loader:
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        # calculate average losses
        train_loss = train_loss / len(train_loader)

        print('Epoch: {} \tTraining Loss: {:.6f}'.format(epoch, train_loss))

    # model in evaluation mode
    model.eval()
    return model


# Model aus Datei laden
with (open("model.pt", "rb")) as f:
    pickload = pickle.load(f)
buffer = io.BytesIO()
torch.save(pickload, buffer)

# Setze die Position des Puffers auf den Anfang
buffer.seek(0)

# Lade das Modell aus dem Puffer
loaded_model = torch.load(buffer, map_location=torch.device('cpu'))
#model = torch.load(pickload)
print(loaded_model)
model = co.ConvNet()
model.load_state_dict(loaded_model)
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
# model muss jedes Mal geupdated werden, transport?
model = train(model, train_loader, criterion, optimizer, 10)
#torch.save(model.state_dict(), "model.pt")
weights = []
param_ten = []
for param_tensor in model.state_dict():
    print(param_tensor)
    param_ten.append(param_tensor)
    weights.append(model.state_dict()[param_tensor])
    print(weights)

# Initialisieren Sie TenSeal Context
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

ser_ctx = b64encode(context.serialize()).decode()
global ctx
ctx = ser_ctx
# Erstellen Sie ein Tensor-Objekt für jeden Gewichtstensor und verschlüsseln Sie es
global weights_lists
encrypted_weights = []
weights_lists = []
n = 0
for weight in weights:
    new = []
    print(param_ten)
    new.append(param_ten[n])
    n = n + 1
    print(weight)
    print(weight.numpy().shape)
    if len(weight.numpy().shape) == 1:
         encrypted_weight = ts.ckks_vector(context, j)
         encrypted_weights.append(encrypted_weight)
         new.append(encrypted_weight)
    else:
        for w in weight.numpy():
            print("Hier")
            print(len(w.shape))
            if len(w.shape) == 1:
                 encrypted_weight = ts.ckks_vector(context, w)
                 vec = encrypted_weight.serialize()
                 vec_new = b64encode(vec).decode()
                 new.append(vec_new)
                 encrypted_weights.append(encrypted_weight)
            else:
                for i in w:
                    print("Dort")
                    print(i.shape)
                    if len(i.shape) == 1:
                         encrypted_weight = ts.ckks_vector(context, i)
                         vec = encrypted_weight.serialize()
                         vec_new = b64encode(vec).decode()
                         new.append(vec_new)
                         encrypted_weights.append(encrypted_weight)
                    else:
                        for j in i:
                            print("Dort2")
                            print(j.shape)
                            encrypted_weight = ts.ckks_vector(context, j)
                            print(encrypted_weight)
                            vec = encrypted_weight.serialize()
                            vec_new = b64encode(vec).decode()
                            new.append(vec_new)
                            encrypted_weights.append(encrypted_weight)
    print("NEW")
    print(new)
    #Liste an Gewichten und darauf Tensoren
    weights_lists.append(new)
print(weights_lists)
#print(encrypted_weights)
#Hier verschlüsseln?
#global updated
#updated = pickle.dumps(model.state_dict())
#print(updated)
