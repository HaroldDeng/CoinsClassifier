#!/usr/bin/env python3
import csv
import json
import pathlib as pl

import numpy as np
import cv2

coin_onehot_assigns = {
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

# goal: accumulate the date of the nested directories as a numpy array of shape:
# (num_images,256,256,3) where num_images is the number of cropped images

def read_directories(dirroot):
	out = {
		"dime":{"head":{"images":[],"regions":None},
		        "tail":{"images":[],"regions":None}},
		"dollar": {"head":{"images":[],"regions":None},
		           "tail":{"images":[],"regions":None}},
		"nickel":{"head":{"images":[],"regions":None},
		          "tail":{"images":[],"regions":None}},
		"non_coin":{"images":[],"regions":None},
		"penny":{"head":{"images":[],"regions":None},
		         "tail":{"images":[],"regions":None}},
		"quarter":{"head":{"images":[],"regions":None},
		           "tail":{"images":[],"regions":None}},
	}
	for s0 in pl.Path(dirroot).iterdir():
		if s0.isdir():
			for s1 in s0.iterdir():
				if s1.isdir():
					for s2 in s1.iterdir():
						if s2.suffix == '.jpg':
							out[s0.name][s1.name]["images"].append(s2)
						elif s2.suffix == '.csv':
							out[s0.name][s1.name]["regions"] = s2
				elif s0.name == "non_coin":
					if s1.suffix == '.jpg':
						out[s0.name]["images"].append(s1)
					elif s1.suffix == '.csv':
						out[s0.name]["regions"] = s1
	return out

def apply_region_info(im_re_dict):
	"output a list of numpy arrays with region info applied"
	# read images -> dict of filename to numpy array
	# read regions csv for data -> list of dict's
	# apply crop and resize per images -> list of numpy array
	images = im_re_dict["images"]
	arrays = { img.name: cv2.imread(str(img),cv2.IMREAD_COLOR) for img in images}
	regions_fn = im_re_dict["regions"]
	region_info = []
	with regions_fn.open() as f:
		rdr = csv.DictReader(f)
		for row in rdr:
			shape_attr = json.loads(row['region_shape_attributes'])
			row_pr = { "filename": row['#filename'], "resize": shape_attr }
			region_info.append(row_pr)
	cropped_images = []
	for ri in region_info:
		fn = ri["filename"]
		resize = ri["resize"]
		rx = resize["x"]
		ry = resize["y"]
		rw = resize["width"]
		rh = resize["height"]
		if fn in arrays:
			arr = arrays[fn].copy()
			cropped_images.append(cv2.resize(arr[rx:rw, ry:rh, :], (256,256)))
	return cropped_images

# optional step: rotations, changing hue, etc.
# next step: stack arrays, and track the accumulation to generate the outputs array for the other "side" of the training data sent to keras' fit method

def accum_stacked_arrays(hierarchy,other_steps=(lambda x: [x])):
	"returns tuple of 2 numpy arrays, first is training input, and second is expected outputs"
	non_coin_imgs = apply_region_info(
	for k0 in hierarchy:
		pass
			
	