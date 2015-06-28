# Graham Arthur
# Vector Class

import copy
import sympy as sym
from sympy import cos, sin, tan, cot, sec, csc, pi
from sympy.mpmath import *
from sympy.parsing.sympy_parser import parse_expr

[x,y,z] = sym.symbols('x y z')

class Vector(object):

	@staticmethod
	def isLegalInput(item):
		# for use in vector construction
		return type(item) != str

	@staticmethod
	def flatten(someList):
		# some cleanup to be done here
		flat = []
		for item in someList:
			if(type(item)!=list and type(item)!=tuple):
				flat.append(item)
			else:
				flat.extend(Vector.flatten(item))
		return flat

	def __init__(self, elems, *args):
		# construct a vector from a list of elements
		# or a set of arguments
		if (Vector.isLegalInput(elems)):
			constructElements = [elems]
			for item in args:
				# change this to allow for polynomials in the vector
				if(not Vector.isLegalInput(item)):
					raise Exception("That cannot be placed in a vector.")
				constructElements.append(item)
		elif (isinstance(elems, list) or isinstance(elems, tuple)):
			constructElements = list(elems)
		else:
			raise Exception("""There has been an error in the creation 
				of this vector.""")
		self.elements = copy.deepcopy(Vector.flatten(constructElements))
		self.variables = [x, y, z] = sym.symbols("x y z")

	def inSpace(self):
		# determines the space in which the vector exists
		return len(self.elements)

	@staticmethod
	def inSameSpace(v1, v2):
		# determines whether or not two vectors are in the same space
		return (v1.inSpace() == v2.inSpace())

	def isDiscreteVector(self):
		for item in self.elements:
			if((type(item) != int) and (type(item) != float)):
				return False
		return True

	def findLength(self):
		rawNum = 0
		for item in self.elements:
			rawNum += (item**2)
		return sym.sqrt(rawNum)

	def __str__(self):
		elementText = [str(item) for item in self.elements]
		return "< %s >" % (", ".join(elementText))

	def __eq__(self, other):
		if (type(other) != type(self)):
			return False
		else:
			if (not Vector.inSameSpace(self, other)):
				return False
			else:
				for i in xrange(len(self.elements)):
					if (self.elements[i] != other.elements[i]):
						return False
		return True

	def __ne__(self, other):
		return (not self==other)

	def __add__(self, other):
		if(isinstance(other, Vector) and Vector.inSameSpace(self, other)):
			newElements = copy.deepcopy(self.elements)
			for i in xrange(len(newElements)):
				newElements[i] = newElements[i] + other.elements[i]
				newElements[i] = sym.simplify(newElements[i])
			return Vector(newElements)
		else:
			raise Exception("That cannot be added to this vector.")

	def __radd__(self, other):
		return self+other

	def __sub__(self, other):
		if(isinstance(other, Vector) and Vector.inSameSpace(self, other)):
			newElements = copy.deepcopy(self.elements)
			for i in xrange(len(newElements)):
				newElements[i] = newElements[i] - other.elements[i]
				newElements[i] = sym.simplify(newElements[i])
			return Vector(newElements)
		else:
			raise Exception("That cannot be subtracted from this vector.")

	def __rsub__(self, other):
		return -(self) + other

	def __mul__(self, other):
		if (not isinstance(other, Vector)):
			newElements = copy.deepcopy(self.elements)
			for i in xrange(len(newElements)):
				newElements[i] = newElements[i]*(other)
				newElements[i] = sym.simplify(newElements[i])
			return Vector(newElements)
		elif (isinstance(other, Vector)):
			# this body of code performs a dot product operation
			# on two vectors
			total = 0
			if (Vector.inSameSpace(self, other)):
				for i in xrange(len(self.elements)):
					total += (self.elements[i]*other.elements[i])
			else:
				raise Exception("""You cannot take the dot product of two 
					vectors not in the same space""")
			return total

	def __rmul__(self, other):
		# dot product is commutative and so is other vector multiplication
		return self*other

	@staticmethod
	def arePerpendicular(v1, v2):
		return (v1*v2 == 0)

	@staticmethod
	def angleBetween(v1, v2):
		# uses definition of dot product to find the angle between two
		# vectors
		dotProd = v1*v2
		len1 = v1.findLength()
		len2 = v2.findLength()
		# perhaps implement degree/radian versions of the angle?
		angle = sym.acos(dotProd/(len1*len2))
		return angle

	def __div__(self, other):
		if(not isinstance(other, Vector)):
			newElements = copy.deepcopy(self.elements)
			for i in xrange(len(newElements)):
				newElements[i] = newElements[i]/(other)
				newElements[i] = sym.simplify(newElements[i])
			return Vector(newElements)
		elif(isinstance(other, Vector)):
			# cross product operation without matrix
			# for simplification, only available for R3 vectors
			assert(self.inSpace() == 3)
			assert(other.inSpace() == 3)
			elems1 = self.elements
			elems2 = other.elements
			newElements = [(elems1[1]*elems2[2]-elems1[2]*elems2[1]), 
				-(elems1[0]*elems2[2]-elems1[2]*elems2[0]), 
					(elems1[0]*elems2[1]-elems1[1]*elems2[0])]
			return Vector(newElements)

	def __rdiv__(self, other):
		if(not isinstance(other, Vector)):
			return (self)/(other)
		elif(isinstance(other, Vector)):
			# taking a cross product is not commutative, so it is a different operation
			# the other way around
			return -(self/other)

	def unitVector(self):
		length = self.findLength()
		return self/length

	def __repr__(self):
		elementText = [str(item) for item in self.elements]
		return "Vector(%s)" %(", ".join(elementText))

	def __hash__(self):
		return hash(str(self))

	def genBasicInfoString(self):
		# this generates an information string with all the basic
		vectorDesc = " |Vector: %s| " %str(self)
		inSpaceText  = " |Exists In: R%d| " %self.inSpace()
		magnitudeText = " |Magnitude: %s| " %str(self.findLength())
		discreteText = " |Discrete Vector: %s| " %str(self.isDiscreteVector())
		infoText = vectorDesc+inSpaceText+"\n"+magnitudeText+discreteText
		return infoText

	def evalAt(self, *values):
		vals = Vector.flatten(values)
		valsAndVars = zip(self.variables, vals)
		evalElems = []
		for item in self.elements:
			try:
				evalElems.append(item.subs(valsAndVars))
			except: evalElems.append(item)
		evalElems = Vector.flatten(evalElems)
		return Vector(evalElems)
