import numpy as np
import cv2
import warnings
from typing import Tuple
from collections import namedtuple

from chaccum import chaccum
from a_methods import IMCMethod


Circle = namedtuple('x', 'y', 'radius', 'metric')

def imfindcircles(
		image,
		rMin: int,
		rMax: int,
		polarity: str='bright',
		method: IMCMethod = IMCMethod.PHASE_LOG,
		sensitivity=0.85,
		edgeThreshold=None
	) -> Tuple[Circle]:
	"""
	Finds circles.
	Parameters
	----------
	rMin: int
		Minimum radius
	rMax: int
		Maximum radius
	polarity: 'bright' | 'dark' = 'bright'
	method: 'PhaseCode' | 'TwoStage' = 'PhaseCode'
		Method to compute the accumulator with
	
	Returns
	-------
	Tuple of circle data
	"""
	if (rMax > 3 * rMin) or (rMax - rMin > 100):
		warnings.warn('rMax is much bigger than rMin')
	if rMin < 5:
		warnings.warn('rMin is pretty small')
	
	accum, gradImg = chaccum(image, rMin, rMax, method=method, polarity=polarity, edgeThreshold=edgeThreshold)
	
	# Test if accumulator is all zeroed
	if not np.any(accum):
		return tuple()
	
	# Estimate the centers
	accumThresh = 1 - sensitivity
	centers, metric = chcenters(accum, accumThresh)
	if len(centers) == 0:
		# No centers found
		return tuple()
		
	


# See github.com/pnlbwh/SignalDropQCTool/blob/master/imageToolBoxPrivateFunctions/chaccum.m
class AthertonCircleTransform(object):
	def __init__(self, minRadius: int, maxRadius: int, polarity: str, edgeThreshold: float):
		self.minRadius = minRadius
		self.maxRadius = maxRadius
		self.polarity = polarity
		self.edgeThreshold = edgeThreshold
	
	def __call__(self, image):
		pass
