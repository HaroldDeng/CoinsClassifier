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
outputSubdir = "./output/"
outCropSubdir = "./output"


# read the frame

with ImageWindow('a') as window:
	accumThresh = 60#window.trackbar("accuThresh", 60, 300)
	minRad = 45#window.trackbar("minRad", 60, 150)
	#minDist = window.trackbar("minDist", 120, 300)
	dp = 2#window.trackbar("dp", 2, 4)

	#do the blur operations once instead of every frame
	origframe = cv2.imread(iname)
	#oframe = cv2.medianBlur(origframe, 17)
	oframe = cv2.pyrMeanShiftFiltering(origframe, 17, 51)
	oframe = cv2.GaussianBlur(oframe, (13, 13), 0)

	#parameter fitting
	smallestRad = 9999
	smallestRad_d = smallestRad
	smallestCt = 0

	while window.isOpen():
		frame = oframe.copy()
		rawframe = origframe.copy()
		drawframe = origframe.copy()
		print(smallestRad)

		grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		grayImg = cv2.threshold(grayImg, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

		#below can be helpful to see what HoughCircles sees
		#frame = grayImg
		#frame = cv2.Canny(frame, 6, 3)
		#frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

		circles = cv2.HoughCircles(grayImg, cv2.HOUGH_GRADIENT, int(dp), int(smallestRad*2.1), param1=6, param2=int(accumThresh), minRadius=minRad, maxRadius=int(minRad*3.4))

		if circles is not None:
			circles = np.uint16(np.around(circles))
			for x, y, rad in circles[0,:]:
				# draw the outer circle
				cv2.circle(drawframe, (x, y), rad, (0,255,0), 5)
				# draw the center of the circle
				cv2.circle(drawframe, (x, y), 2, (0,0,255), 6)
				if rad < smallestRad:
					smallestRad = rad

			if smallestCt == 5:
				cv2.imwrite("output/"+iname, img=drawframe)

				ct = 0
				#save each image
				for x, y, rad in circles[0,:]:
					roi = rawframe[y-rad:y+rad, x-rad:x+rad].copy()
					cv2.imwrite("crop_" + str(ct) + ".jpg", roi)
					ct = ct + 1
				break

		else:
			print("no circ found")

		if smallestRad_d != smallestRad:
			smallestRad_d = smallestRad
			smallestCt = 0
		else:
			smallestCt = smallestCt + 1

		window.show(drawframe)
		if cv2.waitKey(1) == ord('q'):
			cv2.imwrite("output/FAIL_"+iname, img=drawframe)
			break
