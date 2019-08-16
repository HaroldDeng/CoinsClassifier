import cv2
import numpy as np
from typing import List, Tuple

def circle_mask(img, cx, cy, rad):
	roi = img[cy - rad:cy + rad, cx-rad:cx+rad]
	mask = np.zeros(roi.shape[:2], dtype=np.uint8)
	cv2.circle(mask, (rad, rad), rad, (255), -1)
	return cv2.bitwise_and(roi, roi, mask=mask)


def preprocess(rawframe):
	"""
	Preprocess frame

	Parameters
	----------
	rawframe: np.ndarray
		Source image, BGR encoded.
	Returns
	-------
	Gray image, preprocessed. Same dims as rawframe.
	"""
	oframe = cv2.pyrMeanShiftFiltering(rawframe, 17, 51)
	oframe = cv2.GaussianBlur(oframe, (13, 13), 0)
	grayImg = cv2.cvtColor(oframe, cv2.COLOR_BGR2GRAY)
	grayImg = cv2.threshold(grayImg, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	return grayImg


def preprocess_topo(rawframe):
	grayImg = cv2.cvtColor(rawframe, cv2.COLOR_BGR2GRAY)
	grayImg = cv2.adaptiveThreshold(grayImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)
	kernel = np.ones((3, 3), np.uint8)
	grayImg = cv2.morphologyEx(grayImg, cv2.MORPH_CLOSE, kernel, iterations=1)
	return grayImg


def find_circles(frame, dp: float = 2, minRad: int = 45, accumThresh: int = 60, verbose: bool = False) -> List[Tuple[int, int, int]]:
	smallestRad = 9999
	smallestRad_r = -1
	iter = 0
	if verbose:
		print(f"Shape={frame.shape}, dtype={frame.dtype}")
	while smallestRad_r != smallestRad:
		if verbose:
			print(f"\t-> Iteration {iter + 1} (smallest={smallestRad})")
		smallestRad_r = smallestRad
		circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, int(dp), int(smallestRad*2.1), param1=6, param2=int(accumThresh), minRadius=minRad, maxRadius=int(minRad*3.4))
		if circles is None:
			# Return empty array
			return np.zeros((0, 2), dtype=np.uint16)
		smallestRad = np.min(circles[0,:, 2])
		iter += 1
	return np.uint16(np.around(circles[0]))


def crop_circles(rawframe, callback, verbose=False):
	if verbose:
		print("Preprocessing...")
	processed = preprocess(rawframe)
	# processed = preprocess_topo(rawframe)
	if verbose:
		cv2.imwrite("preprocessed.jpg", processed)
		print("\t-> Done")
		print("Finding circles...")
	circles = find_circles(processed, verbose=verbose)
	
	if verbose:
		print(f"\t-> Found {len(circles)}")
	i = 0
	for x, y, r in circles:
		cropped = circle_mask(rawframe, x, y, r)
		callback(cropped, i=i, x=x, y=y, r=r)
		i += 1
