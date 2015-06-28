# VP Workspace Window
# vectorClass tests

import os
import sys
import time
import random

# add the project directory for path so we can import
# files from the source directory
TOPDIR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(TOPDIR_PATH)

# import the vectorClass to run our tests
from source.vectorClass import Vector

def runFullTests(rigor = 100):
	startTime = time.time()

	def runCreationTests():
		random.shuffle(arbitraryElements)
		makeVector = Vector(arbitraryElements)
		assert(type(makeVector) == Vector)
		assert(makeVector.inSpace() == test)
		assert(makeVector == Vector(arbitraryElements))

	def runInteractionTests():
		random.shuffle(arbitraryElements)
		vec1 = Vector(arbitraryElements)
		random.shuffle(arbitraryElements)
		vec2 = Vector(arbitraryElements)
		assert(type(vec1*vec2) == int)
		assert(type(vec1+vec2) == Vector)
		assert(type(vec1-vec2) == Vector)
		if (test == 3):
			assert(type(vec1/vec2) == Vector)
			assert(vec1/vec2 == -1*(vec2/vec1))

	def runMethodTests():
		random.shuffle(arbitraryElements)
		makeVector = Vector(arbitraryElements)
		assert(makeVector.isDiscreteVector())
		assert(type(makeVector.unitVector()) == Vector)

	for test in xrange(rigor):
		arbitraryElements = range(test)
		runCreationTests()
		runInteractionTests()
		runMethodTests()

	return time.time() - startTime