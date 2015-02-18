# 15-112 term project
# basic testWindow

import copy
import os
import sympy as sym
# some special functions need to be imported for eval purposes
from sympy import cos, acos, sin, asin, tan, atan, cot, sec, csc, pi, ln, log, sqrt

from vectorClass import Vector
from polynomialClass import PolynomialMultiVar

# import graphics modules
from eventBasedAnimationClass import EventBasedAnimationClass
from Tkinter import *
import tkMessageBox, tkFileDialog

x, y, z = sym.symbols('x y z')

def readFile(filename, mode="rt"):
    # rt = "read text"
    with open(filename, mode) as fin:
        return fin.read()

def writeFile(filename, contents, mode="wt"):
    # wt = "write text"
    with open(filename, mode) as fout:
        fout.write(contents)

def replaceFunctionSymbolsWithUnicode(s):
	mulAndPow = s.replace("**","^").replace("*",u"\u2219")
	mulAndPowAndDiv = mulAndPow.replace("pi",u"\u03C0").replace("sqrt",u"\u221A")
	return mulAndPowAndDiv

class WorkspaceObject(object):

	def __init__(self, posX, posY, containedObject):
		self.object = containedObject
		self.posX, self.posY = posX, posY
		self.height = 10
		self.width = (len(str(containedObject))*7)/2.0 

	# all methods between this and the next comment 
	# deal with how the object is displayed on screen
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

	# this method simply returns the inner object without
	# any x or y position
	def inner(self):
		return self.object

	def __repr__(self):
		return "WorkspaceObject(%d,%d,%s)" %(self.posX, self.posY,
			repr(self.inner()))

class Workspace(object):

	def __init__(self, objects=[]):
		self.objects = objects
		self.workingObjects = []
		self.operationText = ""

	def drawWorkspace(self, canvas, x0, y0, x1, y1, mouseX, mouseY):
		canvas.create_rectangle(x0, y0, x1, y1, fill="white")
		for item in self.objects:
			try: 
				item.draw(canvas)
				if (item.isSelected(mouseX,mouseY) and 
							item not in self.workingObjects):
					item.highlight(canvas)
			except:
				canvas.create_text(x0+10, y1+10, text=str(item), fill='red')
		for i in xrange(len(self.workingObjects)):
				self.workingObjects[i].highlight(canvas, 'blue')
				self.workingObjects[i].labelOrder(canvas, i+1)

	def objectSelected(self, posX, posY):
		for item in self.objects:
			if (item.isSelected(posX,posY)):
				return True
		return False

	def moveObject(self, newX, newY):
		for item in self.objects:
			if(item.isSelected(newX,newY)):
				item.move(newX, newY)

	def selectObject(self, posX, posY):
		if(not self.objectSelected(posX,posY)):
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
					primeItem *= innerObjects[i]
				elif(operation == '/'):
					primeItem /= innerObjects[i]
				elif(operation == '+'):
					primeItem += innerObjects[i]
				elif(operation == '-'):
					primeItem -= innerObjects[i]
			primeItem = sym.simplify(primeItem)
			self.addToWorkspace(WorkspaceObject(returnX, returnY, primeItem))
		except:
			tkMessageBox.showerror("Operation Error",
				"This workspace does not support that operation.")

################################################################################
#DIALOG BOXES
################################################################################
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
		# the vector
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

################################################################################
#APP WINDOW
################################################################################

