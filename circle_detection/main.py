import cv2
import numpy as np
from webcam import Webcam
from window import ImageWindow

# create an overlay image. You can use any image
background = np.ones((100,100,3),dtype='uint8')*255
cv2.namedWindow('a')
# Open the camera
with Webcam(0) as cap:
	# Set initial value of weights
	alpha = 0.4
	with ImageWindow('a') as window:
		while window.isOpen():
			# read the frame
			frame = next(cap)
			# Select the region in the frame where we want to add the image and add the images using cv2.addWeighted()
			added_image = cv2.addWeighted(frame[150:250,150:250,:],alpha,background[0:100,0:100,:],1-alpha,0)
			# Change the region with the result
			frame[150:250,150:250] = added_image
			# For displaying current value of alpha(weights)
			font = cv2.FONT_HERSHEY_SIMPLEX
			cv2.putText(frame,'alpha:{}'.format(alpha),(10,30), font, 1,(255,255,255),2,cv2.LINE_AA)
			grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			grayImg = cv2.Canny(grayImg, 32, 2)
			window.show(grayImg)
			k = cv2.waitKey(10)
			# Press q to break
			if k == ord('q'):
				break
			# press a to increase alpha by 0.1
			if k == ord('a'):
				alpha +=0.1
				if alpha >=1.0:
					alpha = 1.0
			# press d to decrease alpha by 0.1
			elif k== ord('d'):
				alpha -= 0.1
				if alpha <=0.0:
					alpha = 0.0
