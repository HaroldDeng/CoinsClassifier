from enum import Enum

class IMCMethod(Enum):
	TWO_STAGE = 'TwoStage'
	PHASE_LINEAR = 'PhaseCodingLinear'
	PHASE_RAMPED = 'PhaseCodingRamped'
	PHASE_LOG = 'PhaseCodingLog'
