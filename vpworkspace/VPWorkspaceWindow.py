# Graham Arthur
# VP Workspace

import os
import sys
import copy
import time
import threading

# modules for function eval
import sympy as sym
## some special functions need to be imported for eval purposes
from sympy import cos, acos, sin, asin, tan, atan, cot, sec, csc, pi, ln, log, sqrt

# self-written modules for manipulations
from source.vectorClass import *
from source.polynomialClass import *

# import graphics modules
from Tkinter import *
from graphics.eventBasedAnimationClass import EventBasedAnimationClass
import tkMessageBox, tkFileDialog

x, y, z = sym.symbols('x y z')

def readFile(filename, mode="rt"):
	# this function is taken from the CMU 15-112 course notes
    # rt = "read text"
    with open(filename, mode) as fin:
        return fin.read()

def writeFile(filename, contents, mode="wt"):
	# this function is taken from the CMU 15-112 course notes
    # wt = "write text"
    with open(filename, mode) as fout:
        fout.write(contents)

def replaceFunctionSymbolsWithUnicode(s):
	# replaces some basic symbols with unicode symbols
	# needs to be expanded...
	mulAndPow = s.replace("**","^").replace("*",u"\u2219")
	mulAndPowAndDiv = mulAndPow.replace("pi",u"\u03C0").replace("sqrt",u"\u221A")
	return mulAndPowAndDiv

class WorkspaceObject(object):

	def __init__(self, posX, posY, containedObject):
		self.object = containedObject
		self.posX, self.posY = posX, posY
		self.height = 10*(len(str(containedObject).splitlines()))
		self.width = (len(str(containedObject))*7)/2.0 

	# these methods deal with how the object is displayed on screen
	def draw(self, canvas):
		drawText = replaceFunctionSymbolsWithUnicode(str(self.object))
		canvas.create_text(self.posX, self.posY, text=drawText,
			font="Arial 10 bold", fill="black")

	def highlight(self, canvas, color='black'):
		canvas.create_rectangle(self.posX-self.width, self.posY-self.height, 
			self.posX+self.width, self.posY+self.height, outline=color)

	def labelOrder(self, canvas, position):
		canvas.create_text(self.posX+self.width, self.posY-self.height,
			anchor='ne', fill='blue', text=str(position), font="Arial 7")

	def move(self, newX, newY):
		self.posX, self.posY = newX, newY

	def isSelected(self, mouseX, mouseY):
		return all([self.posX-self.width<mouseX<self.posX+self.width, 
			self.posY-self.height<mouseY<self.posY+self.height])

	def inner(self):
		# this method simply returns the inner object without
		# any x or y position
		return self.object

	def __repr__(self):
		return "WorkspaceObject(%d,%d,%s)" %(self.posX, self.posY,
			repr(self.inner()))

