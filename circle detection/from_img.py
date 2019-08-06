import cv2
import numpy as np
from window import ImageWindow
from radsym import RadSymTransform
from sys import argv

# create an overlay image. You can use any image
background = np.ones((100,100,3),dtype='uint8')*255
iname = argv[1]


# read the frame
frame = cv2.imread(iname)
for i in range(10, 110, 10):
	radSym = RadSymTransform(i)

	grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	frame = radSym(grayImg)
	frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
	cv2.imwrite(f'out_{i}.jpg', frame)