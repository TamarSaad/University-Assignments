from gcommand_dataset import GCommandLoader
import torch

dataset_train = GCommandLoader('../data/data/train')
dataset_val = GCommandLoader('../data/data/val')
dataset_test = GCommandLoader('../data/data/test')

test_loader = torch.utils.data.DataLoader(
    dataset_train, batch_size=100, shuffle=None,
    num_workers=20, pin_memory=True, sampler=None)

# for k, (input, label) in enumerate(test_loader):
#     print(input.size(), len(label))

