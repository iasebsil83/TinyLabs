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

#create new group
def createNewGroup(lab, group_path):
	if isPath(lab):
		group_name      = os.path.basename(group_path)
		full_group_path = lab + '/' + group_path

		#check existence
		if os.path.exists(full_group_path):
			Err_fatal("Could not create group at location '" + full_group_path + "', element already exists.")

		#check group name
		checkIDName(group_name)

		#beginning message
		print("Starting group creation at '" + full_group_path + "'...")

		#copy group template
		try:
			shutil.copytree(INSTALL_DIR + "/templates/default/group", full_group_path)
		except (IOError, IsADirectoryError, FileNotFoundError):
			Err_fatal("Error creating new group (could not copy default template to destination).")

		#end message
		print("New group successfully created at '" + full_group_path + "'.")
		return

	#URL
	Err_fatal("URL request for group creation has not been implemented yet.")
