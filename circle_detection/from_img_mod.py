#todo: figurue out method to dynamically adjust mindist, minrad, and accumThresh
#dp should probably just be at 2--if we cannot get any circles, then it's a bad image!
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
	#determined empirically to not matter much at all
	cannyParam = 50 #window.trackbar("cannyParam", 50, 200)
	accumThresh = window.trackbar("accuThresh", 60, 300)
	minRad = window.trackbar("minRad", 60, 150)
	minDist = window.trackbar("minDist", 120, 300)
	dp = window.trackbar("dp", 1, 4)

	#do the blur operations once instead of every frame
	origframe = cv2.imread(iname)
	#oframe = cv2.medianBlur(origframe, 17)
	oframe = cv2.pyrMeanShiftFiltering(origframe, 31, 61)
	oframe = cv2.GaussianBlur(oframe, (13, 13), 0)
	
	while window.isOpen():
		frame = oframe.copy()

		#frame = cv2.bilateralFilter(frame, 19, 2000, 100)
		#print(int(tbP1), int(tbP2))
		#findCircles = HoughCircleTransform(1, 40, param1=int(tbP1), param2=int(tbP2), minRadius=5, maxRadius=50)
		grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		#grayImg = cv2.adaptiveThreshold(grayImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 1)

		#below can be helpful to see what HoughCircles sees
		#frame = grayImg
		#frame = cv2.Canny(frame, 6, 3)
		#frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

		circles = cv2.HoughCircles(grayImg, cv2.HOUGH_GRADIENT, int(dp), int(minDist), param1=50, param2=int(accumThresh), minRadius=int(minRad), maxRadius=int(int(minRad)*2))

		if circles is not None:
			circles = np.uint16(np.around(circles))
			for x, y, rad in circles[0,:]:
				# draw the outer circle
				cv2.circle(frame, (x, y), rad, (0,255,0), 2)
				# draw the center of the circle
				cv2.circle(frame, (x, y), 2, (0,0,255), 3)
		else:
			print("no circ found")
		window.show(frame)
		if cv2.waitKey(1) == ord('q'):
			break