class VPWorkspaceWindow(EventBasedAnimationClass):

	def __init__(self):
		margin = 50
		canvasWidth, canvasHeight = 16*margin, 9*margin
		super(VPWorkspaceWindow, self).__init__(canvasWidth, canvasHeight)
		self.margin = canvasHeight/9.0
		self.canvasWidth, self.canvasHeight = canvasWidth, canvasHeight

	def initAnimation(self):
		# create a workspace
		self.Workspace1 = Workspace()
		self.timerDelay = 200
		# initialize variables that determine whether or not
		# help screens will be displayed
		self.help = self.vectorHelpDisplay = self.polynomialHelpDisplay = False
		# bind events to appropriate functions
		self.root.bind("<Configure>", lambda event: self.sizeChanged(event))
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
		# initialize right-click popup menu
		self.initPopupMenu()

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
			self.Workspace1.addToWorkspace(derivative)
		self.derivMenu.add_command(label=u"\u2202"+"X", 
			command= lambda: deriv('x'))
		self.derivMenu.add_command(label=u"\u2202"+"Y", 
			command= lambda: deriv('y'))
		self.derivMenu.add_command(label=u"\u2202"+"Z", 
			command= lambda: deriv('z'))

	def updatePopupMenu(self):
		# clear all leftover entries from the menu
		self.popupMenu.delete(0, END)
		activeItem = None
		offset = 20
		# find the item that is currently being hovered over, 
		# and create the menu based on what type of object it is
		for item in self.Workspace1.objects:
			if(item.isSelected(self.mouseX,self.mouseY)):
				activeItem = item
				break
		if (activeItem != None):
			# bind commands to entries on the popup menu 
			def evaluate(): self.evaluateObject(activeItem)
			def information(): self.showInformationString(activeItem)
			if (type(activeItem.inner()) == Vector):
				magnitude = WorkspaceObject(activeItem.posX,
					activeItem.posY+offset, activeItem.inner().findLength())
				unitVector = WorkspaceObject(activeItem.posX,
					activeItem.posY+offset, activeItem.inner().unitVector())
				def addMagnitude(): self.Workspace1.addToWorkspace(magnitude)
				def addUnitVector(): self.Workspace1.addToWorkspace(unitVector)
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
					self.Workspace1.addToWorkspace(gradientObject)
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
			command=lambda: self.Workspace1.deleteSelectedObject(self.mouseX,
				self.mouseY))
		self.popupMenu.add_separator()
		self.popupMenu.add_command(label="Open", 
			command=lambda: self.openWorkspace())
		self.popupMenu.add_command(label="Save",
			command=lambda: self.saveWorkspace())
		self.popupMenu.add_separator()
		def activateHelp(): self.help = not self.help
		self.popupMenu.add_command(label="Help" if not self.help else "Workspace",
			command= activateHelp)
		self.popupMenu.add_command(label="Clear",
			command= lambda: self.Workspace1.clearWorkspace())
		self.popupMenu.add_command(label="Exit",
			command= lambda: self.savePopupAndQuit())

############# IN PROGRESS ##############

	def savePopupAndQuit(self):
		save = tkMessageBox.askyesno("Quit", "Do you want to save and quit?")
		if (save):
			self.saveWorkspace(self.makeWorkspaceReprString())
		self.root.quit()

############# IN PROGRESS ##############

	def makeWorkspaceReprString(self):
		# represents every item in the workspace
		# for use in saving a workspace as a .txt file
		return "\n".join([repr(item) for item in self.Workspace1.objects])

	def getWorkspaceFromReprString(self, reprString):
		# re-evaluates each string into a workspace object
		# for use in opening a workspace from a .txt file
		return Workspace([eval(item) for item in reprString.splitlines()])

	def saveWorkspace(self):
		# turns workspace into a string, gets path from tkFileDialog
		contents = self.makeWorkspaceReprString()
		path = tkFileDialog.asksaveasfilename(initialdir="Workspaces", 
			defaultextension=".txt")
		# create path if none exists yet
		if (not os.path.exists("Workspaces")):
			os.makedirs("Workspaces")
		# write contents to file
		writeFile(path, contents)
		print "Saving...   " + path

	def openWorkspace(self):
		# get path from tkFileDialog
		path = tkFileDialog.askopenfilename(initialdir="Workspaces")
		print "Opening...   " + path
		if (not os.path.exists("Workspaces")):
			os.makedirs("Workspaces")
		# read from file and set as current workspace
		else:
			reprString = readFile(path)
			self.Workspace1 = self.getWorkspaceFromReprString(reprString)

	def showInformationString(self, item):
		# this method displays a short information string at the bottom of
		# screen, serving almost as the 'console' for this window
		if (type(item.inner()) == Vector):
			self.Workspace1.operationText = item.inner().genBasicInfoString()
		else:
			infoText = PolynomialMultiVar.genBasicInfoString(item.inner())
			self.Workspace1.operationText = infoText

	def vectorCreation(self):
		# initializes a vector creation dialog, shown above
		VectorCreationDialog(self.root, self.Workspace1, self.mouseX,
			self.mouseY)

	def polynomialCreation(self):
		# initializes a polynomial creation dialog
		PolynomialCreationDialog(self.root, self.Workspace1, self.mouseX,
			self.mouseY)

	def evaluateObject(self, activeObject):
		# initializes an evaluation dialog
		EvaluationDialog(self.root, self.Workspace1, activeObject)

	def inWorkspace(self):
		# determines if the current mouse location is in the workspace
		if(self.mouseY<self.margin or 
			self.mouseY>self.canvasHeight-self.margin):
			return False
		return True

	#def inTitleBar(self):
	#	return (not self.inWorkspace())

	def onMouseMotion(self, event):
		# simply update the mouse position
		self.mouseX, self.mouseY = event.x, event.y

