import torch
import numpy as np
import sys
# import scipy
from torch import nn, optim
# from torch.autograd.grad_mode import F
from torch.nn import functional as F
from torch.utils.data import TensorDataset
import matplotlib.pyplot as plt

eta = 0.01
p = 0.3
batch_size = 64
EPOCHS = 10


class ModelA(nn.Module):
    def __init__(self, image_size):
        super(ModelA, self).__init__()
        self.image_size = image_size
        self.fc0 = nn.Linear(self.image_size, 100)
        self.fc1 = nn.Linear(100, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = x.view(-1, self.image_size)
        x = F.relu(self.fc0(x))
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)


class ModelB(nn.Module):
    def __init__(self, image_size):
        super(ModelB, self).__init__()
        self.image_size = image_size
        self.fc0 = nn.Linear(self.image_size, 100)
        self.fc1 = nn.Linear(100, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = x.view(-1, self.image_size)
        x = F.relu(self.fc0(x))
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)


class ModelC(nn.Module):
    def __init__(self, image_size):
        super(ModelC, self).__init__()
        self.image_size = image_size
        self.dropout = nn.Dropout(p=p)
        self.fc0 = nn.Linear(self.image_size, 100)
        self.fc1 = nn.Linear(100, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = x.view(-1, self.image_size)
        x = F.relu(self.fc0(x))
        x = self.dropout(x)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.dropout(x)
        return F.log_softmax(x, dim=1)


class ModelD(nn.Module):
    def __init__(self, image_size):
        super(ModelD, self).__init__()
        self.image_size = image_size
        self.batch_norm_fc0 = nn.BatchNorm1d(image_size)
        self.fc0 = nn.Linear(self.image_size, 100)
        self.batch_norm_fc1 = nn.BatchNorm1d(100)
        self.fc1 = nn.Linear(100, 50)
        self.batch_norm_fc2 = nn.BatchNorm1d(50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = x.view(-1, self.image_size)

        x = nn.BatchNorm1d(100)(self.fc0(x))
        x = F.relu(x)
        x = nn.BatchNorm1d(50)(self.fc1(x))
        x = F.relu(x)
        x = nn.BatchNorm1d(10)(self.fc2(x))
        x = F.relu(x)

        # x = F.relu(self.fc0(x))
        # x = nn.BatchNorm1d(100)(x)
        # x = F.relu(self.fc1(x))
        # x = nn.BatchNorm1d(50)(x)
        # x = F.relu(self.fc2(x))
        # x = nn.BatchNorm1d(10)(x)

        return F.log_softmax(x, dim=1)


class ModelE(nn.Module):
    def __init__(self, image_size):
        super(ModelE, self).__init__()
        self.image_size = image_size
        self.fc0 = nn.Linear(image_size, 128)
        self.fc1 = nn.Linear(128, 64)
        self.fc2 = nn.Linear(64, 10)
        self.fc3 = nn.Linear(10, 10)
        self.fc4 = nn.Linear(10, 10)
        self.fc5 = nn.Linear(10, 10)

    def forward(self, x):
        x = x.view(-1, self.image_size)
        x = F.relu(self.fc0(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = self.fc5(x)
        return F.log_softmax(x, dim=1)


class ModelF(nn.Module):
    def __init__(self, image_size):
        super(ModelF, self).__init__()
        self.image_size = image_size
        self.fc0 = nn.Linear(image_size, 128)
        self.fc1 = nn.Linear(128, 64)
        self.fc2 = nn.Linear(64, 10)
        self.fc3 = nn.Linear(10, 10)
        self.fc4 = nn.Linear(10, 10)
        self.fc5 = nn.Linear(10, 10)

    def forward(self, x):
        x = x.view(-1, self.image_size)
        x = torch.sigmoid(self.fc0(x))
        x = torch.sigmoid(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        x = torch.sigmoid(self.fc3(x))
        x = torch.sigmoid(self.fc4(x))
        x = self.fc5(x)
        return F.log_softmax(x, dim=1)


class FinalModel(nn.Module):
    def __init__(self, image_size):
        super(FinalModel, self).__init__()
        self.image_size = image_size


def train(epoch, model, train_loader, val_loader, optimizer):
    model.train()
    train_loss = []
    train_accuracy = []
    val_loss = []
    val_accuracy = []
    for i in range(epoch):
        accumulated_loss = 0
        accumulated_accuracy = 0
        for batch_idx, (data, label) in enumerate(train_loader):
            optimizer.zero_grad()
            output = model(data)
            loss = F.nll_loss(output, label)
            accumulated_loss += F.nll_loss(output, label, reduction='sum').item()
            prediction = output.max(1, keepdim=True)[1]
            accumulated_accuracy += prediction.eq(label.view_as(prediction)).cpu().sum()
            loss.backward()
            optimizer.step()
        # print("Train set: Epoch num:{}, Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)"
        #       .format(i, accumulated_loss / len(train_loader.dataset), accumulated_accuracy, len(train_loader.dataset),
        #               100. * accumulated_accuracy / len(train_loader.dataset)))
        train_loss.append(accumulated_loss / len(train_loader.dataset))
        train_accuracy.append(100. * accumulated_accuracy / len(train_loader.dataset))
        # l, a = validation(model, val_loader)
        # val_loss.append(l)
        # val_accuracy.append(100. * a / len(val_loader.dataset))
    return train_loss, train_accuracy, val_loss, val_accuracy


def validation(model, val_loader):
    model.eval()
    # test validation
    val_loss = 0
    val_correct = 0
    with torch.no_grad():
        for (data, target) in val_loader:
            output = model(data)
            val_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            prediction = output.max(1, keepdim=True)[1]  # get the index of the max log-probability
            val_correct += prediction.eq(target.view_as(prediction)).cpu().sum()
    val_loss /= len(val_loader.dataset)
    print('\nVal set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        val_loss, val_correct, len(val_loader.dataset),
        100. * val_correct / len(val_loader.dataset)))
    return val_loss, val_correct


def test(model, test_loader):
    prediction = []
    model.eval()
    with torch.no_grad():
        for data in test_loader:
            output = model(data)
            tag = output.max(1, keepdim=True)[1]
            prediction.append(tag)
    return prediction


def main():
    train_file, tags_file, test_file, out_file = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    # load the data
    trains = np.loadtxt(train_file) / 255
    tags = np.loadtxt(tags_file)
    tests = np.loadtxt(test_file) / 255

    # change data from numpy to tensor
    trains = torch.from_numpy(trains.copy()).float()
    tags = torch.from_numpy(tags.copy()).long()
    tests = torch.from_numpy(tests.copy()).float()

    # shuffle train_X and train_Y, and split them to train and validation
    # dataset = TensorDataset(trains, tags)
    # train_loader, val_loader = torch.utils.data.random_split(dataset,
    #                                                          [int(0.8 * len(trains)), int(0.2 * len(trains))])

    # # define ratio of validation set and train set - 80:20
    # validation_num = int(0.8 * len(trains))
    #
    # # convert data into DatsSet and split data to validation and training sets
    # train_loader = TensorDataset(trains, tags)
    # val_dataSet = TensorDataset(trains[validation_num:], tags[validation_num:])
    #
    # train_loader = torch.utils.data.DataLoader(train_loader, shuffle=True, batch_size=batch_size)
    # val_loader = torch.utils.data.DataLoader(val_loader, shuffle=False, batch_size=batch_size)
    # test_loader = torch.utils.data.Dataloader(TensorDataset(tests), batch_size=batch_size)

    # model_a = ModelA(784)
    # optimizer_a = optim.SGD(model_a.parameters(), lr=eta)
    #
    # model_b = ModelB(784)
    # optimizer_b = optim.Adam(model_b.parameters(), lr=eta)

    # model_c = ModelC(784)
    # optimizer_c = optim.Adam(model_c.parameters(), lr=eta)
    #
    # model_d = ModelD(784)
    # optimizer_d = optim.Adam(model_d.parameters(), lr=eta)
    #
    # model_e = ModelE(784)
    # optimizer_e = optim.Adam(model_e.parameters(), lr=eta)
    #
    # model_f = ModelF(784)
    # optimizer_f = optim.Adam(model_f.parameters(), lr=eta)

    # loss_t, accuracy_t, loss_v, accuracy_v = train(EPOCHS, model_c, train_loader, val_loader, optimizer_c)

    # # loss plot
    # plt.plot(range(EPOCHS), loss_t, label="train loss")
    # plt.plot(range(EPOCHS), loss_v, label="validation loss")
    # plt.xlabel('Epoch')
    # plt.ylabel('Average loss')
    # plt.title('Model C')
    # plt.legend()
    # plt.show()
    #
    # # accuracy plot
    # plt.plot(range(EPOCHS), accuracy_t, label="train accuracy")
    # plt.plot(range(EPOCHS), accuracy_v, label="validation accuracy")
    # plt.xlabel('Epoch')
    # plt.ylabel('Accuracy')
    # plt.title('Model C')
    # plt.legend()
    # plt.show()
    #

    # test model

    model_d = ModelD(784)
    optimizer_d = optim.Adam(model_d.parameters(), lr=eta)

    train_dataset = TensorDataset(trains, tags)
    train_loader = torch.utils.data.DataLoader(train_dataset, shuffle=True, batch_size=batch_size)
    test_dataset = TensorDataset(tests)
    test_loader = torch.utils.data.DataLoader(test_dataset, shuffle=False, batch_size=batch_size)
    loss_t, accuracy_t, loss_v, accuracy_v = train(EPOCHS, model_d, train_loader, "Hello world", optimizer_d)
    predictions = test(model_d, test_loader)
    with open(out_file, "w") as f:
        for ind, tag in enumerate(predictions):
            if ind != 4999:
                f.write("%s\n" % tag[1].item())
            else:
                f.write("%s" % tag[1].item())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
