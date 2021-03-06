import cv2
import numpy as np
from window import ImageWindow
from circle import HoughCircleTransform
from sys import argv
from time import sleep

# create an overlay image. You can use any image
background = np.ones((100,100,3),dtype='uint8')*255
iname = argv[1]


def process(window, tbP1, tbP2, tbIter, minRadius, maxRadius):
	frame = cv2.imread(iname)
	w0, h0 = frame.shape[:2]
	frame = cv2.resize(frame, (int(400 * h0 / w0), 400))
	frame = cv2.GaussianBlur(frame, (15, 15), 0)
	print(int(tbP1), int(tbP2))
	findCircles = HoughCircleTransform(2.2, int(maxRadius) * 2, param1=int(tbP1), param2=int(tbP2), minRadius=int(minRadius), maxRadius=int(maxRadius))
	grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	grayImg = cv2.adaptiveThreshold(grayImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)
	kernel = np.ones((3, 3), np.uint8)
	if tbIter > 0:
		grayImg = cv2.morphologyEx(grayImg, cv2.MORPH_CLOSE, kernel, iterations=int(tbIter))

	frame = grayImg
	# frame = cv2.Canny(frame, int(tbP1), int(tbP1) // 2)
	frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

	cv2.imwrite('out.jpg', frame)

	circles = findCircles(grayImg)
	print(circles)
	if circles is not None:
		circles = np.uint16(np.around(circles))
		for x, y, rad in circles[0,:]:
			# draw the outer circle
			cv2.circle(frame, (x, y), rad, (0,255,0), 2)
			# draw the center of the circle
			cv2.circle(frame, (x, y), 2, (0,0,255), 3)
	window.show(frame)

# read the frame

with ImageWindow('a') as window:
	# tbP1 = window.trackbar('Param1', 50, 100)
	tbP1 = 50
	tbP2 = 25#window.trackbar('Param2', 35, 100)
	tbIter = window.trackbar('MItrs', 1, 10)
	minRadius = window.trackbar('min', 5, 100)
	maxRadius = window.trackbar('max', 50, 200)
	prev_args = None
	while window.isOpen():
		args = (int(tbP1), int(tbP2), int(tbIter), int(minRadius), int(maxRadius))
		if args == prev_args:
			sleep(.1)
		else:
			process(window, *args)
			prev_args = args
		if cv2.waitKey(1) == ord('q'):
			break