# Graham Arthur
# Polynomial Class

# for implementation in 15-112 term project
# basically just an easy container for storing functions

import copy
import sympy as sym
from sympy import cos, sin, tan, cot, sec, csc, pi
from sympy.mpmath import *
from vectorClass import Vector

# graphics initialization
from Tkinter import *
import tkMessageBox

x, y, z = sym.symbols('x y z')

class PolynomialMultiVar(object):

	@staticmethod
	def flatten(someList):
		flat = []
		for item in someList:
			if(type(item)!=list and type(item)!=tuple):
				flat.append(item)
			else:
				flat.extend(Vector.flatten(item))
		return flat

	@staticmethod
	def differentiateWithRespect(function, variable):
		return sym.diff(function, variable)

	@staticmethod
	def fnGradient(function):
		variables, varNum = PolynomialMultiVar.listofVariables(function)
		partialDerivatives = [sym.diff(function, eval(var)) for var in variables]
		return Vector(partialDerivatives)

	@staticmethod
	def evalAt(function, *values):
		vals = PolynomialMultiVar.flatten(values)
		variables = [x,y,z] = sym.symbols('x y z')
		valsAndVars = zip(variables, vals)
		return function.subs(valsAndVars)

	@staticmethod
	def listofVariables(function):
		fnString = str(function)
		variables = [var for var in "xyz" if var in fnString]
		return variables, len(variables)

	@staticmethod
	def graphFunction(function):
		try:
			variables, varNum = PolynomialMultiVar.listofVariables(function)
			if(varNum == 1):
				trueFn = lambda x: eval(str(function))
				variable = variables[0]
				sym.mpmath.plot(trueFn, [-10, 10])
			elif (varNum == 2):
				if (variables == ["x", "y"]):
					trueFn = lambda x,y: eval(str(function))
				elif(variables == ["x", "z"]):
					trueFn = lambda x,z: eval(str(function))
				elif(variables == ["y", "z"]):
					trueFn = lambda y,z: eval(str(function))
				sym.mpmath.splot(trueFn, [-10, 10], [-10,10])
			else:
				tkMessageBox.showerror("Graphing Error",
					"Could not graph that polynomial.")
		except:
			tkMessageBox.showerror("Graphing Error",
				"Could not graph that polynomial.")

	@staticmethod
	def genBasicInfoString(function):
		variables, varNum = PolynomialMultiVar.listofVariables(function)
		fnString = "|f(%s) = %s|" %(",".join(variables), str(function))
		varString = "|Variables: %d|" %varNum
		infoText = fnString+"\n"+varString
		return infoText