class Workspace(object):

	def __init__(self, objects=[]):
		self.objects = objects
		self.workingObjects = []
		self.operationText = ""
		self.activeItem = None

	def drawWorkspace(self, canvas, x0, y0, x1, y1, mouseX, mouseY):
		canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="white")
		for item in self.objects:
			try: 
				item.draw(canvas)
			except:
				pass
		for i in xrange(len(self.workingObjects)):
				self.workingObjects[i].highlight(canvas, 'blue')
				self.workingObjects[i].labelOrder(canvas, i+1)
		if (self.activeItem != None):
			self.activeItem.highlight(canvas)

	def checkForActive(self, posX, posY):
		for item in self.objects:
			if item.isSelected(posX, posY):
				self.activeItem = item
				return
		self.activeItem = None

	def objectSelected(self):
		return self.activeItem != None

	def moveObject(self, newX, newY):
		if (self.activeItem != None):
			self.activeItem.move(newX, newY)

	def selectObject(self, posX, posY):
		if(not self.objectSelected()):
			self.workingObjects = []
			self.operationText = ""
		else:
			for item in self.objects:
				if (item.isSelected(posX,posY) and 
					item not in self.workingObjects):
					self.workingObjects.append(item)

	def deselectLastObject(self):
		if (self.workingObjects != []):
			self.workingObjects.pop()

	def deleteLastObject(self):
		if (self.objects != []):
			self.objects.pop()

	def deleteSelectedObject(self, posX, posY):
		for i in xrange(len(self.objects)):
			if(self.objects[i].isSelected(posX, posY)):
				self.objects.pop(i)
				break

	def addToWorkspace(self, objectToBeAdded):
		self.objects.append(objectToBeAdded)

	def clearWorkspace(self):
		self.objects = []
		self.workingObjects = []

	def performOperation(self, operation, returnX, returnY):
		# get the 'inner' objects, operate on them , and then create a
		# new workspace object and add it to the workspace
		workingObjects = copy.deepcopy(self.workingObjects)
		innerObjects = [item.inner() for item in workingObjects]
		innerObjectsStrings = [str(item) for item in innerObjects]
		self.operationText = (" "+operation+" ").join(innerObjectsStrings)
		try:
			primeItem = innerObjects[0]
			for i in xrange(1, len(innerObjects)):
				if(operation == '*'):
					(primeItem) *= (innerObjects[i])
				elif(operation == '/'):
					(primeItem) /= (innerObjects[i])
				elif(operation == '+'):
					(primeItem) += (innerObjects[i])
				elif(operation == '-'):
					(primeItem) -= (innerObjects[i])
			if (type(primeItem)!= Vector and type(primeItem)!=Matrix):
				primeItem = sym.simplify(primeItem)
			self.addToWorkspace(WorkspaceObject(returnX, returnY, primeItem))
		except:
			raise Exception("That operation could not be performed.")

##############
#DIALOG BOXES#
##############

class VectorCreationDialog(object):

	def __init__(self, parent, Workspace, posX, posY):
		top = self.top = Toplevel(parent)
		self.Workspace = Workspace
		self.posX, self.posY = posX, posY
		Label(top, text="Vector Creation").pack()
		# initialize entry fields and button
		self.e1 = Entry(top)
		self.e1.pack()
		self.e2 = Entry(top)
		self.e2.pack()
		self.e3 = Entry(top)
		self.e3.pack()
		self.e4 = Entry(top)
		self.e4.pack()
		self.e5 = Entry(top)
		self.e5.pack()
		b = Button(top, text="Create", command=self.createVector)
		b.pack()

	def createVector(self):
		entryGetList = [self.e1.get(), self.e2.get(), self.e3.get(), 
								self.e4.get(), self.e5.get()]
		# .get() returns strings, so evaluate the strings and use that to create
		# the new vector
		try:
			elementsList = [sym.simplify(eval(item)) for item in entryGetList if item != ""]
			vectorCreated = Vector(elementsList)
			self.Workspace.addToWorkspace(WorkspaceObject(self.posX,self.posY,
				vectorCreated))
			self.top.destroy()
		except: tkMessageBox.showerror("Creation Error",
			"The app could not parse this text. Please check the help screen.")

class PolynomialCreationDialog(object):

	def __init__(self, parent, Workspace, posX, posY):
		top = self.top = Toplevel(parent)
		self.Workspace = Workspace
		self.posX, self.posY = posX, posY
		Label(top, text="Polynomial Creation").pack()
		# initialize entry field and button
		self.e1 = Entry(top)
		self.e1.pack()
		b = Button(top, text="Create", command=self.createPolynomial)
		b.pack()

	def createPolynomial(self):
		fnString = self.e1.get()
		# attempt to parse the text using sympy, if it does not
		# work, display error dialog
		try:
			self.Workspace.addToWorkspace(WorkspaceObject(self.posX, 
				self.posY, sym.simplify(eval(fnString))))
			self.top.destroy()
		except: tkMessageBox.showerror("Creation Error", 
			"The app could not parse this text. Please check the help screen.")

