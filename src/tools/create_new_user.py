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

#create new user
def createNewUser(lab, user_idname):
	if isPath(lab):
		full_user_cfg_path = lab + "/users/" + user_idname + ".cfg"

		#check existence
		if os.path.exists(full_user_cfg_path):
			Err_fatal("Could not create user configuration at location '" + full_user_cfg_path + "', element already exists.")

		#check user name
		checkIDName(user_idname)

		#beginning message
		print("Starting creation of configuration for user '" + user_idname + "'...")

		#copy user template
		try:
			shutil.copytree(INSTALL_DIR + "/templates/default/user.cfg", full_user_cfg_path)
		except (IOError, IsADirectoryError, FileNotFoundError):
			Err_fatal("Error creating new user configuration (could not copy default template to destination).")

		#end message
		print("New user successfully created (configuration accessible at '" + full_user_cfg_path + "').")
		return

	#URL
	Err_fatal("URL request for user creation has not been implemented yet.")