############# IN PROGRESS ##############

	def sizeChanged(self, event):
		self.canvasWidth = event.width - 4
		self.canvasHeight = event.height - 4
		self.margin = self.canvasHeight/9.0
		self.redrawAll()

############# IN PROGRESS ##############

	def onMousePressed(self, event):
		# first unpost the right click menu, if it is posted
		# then 
		self.popupMenu.unpost()
		if(self.inWorkspace()):
			self.Workspace1.selectObject(self.mouseX, self.mouseY)

	def onLeftDrag(self, event):
		self.mouseX, self.mouseY = event.x, event.y
		if(self.inWorkspace() and self.Workspace1.objectSelected(self.mouseX,
			self.mouseY)):
			self.Workspace1.moveObject(self.mouseX, self.mouseY)

	def onShiftKeyPressed(self, event):
		if(event.char in "*+"):
			self.Workspace1.performOperation(event.char, self.mouseX,
				self.mouseY)

	def onCtrlKeyPressed(self, event):
		if (event.keysym == "s"):
			self.saveWorkspace()
		elif (event.keysym == "o"):
			self.openWorkspace()

	def onKeyPressed(self, event):
		self.popupMenu.unpost()
		if(not self.help):
			if (event.keysym == "Shift_L" or event.keysym == "Control_L"):
				pass
			elif(event.keysym == "Return"):
				self.Workspace1.clearWorkspace()
				self.redrawAll()
			elif(event.keysym == "BackSpace"):
				self.Workspace1.deleteLastObject()
			elif(event.char in "1234567890"):
				if(self.inWorkspace() and not 
					self.Workspace1.objectSelected(self.mouseX, self.mouseY)):
					self.Workspace1.addToWorkspace(WorkspaceObject(self.mouseX, 
						self.mouseY, eval(event.char)))
			elif(event.char in "/-"):
				if(self.inWorkspace()):
					self.Workspace1.performOperation(event.char, self.mouseX,
						self.mouseY)
			elif(event.char == "v"):
				self.vectorCreation()
			elif(event.char == "p"):
				self.polynomialCreation()
		if(event.char == "h"):
			self.help = not(self.help)
			if(not self.help):
				self.vectorHelpDisplay = self.polynomialHelpDisplay = False
		elif(event.keysym == "Down"):
			self.vectorHelpDisplay = self.polynomialHelpDisplay = False
		elif(event.keysym == "Right"):
			if(self.help):
				self.vectorHelpDisplay = True
				self.polynomialHelpDisplay = False
		elif(event.keysym == "Left"):
			if(self.help):
				self.polynomialHelpDisplay = True
				self.vectorHelpDisplay = False

	def onRightMouse(self, event):
		self.popupMenu.unpost()
		try:
			self.popupMenu.tk_popup(event.x_root, event.y_root)
		finally:
			self.popupMenu.grab_release()

	def drawOperationText(self):
		posX, posY = 0, self.canvasHeight-self.margin
		opText = self.Workspace1.operationText
		fontSize = 10
		font = "Arial %d" %(fontSize)
		self.canvas.create_text(posX, posY, anchor="nw", text=opText, 
			fill="red", font=font)

	def drawTitle(self):
		title = "VP Workspace"
		fontScale = 20
		titleSize = len(title)*fontScale
		offset = 5
		self.canvas.create_text(offset, self.margin/2.0, anchor="w", text=title,
			font="Helvetica 20 bold")

	def drawHelp(self):
		offset = 60
		self.canvas.create_rectangle(0, self.margin, self.canvasWidth,
			self.canvasHeight-self.margin, fill="white")
		helpText = "Press 'v' to create a vector and 'p' for a polynomial.\
\n\
\nClick on an object to select it. Selected items are highlighted\
\n  in blue with their queue position in the top right.\
\n\
\nRight-clicking will display a popup menu specific to the item selected.\
\nFor more info on the commands in this popup menu, please see the specialized\
\n  help sections as described below."
		controlsText = "Press right arrow for vector help and left for \
polynomial help. To return here, press the down button."
		if (not any([self.vectorHelpDisplay, self.polynomialHelpDisplay])):
			self.canvas.create_text(self.canvasWidth/2.0, self.margin, 
				anchor="n", text="General Help", font="Arial 15 bold")
			self.canvas.create_text(self.margin, self.margin+offset, 
				anchor="nw", text=helpText)
			self.canvas.create_text(self.margin, self.canvasHeight/1.5,
				anchor="nw", text=controlsText)
		elif(self.vectorHelpDisplay):
			self.vectorHelp()
		elif(self.polynomialHelpDisplay):
			self.polynomialHelp()

	def vectorHelp(self):
		offset1 = 5
		self.canvas.create_text(self.canvasWidth/2.0, self.margin+offset1,
			anchor="n", text="Vector Help", font="Arial 15 bold")
		generalHelpText = "Press 'V' to create a vector.\
\nThis workspace supports vectors that contain polynomials. See polynomial help\
 for more info."
		commandText = "Workspace Commands:\
\n  (*): vector multiplication, dot product if multiple vectors selected\
\n  (/): vector division, cross product if multiple vectors\
\n  (+): vector addition\
\n  (-): vector subtraction"
		menuDescription = "Menu Commands:\
\n  (Unit Vector): returns a vector of length 1 in the same direction\
\n  (Evaluate): returns a vector whose elemets are evaluated at certain values\
\n  (Information): displays some basic information about the vector"
		offset2 = 60
		self.canvas.create_text(self.margin, self.margin+offset2, anchor="nw",
			text=generalHelpText)
		self.canvas.create_text(self.margin, self.canvasHeight/2.4, 
			anchor="nw", text=commandText)
		self.canvas.create_text(self.margin, self.canvasHeight*(2/3.0),
			anchor="nw", text=menuDescription)

	def polynomialHelp(self):
		offset1 = 5
		self.canvas.create_text(self.canvasWidth/2.0, self.margin+offset1,
			anchor="n", text="Polynomial Help", font="Arial 15 bold")
		generalHelpText = "Press 'P' to create a polynomial.\
\nThis app supports trigonometric functions, as well as natural logs.\
\nWhen creating a polynomial, please use the following symbols:\
\n\t(**):power, (*):multiply, (/):divide, \n\t(+):add, (-):subtract, \
(x, y, z):variables"
		commandText = "Workspace Commands:\
\n (*): polynomial multiplication\
\n (/): polynomial division\
\n (+): polynomial addition\
\n (-): polynomial subtraction"
		menuDescription = "Menu Commands:\
\n (Gradient): returns a vector whose elements are the partial derivatives \
of the function\
\n (Derivative): returns the derivative of a function with respect to a \
variable\
\n (Graph): graphs a plot of the function\
\n (Evaluate): returns the function, evaluated a the given values\
\n (Information): displays some basic information about the polynomial"
		offset2 = 60
		self.canvas.create_text(self.margin, self.margin+offset2, anchor="nw",
			text=generalHelpText)
		self.canvas.create_text(self.margin, self.canvasHeight/2.3, anchor="nw",
			text=commandText)
		self.canvas.create_text(self.margin, self.canvasHeight*(2/3.0),
			anchor="nw", text=menuDescription)

	def redrawAll(self):
		self.canvas.create_rectangle(0, 0, self.canvasWidth, self.margin, 
			fill="lightBlue")
		self.canvas.create_rectangle(0, self.canvasHeight-self.margin, 
			self.canvasWidth, self.canvasHeight, fill="lightBlue")
		self.drawTitle()
		if(not self.help):
			self.Workspace1.drawWorkspace(self.canvas, 0, self.margin, 
				self.canvasWidth, self.canvasHeight-self.margin, self.mouseX, 
					self.mouseY)
			self.drawOperationText()
		else:
			self.drawHelp()