#!/usr/bin/python3




# -------- IMPORTATIONS --------

#system
import os, sys
sys.path.append(".")

#tools
import config
from general import *






# -------- FUNCTIONS --------

#create new lab
def createNewLab(lab):
	onlyPath(lab)

	#check existence
	if os.path.exists(lab):
		Err_fatal("Could not create lab at location '" + lab + "', element already exists.")

	#check filename
	checkIDName(lab)

	#beginning message
	print("Creating a new lab at '" + lab + "'...")

	#create directories
	if shutil.copy2(INSTALL_DIR + "/templates/empty_lab", lab):
		Err_fatal("Error creating new lab (could not copy default template to destination).")

	#end message
	print("New lab successfully created at '" + lab + "'.")
