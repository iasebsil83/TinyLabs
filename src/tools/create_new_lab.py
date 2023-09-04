#!/usr/bin/python3




# -------- IMPORTATIONS --------

#system
import sys, os, sys
SRC_DIR = os.path.dirname(os.getcwd())
if SRC_DIR not in sys.path:
	sys.path.append(SRC_DIR)

#tools
from tools.general import *






# -------- FUNCTIONS --------

#create new lab
def createNewLab(lab):
	if isPath(lab):

		#check existence
		if os.path.exists(lab):
			Err_fatal("Could not create lab at location '" + lab + "', element already exists.")

		#check lab name
		if not checkIDName(lab):
			Err_fatal("Could not continue, stopping lab creation.")

		#beginning message
		print("Starting lab creation at '" + lab + "'...")

		#copy lab template
		if shutil.copy2(INSTALL_DIR + "/templates/default/lab", lab):
			Err_fatal("Error creating new lab (could not copy default template to destination).")

		#end message
		print("New lab successfully created at '" + lab + "'.")
		return

	#URL
	Err_fatal("URL request for creating a new lab has not been implemented yet.")
