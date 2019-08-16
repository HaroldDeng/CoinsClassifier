#!/usr/bin/env python3
import csv
import json
import pathlib as pl

import numpy as np
import cv2

# coin_onehot_assigns = {
# 	'penny_head'  : np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
# 	'penny_tail'  : np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
# 	'nickel_head' : np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
# 	'nickel_tail' : np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]),
# 	'dime_head'   : np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]),
# 	'dime_tail'   : np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]),
# 	'quarter_head': np.array([0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]),
# 	'quarter_tail': np.array([0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]),
# 	'dollar_head' : np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]),
# 	'dollar_tail' : np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]),
# 	'not_us_coin' : np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]),
# }


# new goal: process images with region info, then output to new nested directory structure

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
		if s0.is_dir():
			for s1 in s0.iterdir():
				if s1.is_dir():
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
	parent = images[0].parent
	arrays = {img: cv2.imread(str(img),cv2.IMREAD_COLOR) for img in images}
	regions_file = im_re_dict["regions"]
	region_info = []
	with regions_file.open() as f:
		for row in csv.DictReader(f):
			shape_attr = json.loads(row['region_shape_attributes'])
			row_pr = {
				"filename": row['#filename'],
				"resize": shape_attr
				"region_id": row["region_id"]
			}
			region_info.append(row_pr)
	for ri in region_info:
		fn = ri["filename"]
		resize = ri["resize"]
		rx = resize["x"]
		ry = resize["y"]
		rw = resize["width"]
		rh = resize["height"]
		res_f = parent / fn
		if res_f in arrays:
			arr = arrays[res_f].copy()
			arr_pr = cv2.resize(arr[rx:rw, ry:rh, :], (256,256))
			reg_id = ri["region_id"]
			new_f = str(parent) + res_f.stem + str(reg_id) + res_f.suffix
			cv2.imwrite(new_f, arr_pr)

def recourse_mapped_dirs(hier):
	for _, v in hier.items():
		if "head" in v and "tail" in v:
			for _, im_re in v.items():
				apply_region_info(im_re)
		elif "images" in v and "regions" in v:
			apply_region_info(v)

			
	