# Tamar Saad 207256991
# Efraim Rahamim 315392621

import numpy as np
# import sys
from torch import nn, optim
# from torchsummary import summary
import os
import os.path
import soundfile as sf
import librosa
import torch
import torch.utils.data as data
from torch.nn import functional as F
# from torch.utils.data import TensorDataset
# import matplotlib.pyplot as plt

AUDIO_EXTENSIONS = [
    '.wav', '.WAV',
]


def is_audio_file(filename):
    return any(filename.endswith(extension) for extension in AUDIO_EXTENSIONS)


def find_classes(dir):
    classes = [d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))]
    classes.sort()
    class_to_idx = {classes[i]: i for i in range(len(classes))}
    return classes, class_to_idx


def make_dataset(dir, class_to_idx):
    spects = []
    dir = os.path.expanduser(dir)
    for target in sorted(os.listdir(dir)):
        d = os.path.join(dir, target)
        if not os.path.isdir(d):
            continue

        for root, _, fnames in sorted(os.walk(d)):
            for fname in sorted(fnames):
                if is_audio_file(fname):
                    path = os.path.join(root, fname)
                    item = (path, class_to_idx[target])
                    spects.append(item)
    return spects


def spect_loader(path, window_size, window_stride, window, normalize, max_len=101):
    y, sr = sf.read(path)
    # n_fft = 4096
    n_fft = int(sr * window_size)
    win_length = n_fft
    hop_length = int(sr * window_stride)

    # STFT
    D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length,
                     win_length=win_length, window=window)
    spect, phase = librosa.magphase(D)

    # S = log(S+1)
    spect = np.log1p(spect)

    # make all spects with the same dims
    # TODO: change that in the future
    if spect.shape[1] < max_len:
        pad = np.zeros((spect.shape[0], max_len - spect.shape[1]))
        spect = np.hstack((spect, pad))
    elif spect.shape[1] > max_len:
        spect = spect[:, :max_len]
    spect = np.resize(spect, (1, spect.shape[0], spect.shape[1]))
    spect = torch.FloatTensor(spect)

    # z-score normalization
    if normalize:
        mean = spect.mean()
        std = spect.std()
        if std != 0:
            spect.add_(-mean)
            spect.div_(std)

    return spect


class GCommandLoader(data.Dataset):
    """A google command data set loader where the wavs are arranged in this way: ::
        root/one/xxx.wav
        root/one/xxy.wav
        root/one/xxz.wav
        root/head/123.wav
        root/head/nsdf3.wav
        root/head/asd932_.wav
    Args:
        root (string): Root directory path.
        transform (callable, optional): A function/transform that  takes in an PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
        window_size: window size for the stft, default value is .02
        window_stride: window stride for the stft, default value is .01
        window_type: typye of window to extract the stft, default value is 'hamming'
        normalize: boolean, whether or not to normalize the spect to have zero mean and one std
        max_len: the maximum length of frames to use
     Attributes:
        classes (list): List of the class names.
        class_to_idx (dict): Dict with items (class_name, class_index).
        spects (list): List of (spects path, class_index) tuples
        STFT parameter: window_size, window_stride, window_type, normalize
    """

    def __init__(self, root, transform=None, target_transform=None, window_size=.02,
                 window_stride=.01, window_type='hamming', normalize=True, max_len=101):
        classes, class_to_idx = find_classes(root)
        spects = make_dataset(root, class_to_idx)

        if len(spects) == 0:
            raise (RuntimeError(
                "Found 0 sound files in subfolders of: " + root + "Supported audio file extensions are: " + ",".join(
                    AUDIO_EXTENSIONS)))

        self.root = root
        self.spects = spects
        self.classes = classes
        self.class_to_idx = class_to_idx
        self.transform = transform
        self.target_transform = target_transform
        self.loader = spect_loader
        self.window_size = window_size
        self.window_stride = window_stride
        self.window_type = window_type
        self.normalize = normalize
        self.max_len = max_len
        self.len = len(self.spects)

    def __getitem__(self, index):
        """
        Args:
            index (int): Index
        Returns:
            tuple: (spect, target) where target is class_index of the target class.
        """
        # print(index)
        path, target = self.spects[index]
        spect = self.loader(path, self.window_size, self.window_stride, self.window_type, self.normalize, self.max_len)
        # print (path)
        if self.transform is not None:
            spect = self.transform(spect)
        if self.target_transform is not None:
            target = self.target_transform(target)

        return spect, target

    def __len__(self):
        return self.len


# if torch.cuda.is_available():
#   device  = torch.device("cuda:0")
#   print("GPU")
# else:
#   device = torch.device("cpu")
#   print("CPU")

lr = 0.001
EPOCHS = 5


# from google.colab import drive
# # Tamar -------------------------------------------------------
# #drive.mount('/content/drive')
# #!unzip "/content/drive/MyDrive/ex5_ML/data.zip" -d "/content"
# # -------------------------------------------------------------
#
# # Efi ---------------------------------------------------------
# drive.mount('/content/drive')
# !unzip "/content/drive/MyDrive/ML_ex5/data.zip" -d "/content"
# # -------------------------------------------------------------

