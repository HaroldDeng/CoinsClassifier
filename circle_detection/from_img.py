import cv2
import numpy as np
from window import ImageWindow
from circle import HoughCircleTransform
from sys import argv

# create an overlay image. You can use any image
background = np.ones((100,100,3),dtype='uint8')*255
iname = argv[1]


# read the frame

with ImageWindow('a') as window:
	# tbP1 = window.trackbar('Param1', 50, 100)
	tbP1 = 50
	tbP2 = 25#window.trackbar('Param2', 35, 100)
	tbIter = 2# window.trackbar('MItrs', 4, 10)
	while window.isOpen():
		frame = cv2.imread(iname)
		frame = cv2.GaussianBlur(frame, (15, 15), 0)
		print(int(tbP1), int(tbP2))
		findCircles = HoughCircleTransform(1, 40, param1=int(tbP1), param2=int(tbP2), minRadius=5, maxRadius=50)
		grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		grayImg = cv2.adaptiveThreshold(grayImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)
		kernel = np.ones((3, 3), np.uint8)
		grayImg = cv2.morphologyEx(grayImg, cv2.MORPH_CLOSE, kernel, iterations=int(tbIter))

		frame = grayImg
		# frame = cv2.Canny(frame, int(tbP1), int(tbP1) // 2)
		frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

		circles = findCircles(grayImg)
		if circles is not None:
			circles = np.uint16(np.around(circles))
			for x, y, rad in circles[0,:]:
				# draw the outer circle
				cv2.circle(frame, (x, y), rad, (0,255,0), 2)
				# draw the center of the circle
				cv2.circle(frame, (x, y), 2, (0,0,255), 3)
		window.show(frame)
		if cv2.waitKey(1) == ord('q'):
			break