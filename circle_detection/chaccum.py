import cv2
import numpy as np
import numpy.matlib as npm
from math import pi
from a_methods import IMCMethod
from skimage.filters import threshold_otsu

# References:
# Atherton & Kerbyson: citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.24.3310&rep=rep1&type=pdf
# ER Davies: doc.lagout.org/science/0_Computer%20Science/2_Algorithms/Computer%20and%20Machine%20Vision_%20Theory%2C%20Algorithms%2C%20Practicalities%20%284th%20ed.%29%20%5BDavies%202012-03-19%5D.pdf



TWO_PI = 2 * pi


def rFilter(r: float, rMin: int, rMax: int, method: IMCMethod) -> complex:
	if method == IMCMethod.TWO_STAGE:
		# Circumference normalization (Inverse circumference weighting)
		return r / TWO_PI
	
	# Some kind of phase coding
	if method == IMCMethod.PHASE_LINEAR:
		phi = (r - rMin) / (rMax - rMin)
	elif method == IMCMethod.PHASE_RAMPED:
		rRatio = rMin / rMax
		rRange = rMax - rMin
		rDelta = r - rMin
		phi = (rDelta / rRange) * (rRatio + ((1 - rRatio) * rDelta) / rRange)
	elif method == IMCMethod.PHASE_LOG:
		logrMin = np.log(rMin, dtype=complex)
		logrMax = np.log(rMax, dtype=complex)
		# MatLab tweak: - PI
		# Default: phi = (np.log(r) - logrMin) / (logrMax - logrMin)
		phi = TWO_PI - (np.log(r) - logrMin) / (logrMax - logrMin) - np.pi
	else:
		raise "Unknown method"

	return np.exp(TWO_PI * 1j * phi)


def genFilter(rMin: int, rMax: int, rRange, method: IMCMethod):
	#TODO: more efficient computation here (numpy primitives)
	return np.apply_along_axis(lambda r: rFilter(r, rMin, rMax, method), 0, rRange)

def chaccum_native(edges, gx, gy, gradImg, rMin, rMax, RR, w0):
	ey, ex = np.nonzero(edges)

	gxN = gx[ey, ex]
	gyN = gy[ey, ex]
	gradN = gradImg[ey, ex]

	numIndices = ex.shape[0]
	rads = np.broadcast_to(-RR, (numIndices, RR.shape[0]))

	def broadcast2(arr, dim2):
		return np.broadcast_to(arr.reshape(-1, 1), (arr.shape[0], dim2))

	xc = np.rint(broadcast2(ex, RR.shape[0]) + broadcast2(gxN / gradN, RR.shape[0]) * rads).astype(int)
	yc = np.rint(broadcast2(ey, RR.shape[0]) + broadcast2(gyN / gradN, RR.shape[0]) * rads).astype(int)

	inside = np.logical_and(np.logical_and(0 <= xc, xc < cols), np.logical_and(0 <= yc, yc < rows))
	# rows_to_keep = np.any(inside, axis=1)
	# xc = xc[rows_to_keep, :]
	# yc = yc[rows_to_keep, :]
	# inside = inside[rows_to_keep]
	w = npm.repmat(w0, xc.shape[0], 1)

	xc = xc[inside]
	yc = yc[inside]
	w = w[inside]

	idxs = np.ravel_multi_index((yc, xc), (rows, cols), mode='clip')
	wRe = np.real(w)
	accumRe = np.bincount(idxs, wRe.reshape(-1), minlength=(rows * cols)).reshape(rows, cols)
	wIm = np.imag(w)
	accumIm = np.bincount(idxs, wIm.reshape(-1), minlength=(rows * cols)).reshape(rows, cols)
	accum = np.hypot(accumRe, accumIm)
	return accum
	

def chaccum(
		image,
		rMin: int,
		rMax: int,
		method: IMCMethod = IMCMethod.PHASE_LOG,
		polarity: str = 'bright',
		edgeThreshold=None):
	""" Circular Hough Transform accumulator"""
	rows, cols = image.shape[:2]
	gx = cv2.Sobel(image, cv2.CV_16S, 1, 0, scale=1, delta=0, borderType=cv2.BORDER_REPLICATE)
	gy = cv2.Sobel(image, cv2.CV_16S, 0, 1, scale=1, delta=0, borderType=cv2.BORDER_REPLICATE)
	gradImg = np.hypot(gx, gy)
	edges = getEdgePixels(gradImg, edgeThreshold)
	ey, ex = np.nonzero(edges)
	# idxE = np.ravel_multi_index((ex, ey), (rows, cols))

	radiusRange = np.arange(rMin, rMax, 0.5, dtype=float)
	if polarity == 'bright':
		RR = radiusRange
	elif polarity == 'dark':
		RR = -radiusRange
	else:
		raise "Invalid polarity"

	
	w0 = genFilter(rMin, rMax, radiusRange, method)

	gxN = gx[ey, ex]
	gyN = gy[ey, ex]
	gradN = gradImg[ey, ex]
	numIndices = ex.shape[0]
	rads = np.broadcast_to(-RR, (numIndices, RR.shape[0]))

	accum = chaccum_native(edges, gx, gy, gradImg, rMin, rMax, RR, w0)

	return accum, gradImg


def getEdgePixels(gradImg, edgeThreshold):
	gMax = np.max(gradImg)
	if (edgeThreshold is None) or (len(edgeThreshold) == 0):
		edgeThreshold = threshold_otsu(gradImg / gMax)
	else:
		edgeThreshold = float(edgeThreshold)
	
	t = gMax * edgeThreshold
	return (gradImg > t)