# CoinsClassifier
An image recognition  project for CSCI 4962

## How It Works
Labeling
- Making a dataset by photograph U.S. coins, in total our team took around 800 photos.
- Organize into folders of each type of coin and subfolders of heads and tails and a folder of non-U.S. coins
- Label the position of each individual coin in the photo using VGG Image Annotator, store data in .csv files. In total our team labeled 430 photos.

Preprocessing/ Masking
- Downsizing images to 224 x 224 pixels for Neural net (ResNet18)
- Apply filters, increases contrast between coins and background. Pyramid mean shift and gaussian blur are being used

Model Hyperparameters
- Batch size 32
- Architecture: RestNet18
- 18 layers
- Adam optimizer, learning rate 10^-5
- Number of epochs: 80
- Loss function: Cross Entropy Loss
- Fully connected layer: linear layer

## Dependencies
- Python 3.6 or 3.7
- Pytorch 0.40
- Python 3.6
- Numpy
- Flask
- OpenCV 3

##Links
#Project Repository
https://github.com/HaroldDeng/CoinsClassifier.git
#Labeled Image Repository
https://github.com/HaroldDeng/Object_Recognition_Coins_Dataset_U.S..git

##Keywords
-pyramid mean shift
-gaussian blur
-hough circles
-neural net
-cnn
-webapp
