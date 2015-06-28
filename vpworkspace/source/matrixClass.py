# Graham Arthur
# Matrix Class

# for implementation in 15-112 term project

import math
import copy
import numpy as np
import sympy as sym
from sympy import cos, sin, tan, cot, sec, csc, pi
from sympy.mpmath import *

[x,y,z] = sym.symbols('x y z')

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
		newElements = [ ]
		if (isinstance(other, Matrix)):
			assert(self.cols == other.rows)
		elif (isinstance(other, Vector)):
			assert(self.cols == len(other.elements))
		else:
			for row in self.rows:
				rowElems = []
				for col in self.cols:
					newElem = self.elements[row][col]*other
					rowElems.append(newElem)
				newElements.append(rowElems)
			return Matrix(newElements)

	def __rmul__(self, other):
		# not the same as mul
		if (isinstance(other, Matrix)):
			pass
		elif(isinstance(other, Vector)):
			pass
		else:
			return self*other

	def transpose(self):
		pass

	def determinant(self):
		pass

	def getCofactorMatrix(self):
		pass

	def inverse(self):
		pass