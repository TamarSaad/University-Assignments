""""
Tamar Saad: 207256991
Efraim Rahamim: 315392621
"""""

import numpy as np
import sys
from torch import nn
from torchsummary import summary
from gcommand_dataset import GCommandLoader
import os
import os.path
import soundfile as sf
import librosa
import numpy as np
import torch
import torch.utils.data as data


lr = 0.001
epochs = 10

class CNN(nn.Module):
    def __init__(self, size1, size2, size3, size4, size5):
        super().__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(
                in_channels=size1,
                out_channels=size2,
                kernel_size=3,
                stride=1,
                padding=2
            ),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(
                in_channels=size2,
                out_channels=size3,
                kernel_size=3,
                stride=1,
                padding=2
            ),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        self.conv3 = nn.Sequential(
            nn.Conv2d(
                in_channels=size3,
                out_channels=size4,
                kernel_size=3,
                stride=1,
                padding=2
            ),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        self.conv4 = nn.Sequential(
            nn.Conv2d(
                in_channels=size4,
                out_channels=size5,
                kernel_size=3,
                stride=1,
                padding=2
            ),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        self.flatten = nn.Flatten()
        self.linear = nn.Linear(11264, 30)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, input_data):
        x = self.conv1(input_data)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.flatten(x)
        logits = self.linear(x)
        predictions = self.softmax(logits)
        return predictions

def train(model, epochs, data_loader, optimizer, loss_fn):
    for i in range (epochs):
        for x,y in data_loader:
            prediction = model.forward(x)
            loss = loss_fn(prediction, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

def main():

    dataset_train = GCommandLoader('../data/data/train')
    dataset_val = GCommandLoader('../data/data/valid')
    dataset_test = GCommandLoader('../data/data/test')

    train_loader = torch.utils.data.DataLoader(
        dataset_train, batch_size=100, shuffle=None,
        num_workers=20, pin_memory=True, sampler=None)

    cnn = CNN(1, 16, 32, 64, 128)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(cnn.parameters(), lr=lr)

    train(cnn, epochs, train_loader, optimizer, loss_fn)




if __name__ == '__main__':
    main()
    #summary(cnn, (1, 161, 101))