class EvaluationDialog(object):

	def __init__(self, parent, Workspace, WorkspaceObject):
		top = self.top = Toplevel(parent)
		self.Workspace, self.WorkspaceObject = Workspace, WorkspaceObject
		Label(top, text="Evaluation").pack()
		# initialize entries and button
		self.xEntry = Entry(top)
		self.xEntry.insert(0, "x")
		self.xEntry.pack()
		self.yEntry = Entry(top)
		self.yEntry.insert(0, "y")
		self.yEntry.pack()
		self.zEntry = Entry(top)
		self.zEntry.insert(0, "z")
		self.zEntry.pack()
		b = Button(top, text="Evaluate", command=self.evaluateAt)
		b.pack()

	def evaluateAt(self):
		# attempt to parse the values text, evaluate the 'inner' objects
		# and add the resulting object to the workspace
		offset = 20
		try:
			values = [eval(self.xEntry.get()), eval(self.yEntry.get()),
							eval(self.zEntry.get())]
			valsAndVars = zip([x,y,z], values)
			returnX, returnY = (self.WorkspaceObject.posX, 
				self.WorkspaceObject.posY+offset)
			if(type(self.WorkspaceObject.inner()) == Vector):
				try:
					newVector = self.WorkspaceObject.inner().evalAt(values)
					self.Workspace.addToWorkspace(WorkspaceObject(returnX,
						returnY, newVector))
					self.top.destroy()
				except:
					tkMessageBox.showerror("Evaluation Error",
						"You cannot evaluate this object with \
						the given values.")
			else:
				try:
					newPolynomial = PolynomialMultiVar.evalAt(
						self.WorkspaceObject.inner(), values)
					self.Workspace.addToWorkspace(WorkspaceObject(returnX,
						returnY, newPolynomial))
					self.top.destroy()
				except:
					tkMessageBox.showerror("Evaluation Error",
						"You cannot evaulate this object with \
						the given values.")
		except:
			tkMessageBox.showerror("Evaluation Error",
				"The app could not parse this text. \
				Please check the help screen.")

############
#APP WINDOW#
############

