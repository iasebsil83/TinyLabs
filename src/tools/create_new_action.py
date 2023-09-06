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

#create new action
def createNewAction(lab, action_path):
	if isPath(lab):
		action_name      = os.path.basename(action_path)
		full_action_path = lab + '/' + action_path

		#check existence
		if os.path.exists(full_action_path):
			Err_fatal("Could not create action at location '" + full_action_path + "', element already exists.")

		#check action name
		checkIDName(action_name)

		#beginning message
		print("Starting action creation at '" + full_action_path + "'...")

		#copy action template
		try:
			shutil.copytree(INSTALL_DIR + "/templates/default/action", full_action_path)
		except (IOError, IsADirectoryError, FileNotFoundError):
			Err_fatal("Error creating new action (could not copy default template to destination).")

		#end message
		print("New action successfully created at '" + full_action_path + "'.")
		return

	#URL
	Err_fatal("URL request for action creation has not been implemented yet.")
