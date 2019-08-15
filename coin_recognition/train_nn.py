import numpy as np
import argparse
import torch
import torch.nn as nn
from torch.autograd import Variable
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import torchvision
import torchvision.transforms as T
from torchvision.datasets import ImageFolder
from sklearn.metrics import confusion_matrix

"""
PyTorch script finetuning a ResNet model on coins data

command line to run: python train_nn.py --train_dir ~/coins/train --val_dir ~/coins/vali --test_dir ~/coins/test  --num_workers 6 --num_epochs1 40 --num_epochs2 40 --use_gpu

Training data directory structure:
finetune.py
coins/
  train/
    quarter/
    dime/
    nickel/
    penny/
  val/
    quarter/
    dime/
    nickel/
    penny/
  test/
    quarter/
    dime/
    nickel/
    penny/
"""

parser = argparse.ArgumentParser()
parser.add_argument('--train_dir', default='coins/train')
parser.add_argument('--val_dir', default='coins/vali')
parser.add_argument('--test_dir', default='coins/test')
parser.add_argument('--batch_size', default=32, type=int)
parser.add_argument('--num_workers', default=4, type=int)
parser.add_argument('--num_epochs1', default=10, type=int)
parser.add_argument('--num_epochs2', default=10, type=int)
parser.add_argument('--use_gpu', action='store_true')

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


def main(args):

  dtype = torch.FloatTensor
  if args.use_gpu:
    dtype = torch.cuda.FloatTensor

  train_transform = T.Compose([
    T.Scale(256),
    T.RandomSizedCrop(224),
    T.RandomHorizontalFlip(),
    T.ToTensor(),
    T.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
  ])

  train_dset = ImageFolder(args.train_dir, transform=train_transform)
  train_loader = DataLoader(train_dset,
                    batch_size=args.batch_size,
                    num_workers=args.num_workers,
                    shuffle=True)

  val_transform = T.Compose([
    T.Scale(224),
    T.CenterCrop(224),
    T.ToTensor(),
    T.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
  ])
  val_dset = ImageFolder(args.val_dir, transform=val_transform)
  val_loader = DataLoader(val_dset,
                  batch_size=args.batch_size,
                  num_workers=args.num_workers)
  test_dset = ImageFolder(args.test_dir, transform=val_transform)
  test_loader = DataLoader(test_dset, batch_size=args.batch_size, num_workers=args.num_workers)

  model = torchvision.models.resnet18(pretrained=True)

  num_classes = len(train_dset.classes)
  model.fc = nn.Linear(model.fc.in_features, num_classes)

  model.type(dtype)
  loss_fn = nn.CrossEntropyLoss().type(dtype)

  for param in model.parameters():
    param.requires_grad = False
  for param in model.fc.parameters():
    param.requires_grad = True

  optimizer = torch.optim.Adam(model.fc.parameters(), lr=1e-3)

  for epoch in range(args.num_epochs1):
    print('Starting epoch %d / %d' % (epoch + 1, args.num_epochs1))
    run_epoch(model, loss_fn, train_loader, optimizer, dtype)

    train_acc = check_accuracy(model, train_loader, dtype)
    val_acc = check_accuracy(model, val_loader, dtype)

    print('Train accuracy: ', train_acc)
    print('Val accuracy: ', val_acc)
    print()

  for param in model.parameters():
    param.requires_grad = True

  optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)

  for epoch in range(args.num_epochs2):
    print('Starting epoch %d / %d' % (epoch + 1, args.num_epochs2))
    run_epoch(model, loss_fn, train_loader, optimizer, dtype)

    train_acc = check_accuracy(model, train_loader, dtype)
    val_acc = check_accuracy(model, val_loader, dtype)
    print('Train accuracy: ', train_acc)
    print('Val accuracy: ', val_acc)
    print()

  test_acc = check_accuracy(model, test_loader, dtype)
  print('Test accuracy :',test_acc)


def run_epoch(model, loss_fn, loader, optimizer, dtype):
  """
  Train the model for one epoch.
  """
  model.train()

  for x, y in loader:
    x_var = Variable(x.type(dtype))
    y_var = Variable(y.type(dtype).long())

    scores = model(x_var)
    loss = loss_fn(scores, y_var)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

def check_accuracy(model, loader, dtype):
  """
  Check the accuracy of the model.
  """
  model.eval()
  num_correct, num_samples = 0, 0
  i = 0
  for x, y in loader:
    x_var = Variable(x.type(dtype), volatile=True)
    scores = model(x_var)
    _, preds = scores.data.cpu().max(1)
    num_correct += (preds == y).sum()
    num_samples += x.size(0)
  acc = float(num_correct) / num_samples

  return acc


if __name__ == '__main__':
  args = parser.parse_args()
  main(args)
