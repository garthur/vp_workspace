# VP Workspace Window
# path checks to make sure the installation is safe

import os
import sys

PROJDIR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJDIR_PATH)

PACKAGEDIR_PATH = os.path.dirname(PROJDIR_PATH)

def checkAllFiles():

	def checkProjectFolder():
		# top level file check
		print "Checking project directory..."
		assert(os.path.exists(PROJDIR_PATH+os.sep+"settings.txt"))
		assert(os.path.exists(PROJDIR_PATH+os.sep+"__init__.py"))
		assert(os.path.exists(PROJDIR_PATH+os.sep+"VPWorkspaceWindow.py"))

	def checkAssetsFolder():
		# crawl the assets folder for the help text files
		# eventually, image files will be placed here for logos etc.
		print ">>> Checking assets folder...",
		addonToPath = PROJDIR_PATH+os.sep+"assets"+os.sep
		allHelpPaths = ["genHelp.txt", "vectorHelp.txt", "polyHelp.txt",
			"matrixHelp.txt"]
		assert(all([os.path.exists(addonToPath+helpPath)
			for helpPath in allHelpPaths]))
		print "Passed"

	def checkGraphicsFolder():
		# crawl the graphics folder for the graphics startup files
 		# these files are taken directly from CMU 15-112
 		print ">>> Checking graphics folder...",
		addonToPath = PROJDIR_PATH+os.sep+"graphics"+os.sep
		graphicsPaths = ["eventBasedAnimationClass.py"]
 		assert(all([os.path.exists(addonToPath+graphicsPath) 
 			for graphicsPath in graphicsPaths]))
 		print "Passed"

	def checkSourceFolder():
		# crawl the source folder for the backend class files
		# that I wrote to implement some data types
		print ">>> Checking source folder...",
		addonToPath = PROJDIR_PATH+os.sep+"source"+os.sep
		assert(os.path.exists(addonToPath+"__init__.py"))
		sourcePaths = ["matrixClass.py", "polynomialClass.py",
			"vectorClass.py"]
		assert(all([os.path.exists(addonToPath+sourcePath)
			for sourcePath in sourcePaths]))
		print "Passed"

	def checkTestFolder():
		print ">>> Checking test folder...",
		addonToPath = PROJDIR_PATH+os.sep+"text"+os.sep
		print "Passed"
		pass

	readmePath, tkinterColorChartPath = "README.md", "tkinterColorChart.png"
	docsPath, licensePath = "docs", "LICENSE"
	print "Checking package directory...",
	assert(os.path.exists(PACKAGEDIR_PATH+os.sep+docsPath))
	assert(os.path.exists(PACKAGEDIR_PATH+os.sep+licensePath))
	assert(os.path.exists(PACKAGEDIR_PATH+os.sep+readmePath))
	assert(os.path.exists(PACKAGEDIR_PATH+os.sep+tkinterColorChartPath))
	assert(os.path.exists(PROJDIR_PATH))
	print "Passed"

	checkProjectFolder()
	checkAssetsFolder()
	checkGraphicsFolder()
	checkSourceFolder()
	checkTestFolder()
	print "All files present."