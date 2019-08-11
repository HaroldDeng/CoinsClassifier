import cv2
import numpy as np
from window import ImageWindow
from circle import HoughCircleTransform
from sys import argv
from time import sleep
from frst import frst

# create an overlay image. You can use any image
background = np.ones((100,100,3),dtype='uint8')*255
iname = argv[1]


def process(window, radii, alpha, beta, tbIter, tra):
	frame = cv2.imread(iname)
	w0, h0 = frame.shape[:2]
	frame = cv2.resize(frame, (int(400 * h0 / w0), 400))
	frame = cv2.GaussianBlur(frame, (15, 15), 0)
	grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	grayImg = cv2.adaptiveThreshold(grayImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)
	kernel = np.ones((3, 3), np.uint8)
	if tbIter > 0:
		grayImg = cv2.morphologyEx(grayImg, cv2.MORPH_CLOSE, kernel, iterations=int(tbIter))
	
	grayImg = frst(grayImg, radii, alpha, beta, 0)
	print(np.min(grayImg), np.max(grayImg))
	hi = np.max(grayImg)
	lo = np.min(grayImg)
	grayImg = np.uint8(np.around((grayImg - lo) * 255 / (hi - lo)))
	grayImg = cv2.cvtColor(grayImg, cv2.COLOR_GRAY2BGR)
	# frame = frame[:grayImg.shape[0], :grayImg.shape[1], :]
	grayImg = grayImg[:frame.shape[0], :frame.shape[1]]
	print(frame.shape, grayImg.shape)
	frame = cv2.addWeighted(frame, tra, grayImg, 1 - tra, 0)

	window.show(frame)

# read the frame

with ImageWindow('a') as window:
	# tbP1 = window.trackbar('Param1', 50, 100)
	tbAlpha = window.trackbar('a', 1, 100)
	tbBeta = window.trackbar('b', 20, 100)
	tbRadii = window.trackbar('r', 18, 100)
	# tbIter = window.trackbar('MItrs', 1, 10)
	tbIter = 1
	alpha = window.trackbar('alpha',60, 100)
	prev_args = None
	while window.isOpen():
		args = (int(tbRadii), int(tbAlpha), float(tbBeta), int(tbIter), float(alpha))
		if args == prev_args:
			sleep(.1)
		else:
			process(window, *args)
			prev_args = args
		if cv2.waitKey(1) == ord('q'):
			break