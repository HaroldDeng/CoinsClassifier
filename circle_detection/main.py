import cv2
import numpy as np
from webcam import Webcam
from window import ImageWindow
from circle import HoughCircleTransform
from radsym import RadSymTransform

# create an overlay image. You can use any image
background = np.ones((100,100,3),dtype='uint8')*255
# Open the camera
with Webcam(0) as cap:
	# Set initial value of weights
	alpha = 0.4
	findCircles = HoughCircleTransform(1, 40, param1=50, param2=30, minRadius=0, maxRadius=50)
	radSym = RadSymTransform(100)
	print(findCircles)
	with ImageWindow('a') as window:
		alphaTB = window.trackbar('Alpha', 0, 100)
		while window.isOpen():
			# read the frame
			frame = next(cap)
			# Select the region in the frame where we want to add the image and add the images using cv2.addWeighted()
			alpha = float(alphaTB)
			added_image = cv2.addWeighted(frame[150:250,150:250,:],alpha,background[0:100,0:100,:],1-alpha,0)
			# Change the region with the result
			frame[150:250,150:250] = added_image
			# For displaying current value of alpha(weights)
			font = cv2.FONT_HERSHEY_SIMPLEX
			cv2.putText(frame,'alpha:{}'.format(alpha),(10,30), font, 1,(255,255,255),2,cv2.LINE_AA)

			# Try hough transform
			grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			circles = findCircles(grayImg)
			circles = np.uint16(np.around(circles))
			for x, y, rad in circles[0,:]:
				# draw the outer circle
				cv2.circle(frame, (x, y), rad, (0,255,0), 2)
				# draw the center of the circle
				cv2.circle(frame, (x, y), 2, (0,0,255), 3)
			
			# dx = cv2.Sobel(grayImg, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
			# dy = cv2.Sobel(grayImg, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
			# ax = cv2.convertScaleAbs(dx)
			# ay = cv2.convertScaleAbs(dy)
			# grad = cv2.addWeighted(ax, 0.5, ay, 0.5, 0)
			# frame = ay
			#frame = radSym(grayImg)
			window.show(frame)
			k = cv2.waitKey(10)
			# Press q to break
			if k == ord('q'):
				break
