import cv2

class ImageWindow(object):
	def __init__(self, name: str):
		self.name = name

	def open(self):
		cv2.namedWindow(self.name)
	
	def __enter__(self):
		self.open()
		return self
	
	def destroy(self):
		cv2.destroyWindow(self.name)
	
	def __exit__(self, *args):
		self.destroy()
	
	def isOpen(self) -> bool:
		return cv2.getWindowProperty(self.name, 0) >= 0
	
	def move(self, x: int, y: int):
		cv2.moveWindow(self.name, x, y)
	
	def resize(self, width: int, height: int):
		cv2.resizeWindow(self.name, width, height)
	
	def show(self, frame):
		cv2.imshow(self.name, frame)
