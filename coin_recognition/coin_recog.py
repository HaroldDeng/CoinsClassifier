#!/usr/bin/env python3
import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from keras.utils import to_categorical

import tensorflow as tf

# input to the CNN will be cropped color images of each coin we want to recognize to be converted into a 256×256×3 tensor
# recognition needs to be adaptive to the wear on the coin from cirrculation
# features on the coin such as text and ridges on the observed face may not be dependable due to limitations of the input image
# output will be of 11 different results: heads or tail of each denomination, or not_a_coin

# num_filters=256 ? size of rescaled images
# filter_size=3 ? based on CIFAR-10 example
# in_shape=(256,256,3) based on rescaling using opencv and taking color images
# pool_size= 2
# drop_prob= 0.25
# dense_num = 512 ? consider performance of resulting NN
def construct_coin_model(
		num_filters,
		filter_size,
		in_shape,
		pool_size,
		drop_prob,
		dense_num):
	# todo: any more layers needed (see imagenet architecture paper)
	return Sequential([
		# todo: strides needed for convolve?
		Conv2D(
			num_filters,
			filter_size,
			padding='same',
			activation='relu',
			data_format='channels_last' # dist to other layers
			input_shape=in_shape
		),
		Conv2D(num_filters,filter_size,activation='relu'),
		MaxPooling2D(pool_size=pool_size),
		Dropout(drop_prob),
		Conv2D(num_filters*2,filter_size,activation='relu',padding='same'),
		Conv2D(num_filters*2,filter_size,activation='relu'),
		MaxPooling2D(pool_size=pool_size),
		Dropout(drop_prob),
		Flatten(),
		Dense(dense_num,activation='relu'),
		Dropout(drop_prob*2),
		Dense(11, activation='softmax'),
	])

def model_comp(model,optimizer):
	model.compile(
		optimizer,
		loss='categorical_crossentropy',
		metrics=['accuracy']
	)

def model_fit(model,coin_training,coin_onehot,epochs,val_dat):
	model.fit(
		coin_training,
		coin_onehot, #todo: what does "naming output layers" mean?
		epochs=epochs,
		validation_split=0.1 # consider shuffling coin_training along axis
	)



