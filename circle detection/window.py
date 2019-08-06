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
	
	def trackbar(self, name: str, value: int, count: int) -> 'Trackbar':
		return Trackbar(name, self.name, value, count)


class Trackbar(object):
	def __init__(self, name: str, winname: str, value: int, count: int):
		self.name = name
		self.winname = winname
		self.count = count
		cv2.createTrackbar(name, winname, value, count, self._onUpdate)
	
	def _onUpdate(self, value: int):
		print(f"Trackbar {self.name} updated to {value}")
	
	@property
	def value(self) -> int:
		return cv2.getTrackbarPos(self.name, self.winname)
	
	@value.setter
	def value(self, val: int):
		cv2.setTrackbarMax(self.name, self.winname, val)

	def __int__(self) -> int:
		return self.value
	
	def __float__(self) -> float:
		return float(self.value) / self.count
