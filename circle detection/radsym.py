import math
import numpy as np
import cv2
import time

class RadSymTransform(object):
	def __init__(self, ray: int, minval: float = 0, maxval: float = 255):
		self.ray = ray
		self.minval = minval
		self.maxval = maxval
	
	def __call__(self, image):
		dx = cv2.Sobel(image, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
		dy = cv2.Sobel(image, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
		d = np.stack((dx, dy), axis=-1, out=np.empty((dx.shape[0], dx.shape[1], 2), dtype=np.float32))
		result = np.zeros(image.shape, np.uint16)
		mags = np.linalg.norm(d, axis=-1)
		inter = np.logical_and(self.minval < mags, mags < self.maxval)
		rows, cols = image.shape[:2]
		last = -1
		t0 = time.time()
		stime = time.time()
		for y in range(rows):
			p = int(y / rows * 100)
			if p != last:
				print(f"{p}% ({(time.time() - stime)*1000:.3f}ms)")
				last = p
				stime = time.time()
			for x in range(cols):
				if inter[y, x]:
					gx = float(dx[y, x])
					gy = float(dy[y, x])
					gMax = max(abs(gx), abs(gy))
					gx /= gMax
					gy /= gMax
					tx = int(x - self.ray * gx)
					ty = int(y - self.ray * gy)
					if (tx < 0) or (cols <= tx) or (ty < 0) or (rows <= ty):
						continue
					# print((y - gy, x - gx), (ty, tx), result.shape)
					idxsY = np.linspace(y - gy, ty, self.ray, endpoint=False, dtype=int)
					idxsX = np.linspace(x - gx, tx, self.ray, endpoint=False, dtype=int)
					result[idxsY, idxsX] += 1
		print(f"Timing for {self.ray}: {time.time() - t0}s")
		return result

