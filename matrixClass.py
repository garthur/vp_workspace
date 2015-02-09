# Graham Arthur
# Matrix Class

# for implementation in 15-112 term project

import math
import copy
import numpy as np
import scipy as sp
from vectorClass import Vector

class Matrix(object):

	# a matrix is basically just a 2d list, but i need some
	# easy way of manipulating them , so object it is

	@staticmethod
	def is2dList(someList):
		# determines whether or not a list is a 2dlist
		# for use in init function
		if(type(someList) != list):
			return False
		for item in someList:
			if (type(item) != list):
				return False
		return True

	@staticmethod
	def isRagged(someList):
		# determines whether or not a list is ragged
		# for use in init function
		targetLength = len(someList[0])
		for item in someList:
			if(len(item) != targetLength):
				return False
		return True

	def __init__(self, elements):
		if (not Matrix.is2dList(elements) or Matrix.isRagged(elements)):
			raise Exception("That is not a valid Matrix.")
		else:
			self.elements = elements
			self.rows, self.cols = len(elements), len(elements[0])

	# some of the methods below require vector operations

	def __add__(self, other):
		pass

	def __radd__(self, other):
		pass

	def __mul__(self, other):
		# **VECTOR OPERATIONS**
		pass

	def __rmul__(self, other):
		# **VECTOR OPERATIONS**
		# not the same as mul
		pass

	def __div__(self, other):
		# well see what is going to happen with this one
		pass

	def __rdiv__(self, other):
		# well see what is going to happen with this one
		pass

	def transpose(self):
		pass

	def determinant(self):
		pass

	def getCofactorMatrix(self):
		pass

	def inverse(self):
		pass