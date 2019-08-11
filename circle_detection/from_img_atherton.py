import cv2
import numpy as np
from window import ImageWindow
from circle import HoughCircleTransform
from sys import argv
from time import sleep
from chaccum import chaccum
from a_methods import IMCMethod

# create an overlay image. You can use any image
background = np.ones((100,100,3),dtype='uint8')*255
iname = argv[1]


def process(window, morphIters, rMin, rMax, alpha):
	frame = cv2.imread(iname)
	w0, h0 = frame.shape[:2]
	frame = cv2.resize(frame, (int(400 * h0 / w0), 400))
	frame = cv2.GaussianBlur(frame, (15, 15), 0)
	grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	grayImg = cv2.adaptiveThreshold(grayImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)
	kernel = np.ones((3, 3), np.uint8)
	if morphIters > 0:
		grayImg = cv2.morphologyEx(grayImg, cv2.MORPH_CLOSE, kernel, iterations=int(morphIters))
	
	accum, gradImg = chaccum(grayImg, rMin, rMax, method=IMCMethod.PHASE_LINEAR)

	hi = np.max(accum)
	lo = np.min(accum)
	accumImg = np.uint8(np.around((accum - lo) * 255 / (hi - lo)))
	accumImg = cv2.cvtColor(accumImg, cv2.COLOR_GRAY2BGR)
	cv2.imwrite('out.png', accumImg)
	accumImg[:,:,1] = 0
	accumImg[:,:,2] = 0
	frame = cv2.cvtColor(grayImg, cv2.COLOR_GRAY2BGR)
	frame[:,:,0] = 0
	frame = cv2.addWeighted(frame, alpha, accumImg, 1 - alpha, 0)


	window.show(frame)

# read the frame

with ImageWindow('a') as window:
	tbIter = window.trackbar('MItrs', 1, 10)
	minRadius = window.trackbar('rMin', 5, 100)
	maxRadius = window.trackbar('rMax', 50, 200)
	tbAlpha = window.trackbar('alpha', 40, 100)
	prev_args = None
	while window.isOpen():
		args = (int(tbIter), int(minRadius), int(maxRadius), float(tbAlpha))
		if args == prev_args:
			sleep(.1)
		else:
			process(window, *args)
			prev_args = args
		if cv2.waitKey(1) == ord('q'):
			break