class CNN(nn.Module):
    def __init__(self, size1, size2, size3, size4, size5, size6):
        super().__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(
                in_channels=size1,
                out_channels=size2,
                kernel_size=3,
                stride=1,
                padding=2
            ),
            nn.BatchNorm2d(size2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
            # nn.Dropout(0.1)
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(
                in_channels=size2,
                out_channels=size3,
                kernel_size=3,
                stride=1,
                padding=2
            ),
            nn.BatchNorm2d(size3),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
            # nn.Dropout(0.1)
        )
        self.conv3 = nn.Sequential(
            nn.Conv2d(
                in_channels=size3,
                out_channels=size4,
                kernel_size=3,
                stride=1,
                padding=2
            ),
            nn.BatchNorm2d(size4),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
            # nn.Dropout(0.1)
        )
        self.conv4 = nn.Sequential(
            nn.Conv2d(
                in_channels=size4,
                out_channels=size5,
                kernel_size=3,
                stride=1,
                padding=2
            ),
            nn.BatchNorm2d(size5),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
            # nn.Dropout(0.1)
        )
        self.conv5 = nn.Sequential(
            nn.Conv2d(
                in_channels=size5,
                out_channels=size6,
                kernel_size=3,
                stride=1,
                padding=2
            ),
            nn.BatchNorm2d(size6),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
            # nn.Dropout(0.1)
        )
        self.flatten = nn.Flatten()
        self.linear1 = nn.Linear(7680, 30)
        # self.linear2 = nn.Linear(11264, 256)
        # self.linear3 = nn.Linear(22528, 30)

    def forward(self, input_data):
        x = self.conv1(input_data)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.conv5(x)

        # x = x.view(x.size(0), -1)
        x = self.flatten(x)
        # x = F.relu(self.linear1(x))
        # x = F.relu(self.linear2(x))
        # x = F.relu(self.linear3(x))
        logits = self.linear1(x)

        predictions = F.log_softmax(logits, dim=1)
        return predictions


cnn = CNN(1, 16, 32, 64, 128, 256)  # .cuda()
# loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(cnn.parameters(), lr=lr)


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
            # data, label = data.cuda(), label.cuda()
            optimizer.zero_grad()
            output = model(data)
            loss = F.nll_loss(output, label)
            accumulated_loss += F.nll_loss(output, label, reduction='sum').item()
            prediction = output.max(1, keepdim=True)[1]
            accumulated_accuracy += prediction.eq(label.view_as(prediction)).cpu().sum()
            loss.backward()
            optimizer.step()
        # print("Train set: Epoch num:{}, Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)"
        #       .format(i + 1, accumulated_loss / len(train_loader.dataset), accumulated_accuracy,
        #               len(train_loader.dataset),
        #               100. * accumulated_accuracy / len(train_loader.dataset)))
        train_loss.append(accumulated_loss / len(train_loader.dataset))
        train_accuracy.append(100. * accumulated_accuracy / len(train_loader.dataset))
        l, a = validation(model, val_loader)
        val_loss.append(l)
        val_accuracy.append(100. * a / len(val_loader.dataset))
    return train_loss, train_accuracy, val_loss, val_accuracy


def validation(model, val_loader):
    model.eval()
    # test validation
    val_loss = 0
    val_correct = 0
    with torch.no_grad():
        for (data, target) in val_loader:
            # data, target = data.cuda(), target.cuda()
            output = model(data)
            val_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            prediction = output.max(1, keepdim=True)[1]  # get the index of the max log-probability
            val_correct += prediction.eq(target.view_as(prediction)).cpu().sum()
    val_loss /= len(val_loader.dataset)
    # # reduction='sum'
    # print('\nVal set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
    #     val_loss, val_correct, len(val_loader.dataset),
    #     100. * val_correct / len(val_loader.dataset)))
    return val_loss, val_correct


def test(model, test_loader):
    model.eval()
    prediction = []
    with torch.no_grad():
        for (data, t) in test_loader:
            # data, t = data.cuda(), t.cuda()
            output = model(data)
            tag = output.max(1, keepdim=True)[1]
            tag_view = tag.view(len(tag))
            for p in tag_view:
                prediction.append(p.item())
    return prediction


def main():
    dataset_train = GCommandLoader('./gcommands/train')
    dataset_val = GCommandLoader('./gcommands/valid')
    dataset_test = GCommandLoader('./gcommands/test')

    train_loader = torch.utils.data.DataLoader(
        dataset_train, batch_size=64, shuffle=True,
        pin_memory=True)

    val_loader = torch.utils.data.DataLoader(
        dataset_val, batch_size=64, shuffle=True,
        pin_memory=True)

    test_loader = torch.utils.data.DataLoader(
        dataset_test, batch_size=1, shuffle=False,
        pin_memory=True)

    ind_to_class = {}
    for key, value in dataset_train.class_to_idx.items():
        ind_to_class[value] = key

    loss_t, accuracy_t, loss_v, accuracy_v = train(EPOCHS, cnn, train_loader, val_loader, optimizer)
    predictions = test(cnn, test_loader)

    predicted_classes = []
    for pred in predictions:
        predicted_classes.append(ind_to_class[pred])

    prefix_files = []
    for root, _, f_names in sorted(os.walk('./gcommands/test')):
        for f_name in sorted(f_names):
            if f_name == '.DS_Store': continue
            prefix_files.append(int(f_name.split('.')[0]))

    with open("test_y", "w") as f:
        for prefix, pred_class in sorted(zip(prefix_files, predicted_classes)):
            f.writelines(str(prefix) + '.wav' + ',' + pred_class + '\n')



if __name__ == '__main__':
    main()