class VPWorkspaceWindow(EventBasedAnimationClass):

	def __init__(self):
		self.checkFilesHandler()
		self.declareSettings()
		canvasWidth, canvasHeight = self.wRatio*self.margin, self.hRatio*self.margin
		super(VPWorkspaceWindow, self).__init__(canvasWidth, canvasHeight)
		self.canvasWidth, self.canvasHeight = canvasWidth, canvasHeight

	def checkAllFiles(self):
		sourceFilesPath = "vpworkspace"
		dirPath = sys.path[0]
		pathIndex = dirPath.rfind(sourceFilesPath)
		topDirPath = dirPath[:pathIndex]
		readmePath, tkinterColorChartPath = "README.md", "tkinterColorChart.png"
		docsPath, licensePath = "docs", "LICENSE"
		print "Checking home directory...",
		assert(os.path.exists(topDirPath+docsPath))
		assert(os.path.exists(topDirPath+licensePath))
		assert(os.path.exists(topDirPath+readmePath))
		assert(os.path.exists(topDirPath+tkinterColorChartPath))
		assert(os.path.exists(topDirPath+sourceFilesPath))
		print "Passed"
		self.navProjectFiles(topDirPath+sourceFilesPath)

	def navProjectFiles(self, path):
		# top level file check
		print "Checking project directory..."
		assert(os.path.exists(path+os.sep+"settings.txt"))
		assert(os.path.exists(path+os.sep+"__init__.py"))
		assert(os.path.exists(path+os.sep+"VPWorkspaceWindow.py"))
		# do a folder check for more directories
		assert(os.path.exists(path+os.sep+"assets"))
		self.checkAssetsFolder(path+os.sep+"assets")
		assert(os.path.exists(path+os.sep+"graphics"))
		self.checkGraphicsFolder(path+os.sep+"graphics")
		assert(os.path.exists(path+os.sep+"source"))
		self.checkSourceFolder(path+os.sep+"source")
		assert(os.path.exists(path+os.sep+"test"))
		self.checkTestFolder(path+os.sep+"test")
		# check workspace saving folder
		assert(os.path.exists(path+os.sep+"Saved Workspaces"))
		print "All paths found. Starting up..."

	def checkAssetsFolder(self, path):
		# crawl the assets folder for the help text files
		# eventually, image files will be placed here for logos etc.
		print ">>> Checking assets folder...",
		topPath = path
		genHelpPath = topPath+os.sep+"genHelp.txt"
		vectorHelpPath = topPath+os.sep+"vectorHelp.txt"
		polyHelpPath = topPath+os.sep+"polyHelp.txt"
		matrixHelpPath = topPath+os.sep+"matrixHelp.txt"
		allHelpPaths = [genHelpPath, vectorHelpPath, polyHelpPath, 
			matrixHelpPath]
		assert(all([os.path.exists(helpPath) for helpPath in allHelpPaths]))
		print "Passed"

	def checkGraphicsFolder(self, path):
		# crawl the graphics folder for the graphics startup files
		# these files are taken directly from CMU 15-112
		print ">>> Checking graphics folder...",
		topPath = path
		assert(os.path.exists(topPath+os.sep+"__init__.py"))
		graphicsPaths = ["basicAnimation.py", "basicAnimationClass.py",
			"eventBasedAnimationClass.py"]
		assert(all([os.path.exists(topPath+os.sep+graphicsPath) 
			for graphicsPath in graphicsPaths]))
		print "Passed"

	def checkSourceFolder(self, path):
		# crawl the graphics folder for the backend class files
		# that I wrote to implement some data types
		print ">>> Checking source folder...",
		topPath = path
		assert(os.path.exists(topPath+os.sep+"__init__.py"))
		sourcePaths = ["matrixClass.py", "polynomialClass.py",
			"vectorClass.py"]
		assert(all([os.path.exists(topPath+os.sep+sourcePath)
			for sourcePath in sourcePaths]))
		print "Passed"

	def checkTestFolder(self, path):
		# placeholder until I devise unit tests for the classes
		# that I have written
		print ">>> Checking test folder...",
		print "Passed"

	def checkFilesHandler(self):
		# this function just checks all file paths and displays
		# an error popup if something is wrong with the installation
		try:
			self.checkAllFiles()
		except:
			tkMessageBox.showerror("Installation Error",
				"One or more paths is not present.\n\
				Please go to https://github.com/garthur/vp_workspace\
				to redownload the repository")
			raise Exception("Installation Error")
			self.root.quit()

	def declareSettings(self):
		settingsText = readFile("settings.txt")
		for line in settingsText.splitlines():
			if (line.startswith("//")):
				settingVal = line.split(" ")
				currentSetting = settingVal[0].strip("//")
				currentVal = settingVal[1]
				try:
					setattr(self, currentSetting, int(currentVal))
				except:
					setattr(self, currentSetting, currentVal)


	#########################
	#INITIALIZATION HANDLERS#
	#########################

	def initAnimation(self):
		# configure the root window
		self.root.resizable(width=FALSE, height=FALSE)
		# bind events to appropriate functions
		self.root.bind("<Key>", lambda event: self.onKeyPressed(event))
		self.root.bind("<Button-1>", lambda event: self.onMousePressed(event))
		self.root.bind("<Button-3>", lambda event: self.onRightMouse(event))
		self.root.bind("<Motion>", lambda event: self.onMouseMotion(event))
		self.root.bind("<Shift-Key>", 
			lambda event: self.onShiftKeyPressed(event))
		self.root.bind("<Control-Key>", lambda event: self.onCtrlKeyPressed(event))
		self.root.bind("<B1-Motion>", lambda event: self.onLeftDrag(event))
		# initialize mouse location
		self.mouseX, self.mouseY = 0, self.margin
		# create a workspace
		self.workspace = Workspace()
		self.mode = "start"
		self.timerDelay = 200
		# initialize variables that determine whether or not
		# help screens will be displayed
		self.helpTypes = ["Help", "vectorHelp", "polyHelp", "matrixHelp"]
		self.helpIndex = 0
		# initialize right-click popup menu
		self.initPopupMenu()

	def restart(self):
		self.initAnimation()

	def initPopupMenu(self):
		# menu gets recreated every time it is posted to screen,
		# so the actual work happens in updatePopupMenu
		self.popupMenu = Menu(self.root, tearoff=0,
			postcommand=self.updatePopupMenu)

	def initDerivativeSubmenu(self, activeItem):
		self.derivMenu = Menu(self.root, tearoff=0)
		def deriv(variable): 
			derivative = WorkspaceObject(activeItem.posX, activeItem.posY+20, 
				PolynomialMultiVar.differentiateWithRespect(activeItem.inner(),
					variable))
			self.workspace.addToWorkspace(derivative)
		self.derivMenu.add_command(label=u"\u2202"+"X", 
			command= lambda: deriv('x'))
		self.derivMenu.add_command(label=u"\u2202"+"Y", 
			command= lambda: deriv('y'))
		self.derivMenu.add_command(label=u"\u2202"+"Z", 
			command= lambda: deriv('z'))

	def updatePopupMenu(self):
		# clear all leftover entries from the menu
		self.popupMenu.delete(0, END)
		activeItem = self.workspace.activeItem
		offset = 20
		# find the item that is currently being hovered over, 
		# and create the menu based on what type of object it is
		if (activeItem != None):
			# bind commands to entries on the popup menu 
			def evaluate(): self.evaluateObject(activeItem)
			def information(): self.showInformationString(activeItem)
			if (type(activeItem.inner()) == Vector):
				magnitude = WorkspaceObject(activeItem.posX,
					activeItem.posY+offset, activeItem.inner().findLength())
				unitVector = WorkspaceObject(activeItem.posX,
					activeItem.posY+offset, activeItem.inner().unitVector())
				def addMagnitude(): self.workspace.addToWorkspace(magnitude)
				def addUnitVector(): self.workspace.addToWorkspace(unitVector)
				self.popupMenu.add_command(label="Magnitude",
					command= addMagnitude)
				self.popupMenu.add_command(label="Unit Vector",
					command= addUnitVector)
				self.popupMenu.add_command(label="Information",
					command= information)
			else:
				# the 'derivative' option has a submenu, which is above
				self.initDerivativeSubmenu(activeItem)
				gradientObject = WorkspaceObject(activeItem.posX, 
					activeItem.posY+offset, PolynomialMultiVar.fnGradient(
						activeItem.inner()))
				def addGradientVector(): 
					self.workspace.addToWorkspace(gradientObject)
				def graphFunction(): 
					PolynomialMultiVar.graphFunction(activeItem.inner())
				self.popupMenu.add_command(label=u"\u07DC"+"Gradient", 
					command= addGradientVector)
				self.popupMenu.add_cascade(label="Derivative", 
					menu=self.derivMenu)
				self.popupMenu.add_command(label="Graph", 
					command= graphFunction)
				self.popupMenu.add_command(label="Information", 
					command= information)
			self.popupMenu.add_command(label="Evaluate At", 
				command= evaluate)
		self.popupMenu.add_command(label="Remove", 
			command=lambda: self.workspace.deleteSelectedObject(self.mouseX,
				self.mouseY))
		self.popupMenu.add_separator()
		self.popupMenu.add_command(label="Open", 
			command=lambda: self.openWorkspace())
		self.popupMenu.add_command(label="Save",
			command=lambda: self.saveWorkspace())
		self.popupMenu.add_separator()
		def activateHelp(): self.mode = "Help" if (self.mode == "working") else "working"
		self.popupMenu.add_command(label="Help" if (self.mode=="working") 
			else "Workspace", command= activateHelp)
		self.popupMenu.add_command(label="Clear",
			command= lambda: self.workspace.clearWorkspace())
		self.popupMenu.add_command(label="Exit",
			command= lambda: self.savePopupAndQuit())

	##########
	#FILE I/O#
	##########

	def savePopupAndQuit(self):
		# checks if the user wants to save before quitting the app
		save = tkMessageBox.askyesno("Quit", "Do you want to save and quit?")
		if (save):
			self.saveWorkspace(self.makeWorkspaceReprString())
		self.root.quit()

	def makeWorkspaceReprString(self):
		# represents every item in the workspace
		# for use in saving a workspace as a .txt file
		return "\n".join([repr(item) for item in self.workspace.objects])

	def getWorkspaceFromReprString(self, reprString):
		# re-evaluates each string into a workspace object
		# for use in opening a workspace from a .txt file
		return Workspace([eval(item) for item in reprString.splitlines()])

	def saveWorkspace(self):
		# turns workspace into a string, gets path from tkFileDialog
		contents = self.makeWorkspaceReprString()
		path = tkFileDialog.asksaveasfilename(initialdir="Saved Workspaces", 
			defaultextension=".txt")
		# create path if none exists yet
		if (not os.path.exists("Saved Workspaces")):
			os.makedirs("Saved Workspaces")
		# write contents to file
		writeFile(path, contents)
		print "Saving...   " + path

	def openWorkspace(self):
		# get path from tkFileDialog
		path = tkFileDialog.askopenfilename(initialdir="Saved Workspaces")
		print "Opening...   ",
		if (not os.path.exists("Saved Workspaces")):
			os.makedirs("Saved Workspaces")
			print "The 'Saved Workspaces' folder was not found."
		# read from file and set as current workspace
		else:
			reprString = readFile(path)
			self.workspace = self.getWorkspaceFromReprString(reprString)
			print path

	###########################
	#WORKSPACE OBJECT HANDLERS#
	###########################

	def showInformationString(self, item):
		# this method displays a short information string at the bottom of
		# screen, serving almost as the 'console' for this window
		if (type(item.inner()) == Vector):
			self.workspace.operationText = item.inner().genBasicInfoString()
		else:
			infoText = PolynomialMultiVar.genBasicInfoString(item.inner())
			self.workspace.operationText = infoText

	def vectorCreation(self):
		# initializes a vector creation dialog, shown above
		VectorCreationDialog(self.root, self.workspace, self.mouseX,
			self.mouseY)

	def polynomialCreation(self):
		# initializes a polynomial creation dialog
		PolynomialCreationDialog(self.root, self.workspace, self.mouseX,
			self.mouseY)

	def evaluateObject(self, activeObject):
		# initializes an evaluation dialog
		EvaluationDialog(self.root, self.workspace, activeObject)

	def inWorkspace(self):
		# determines if the current mouse location is in the workspace
		if(self.mouseY<self.margin or 
			self.mouseY>self.canvasHeight-self.margin):
			return False
		return True

	def inTitleBar(self):
		return (not self.inWorkspace())

	def handleOperation(self, operation):
		# a wrapper function for workspace operations
		# displays an error message if an operation fails
		try:
			self.workspace.performOperation(operation, 
				self.mouseX, self.mouseY)
		except:
			tkMessageBox.showerror("Operation Error",
				"This workspace does not support that operation.")

	################
	#EVENT HANDLERS#
	################

	def onMouseMotion(self, event):
		# simply update the mouse position
		self.mouseX, self.mouseY = event.x, event.y
		if (self.mode == "working"):
			self.workspace.checkForActive(self.mouseX, self.mouseY)

	def onMousePressed(self, event):
		# first unpost the right click menu, if it is posted
		# then tries to select 
		self.popupMenu.unpost()
		if(self.inWorkspace() and self.mode == "working"):
			self.workspace.selectObject(self.mouseX, self.mouseY)

	def onLeftDrag(self, event):
		self.mouseX, self.mouseY = event.x, event.y
		if(self.inWorkspace() and self.workspace.objectSelected()):
			self.workspace.moveObject(self.mouseX, self.mouseY)

	def onShiftKeyPressed(self, event):
		if(event.char in "*+"):
			self.handleOperation(event.char)

	def onCtrlKeyPressed(self, event):
		if (event.keysym == "s"):
			self.saveWorkspace()
		elif (event.keysym == "o"):
			self.openWorkspace()

	def onKeyPressed(self, event):
		self.popupMenu.unpost()
		if(self.mode == "working"):
			if (event.keysym == "Shift_L" or event.keysym == "Control_L"):
				pass
			elif(event.keysym == "Return"):
				self.workspace.clearWorkspace()
			elif(event.keysym == "BackSpace"):
				self.workspace.deleteLastObject()
			elif(event.char in "1234567890"):
				if(self.inWorkspace() and not 
					self.workspace.objectSelected()):
					self.workspace.addToWorkspace(WorkspaceObject(self.mouseX, 
						self.mouseY, eval(event.char)))
			elif(event.char in "/-"):
				if(self.inWorkspace()):
					self.handleOperation(event.char)
			elif(event.char == "v"):
				self.vectorCreation()
			elif(event.char == "p"):
				self.polynomialCreation()
			elif(event.char == "h"):
				self.helpIndex = 0
				self.mode = self.helpTypes[self.helpIndex]
		elif("Help" in self.mode):
			if(event.keysym == "Right"):
				self.helpIndex = (self.helpIndex+1)%len(self.helpTypes)
				self.mode = self.helpTypes[self.helpIndex]
			elif(event.keysym == "Left"):
				self.helpIndex = (self.helpIndex-1)%len(self.helpTypes)
				self.mode = self.helpTypes[self.helpIndex]
			elif(event.char == "h"): self.mode = "working"
		elif(self.mode == "start"):
			if(event.keysym == "Return"):
				self.activateStartScreen()
				
	def onRightMouse(self, event):
		self.popupMenu.unpost()
		try:
			self.popupMenu.tk_popup(event.x_root, event.y_root)
		finally:
			self.popupMenu.grab_release()

	################
	#DRAW FUNCTIONS#
	################

	def drawGradient(self, orientation, x0=0, y0=0, x1=0, y1=0):
		# set up bounds for the gradient to be drawn
		limit = x1 if (orientation == "vert") else y1
		loopLowBound = x0 if (orientation == "vert") else y0
		distanceToTravel = (x1-x0) if (orientation == "vert") else (y1-y0)
		# get rgb from tkinter colors
		(r1,g1,b1) = self.root.winfo_rgb(self.color1)
		(r2,g2,b2) = self.root.winfo_rgb(self.color2)
		rRatio = float(r2-r1)/distanceToTravel
		gRatio = float(g2-g1)/distanceToTravel
		bRatio = float(b2-b1)/distanceToTravel
		# increment rgb as the x or y value increases
		for i in xrange(loopLowBound, limit+1):
			nr = int(r1 + (rRatio*i))
			ng = int(g1 + (gRatio*i))
			nb = int(b1 + (bRatio*i))
			# create hex color and draw the lines
			color = "#%4.4x%4.4x%4.4x" % (nr,ng,nb)
			if (orientation == "horiz"):
				self.canvas.create_line(x0,i,x1,i, fill=color)
			elif (orientation == "vert"):
				self.canvas.create_line(i,y0,i,y1, fill=color)

	def drawOperationText(self):
		posX, posY = 0, self.canvasHeight-self.margin
		opText = self.workspace.operationText
		fontSize = 10
		font = "Arial %d" %(fontSize)
		self.canvas.create_text(posX, posY, anchor="nw", text=opText, 
			fill="red", font=font)

	def drawTitle(self):
		title = "VP Workspace"
		offset = 5
		self.canvas.create_text(offset, self.margin/2.0, anchor="w", text=title,
			font="Helvetica 20 bold")

	def drawLoadingBar(self, timeElapsed):
		x0 = self.canvasWidth/3.0
		y0, y1 = self.canvasHeight/2.0 - 5, self.canvasHeight/2.0 + 5
		x1 = x0 + (timeElapsed*x0)
		self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", 
			outline="white")

	def activateStartScreen(self):
		timeToLoad = 2.5
		timeIncrement = 0.001
		timeRatio = 0
		def emptyF(): pass
		timingThread = threading.Timer(timeToLoad, emptyF)
		timingThread.start()
		while (timingThread.is_alive()):
			self.root.update()
			time.sleep(timeIncrement)
			timeRatio += (timeIncrement/timeToLoad)*10
			if (timeRatio <= 1):
				self.drawLoadingBar(timeRatio)
		timeRatio = 0
		self.mode = "working"

	def drawStaticStartScreen(self):
		# draws a static start screen with 
		self.drawGradient("horiz", 0, 0, self.canvasWidth, self.canvasHeight)
		self.canvas.create_text(self.canvasWidth/2.0, self.canvasHeight/2.0 - 30,
			text="VP Workspace", font="Arial 20 bold")

	def drawHelp(self):
		offset = 60
		self.canvas.create_rectangle(0, self.margin, self.canvasWidth,
			self.canvasHeight-self.margin, fill="white")
		helpText = readFile("assets"+os.sep+"genHelp.txt")
		if (self.mode == "Help"):
			self.canvas.create_text(self.canvasWidth/2.0, self.margin, 
				anchor="n", text="General Help", font="Arial 15 bold")
			self.canvas.create_text(self.margin, self.margin+offset, 
				anchor="nw", text=helpText)
		elif(self.mode == "vectorHelp"):
			self.vectorHelp()
		elif(self.mode == "polyHelp"):
			self.polynomialHelp()

	def vectorHelp(self):
		offset1 = 5
		self.canvas.create_text(self.canvasWidth/2.0, self.margin+offset1,
			anchor="n", text="Vector Help", font="Arial 15 bold")
		vectorHelpText = readFile("assets"+os.sep+"vectorHelp.txt")
		offset2 = 60
		self.canvas.create_text(self.margin, self.margin+offset2, anchor="nw",
			text=vectorHelpText)

	def polynomialHelp(self):
		offset1 = 5
		self.canvas.create_text(self.canvasWidth/2.0, self.margin+offset1,
			anchor="n", text="Polynomial Help", font="Arial 15 bold")
		polyHelpText = readFile("assets"+os.sep+"polyHelp.txt")
		offset2 = 60
		self.canvas.create_text(self.margin, self.margin+offset2, anchor="nw",
			text=polyHelpText)

	def redrawAll(self):
		self.drawGradient("vert", 0, 0, self.canvasWidth, self.margin)
		self.drawGradient("vert", 0, self.canvasHeight-self.margin, 
			self.canvasWidth, self.canvasHeight)
		self.drawTitle()
		if(self.mode == "working"):
			self.workspace.drawWorkspace(self.canvas, 0, self.margin, 
				self.canvasWidth, self.canvasHeight-self.margin, self.mouseX, 
					self.mouseY)
			self.drawOperationText()
		elif("Help" in self.mode):
			self.drawHelp()
		elif(self.mode == "start"):
			self.drawStaticStartScreen()

if __name__ == "__main__":
	window = VPWorkspaceWindow()
	window.run()