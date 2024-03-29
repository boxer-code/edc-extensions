import torch
from torchvision import datasets
import torchvision.transforms as transforms
import pickle
import numpy as np
import convnet as co
import io

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
print("The loaded model is:: ")
print(loaded_model)
model = co.ConvNet()
model.load_state_dict(loaded_model)
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
# model muss jedes Mal geupdated werden, transport?
model = train(model, train_loader, criterion, optimizer, 10)
torch.save(model.state_dict(), "model.pt")
#global updated
#updated = pickle.dumps(model.state_dict())
#print(updated)
