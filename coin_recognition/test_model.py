import torch
import torchvision
from torchvision.datasets import ImageFolder
import argparse
from torch.utils.data import DataLoader
import torch.nn as nn
import torchvision.transforms as T
from torch.autograd import Variable
'''
to run: python test_model.py --test_dir ~/cv/coins/test --use_gpu
'''
parser = argparse.ArgumentParser()
parser.add_argument('--test_dir', default='coins/test')
parser.add_argument('--batch_size', default=32, type=int)
parser.add_argument('--num_workers', default=4, type=int)
#parser.add_argument('--num_epochs1', default=10, type=int)
#parser.add_argument('--num_epochs2', default=10, type=int)
parser.add_argument('--use_gpu', action='store_true')

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

def main(args):
    dtype = torch.FloatTensor
    if args.use_gpu:
      dtype = torch.cuda.FloatTensor
    
    val_transform = T.Compose([
    T.Scale(224),
    T.CenterCrop(224),
    T.ToTensor(),
    T.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
  ])
    test_dset = ImageFolder(args.test_dir, transform=val_transform)
    test_loader = DataLoader(test_dset, batch_size=args.batch_size, num_workers=args.num_workers)

    model = load_model('classifier.pth',test_dset,dtype)
    test_acc, cents = check_accuracy(model, test_loader, dtype)
    print("test accuracy", test_acc,"%")
    print("number of cents in image",cents)

def load_model(checkpoint_path,test_dset,dtype):
    chpt = torch.load(checkpoint_path)
    
    model =torchvision.models.resnet18(pretrained=True)
    
    model.class_to_idx = chpt['class_to_idx']
    
    num_classes = len(test_dset.classes)
    print(test_dset.classes)
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    model.type(dtype)
    loss_fn = nn.CrossEntropyLoss().type(dtype)

    for param in model.parameters():
       param.requires_grad = False
    for param in model.fc.parameters():
       param.requires_grad = True

    optimizer = torch.optim.Adam(model.fc.parameters(), lr=1e-3)
    # Put the classifier on the pretrained network
   # model.classifier = classifier
    
    model.load_state_dict(chpt['state_dict'])
    
    return model

def check_accuracy(model, loader, dtype):
  model.eval()
  model.cuda()
  num_correct, num_samples = 0, 0
  num_dime, num_nickel, num_penny, num_quarter = 0, 0, 0, 0
  i = 0
  
  for x, y in loader:
    x_var = Variable(x.type(dtype), volatile=True)
    scores = model(x_var)
    _, preds = scores.data.cpu().max(1)
    num_dime += (preds==0).sum()
    num_nickel += (preds==1).sum()
    num_penny += (preds==2).sum()
    num_quarter += (preds==3).sum()
    
    num_correct += (preds == y).sum()
    num_samples += x.size(0)
  cents = float(num_dime)*10+float(num_nickel)*5+float(num_penny)+float(num_quarter)*25
  acc = float(num_correct) / num_samples*100

  return acc, cents

if __name__ == '__main__':
  args = parser.parse_args()
  main(args)
