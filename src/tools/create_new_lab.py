#!/usr/bin/python3




# -------- IMPORTATIONS --------

#system
import sys, os, shutil
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
		checkIDName(os.path.basename(lab))

		#beginning message
		print("Starting lab creation at '" + lab + "'...")

		#copy lab template
		try:
			shutil.copytree(INSTALL_DIR + "/templates/default/lab", lab)
		except (IOError, IsADirectoryError, FileNotFoundError):
			Err_fatal("Error creating new lab (could not copy default template to destination).")

		#end message
		print("New lab successfully created at '" + lab + "'.")
		return

	#URL
	Err_fatal("URL request for creating a new lab has not been implemented yet.")
