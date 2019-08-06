import cv2
from typing import Optional, Union, Any, Iterable, Iterator, AsyncIterable, AsyncIterator, ContextManager


Frame = Any


class NoFrameException(Exception):
	pass


class WebcamProps(object):
	""" Wrapper for VideoCapture properties"""
	_ATTR_LUT = {
		'width': cv2.CAP_PROP_FRAME_WIDTH,
		'height': cv2.CAP_PROP_FRAME_HEIGHT,
		'fps': cv2.CAP_PROP_FPS}
	_cam: 'Webcam'
	# Delegated to camera
	width: int
	height: int
	fps: float

	def __init__(self, cam: 'Webcam'):
		self._cam = cam

	def __getitem__(self, key: int):
		return self.cam._getProp(key)
	
	def __setitem__(self, key: int, value: Any):
		return self.cam._setProp(key)
	
	# Property delegation
	def __getattr__(self, name: str):
		return self[WebcamProps._ATTR_LUT[name]]
	
	def __setattr__(self, name: str, value: Any):
		if name.startswith('_'):
			self.__dict__[name] = value
		else:
			self[WebcamProps._ATTR_LUT[name]] = value


class WebcamGrab(object):
	def __init__(self, cam: 'Webcam', capture: int):
		self._cam = cam
		self._capture = capture
	
	def retrieve(self, frame: Optional[Frame] = None, channel: Optional[int] = None) -> Frame:
		return self._cam._retrieve(self._capture, frame, channel)


class Webcam(Iterable[Frame]):
	"""
	Pretty wrapper for OpenCV's VideoCapture.
	Provides ContextManager & iterator functionality.
	"""

	def __init__(self, arg: Optional[Union[str, int]] = None):
		self.device = cv2.VideoCapture(arg)
		self.props = WebcamProps(self)
	
	def isOpened(self) -> bool:
		return self.device.isOpened()
	
	def release(self):
		self.device.release()
	
	def _getProp(self, key: int) -> Any:
		return self.device.get(key)
	
	def _setProp(self, key: int, value: Any):
		self.device.set(key, value)
	
	# Context manager
	def __enter__(self):
		return self
	
	def __exit__(self, *args):
		self.release()
	
	def grab(self) -> WebcamGrab:
		""" Grab a frame."""
		capture = self.device.grab()
		return WebcamGrab(self, capture)
	
	def _retrieve(self, frame: Optional[Frame] = None, channel: Optional[int] = None) -> Frame:
		return self.device.retrieve(frame, channel)
	
	def read(self, image: Optional[Frame] = None) -> Frame:
		""" Grab & decode frame"""
		retval, frame = self.device.read(image)
		if not retval:
			raise NoFrameException()
		return frame
	
	async def readAsync(self, image: Optional[Frame] = None) -> Frame:
		return self.read()
	
	# Iterator
	def __iter__(self):
		return self
	
	def __next__(self) -> Frame:
		"""Get next frame"""
		try:
			return self.read()
		except NoFrameException:
			raise StopIteration()

	def __aiter__(self):
		return self
	
	async def __anext__(self) -> Frame:
		try:
			frame = self.read()
		except NoFrameException:
			raise StopAsyncIteration()
		else:
			yield frame