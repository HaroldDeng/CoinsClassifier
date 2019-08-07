from cv2 import HoughCircles, HOUGH_GRADIENT

class HoughCircleTransform(object):
	def __init__(self, dp: int, minDist: int, param1: float, param2: float, minRadius: int = 0, maxRadius: int = 0):
		self.dp = dp
		self.minDist = minDist
		self.param1 = param1
		self.param2 = param2
		self.minRadius = minRadius
		self.maxRadius = maxRadius
	
	def __call__(self, frame):
		return HoughCircles(
			frame,
			HOUGH_GRADIENT,
			self.dp,
			self.minDist,
			param1=self.param1,
			param2=self.param2,
			minRadius=self.minRadius,
			maxRadius=self.maxRadius)
