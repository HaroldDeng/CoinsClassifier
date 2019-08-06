import cv2

class NoFrameException(Exception):
	pass


class Webcam(object):
	def __init__(self, arg):
		self.device = cv2.VideoCapture(arg)
	
	def isOpened(self) -> bool:
		return self.device.isOpened()
	
	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.device.release()
	
	def read(self, image=None):
		retval, frame = self.device.read(image)
		if not retval:
			raise NoFrameException()
		return frame
	
	def __next__(self):
		try:
			return self.read()
		except NoFrameException:
			raise StopIteration()
	
	def __iter__(self):
		return self
