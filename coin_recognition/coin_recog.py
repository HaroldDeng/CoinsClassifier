#!/usr/bin/env python3
import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from keras.utils import to_categorical

import tf

# input to the CNN will be cropped color images of each coin we want to recognize to be converted into a 256×256×3 tensor
# recognition needs to be adaptive to the wear on the coin from cirrculation
# features on the coin such as text and ridges on the observed face may not be dependable due to limitations of the input image
# output will be of 11 different results: heads or tail of each denomination, or not_a_coin

# todo: find basis for hyperparameters, perhaps genetic algorithm trials
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
		Conv2D(num_filters,filter_size,input_shape=in_shape),
		Conv2D(num_filters,filter_size),
		MaxPooling2D(pool_size=pool_size),
		Dropout(drop_prob),
		Flatten(),
		Dense(dense_num,activation='relu'),
		Dense(11, activation='softmax'),
	])

def model_comp(model,optimizer):
	model.compile(
		optimizer,
		loss='categorical_crossentropy',
		metrics=['accuracy']
	)

coin_onehot = {
	'penny_head'  : np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
	'penny_tail'  : np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
	'nickel_head' : np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
	'nickel_tail' : np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]),
	'dime_head'   : np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]),
	'dime_tail'   : np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]),
	'quarter_head': np.array([0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]),
	'quarter_tail': np.array([0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]),
	'dollar_head' : np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]),
	'dollar_tail' : np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]),
	'not_us_coin' : np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]),
}

def model_fit(model,coin_training,epochs,val_dat):
	model.fit(
		coin_training,
		coin_onehot, #todo: what does "naming output layers" mean?
		epochs=epochs,
		validation_data=val_dat
	)

