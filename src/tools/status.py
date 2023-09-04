#!/usr/bin/python3






# -------- IMPORTATIONS --------

#system
import sys, os
SRC_DIR = os.path.dirname(os.getcwd())
if SRC_DIR not in sys.path:
	sys.path.append(SRC_DIR)

#tools
from tools.general import *






# -------- STATUS --------

#status check
def getStatus(lab, mode, relative_path):

	# CASE 1: GENERAL
	if mode == MODE__GENERAL:
		if isPath(lab):

			#read description file
			try:
				open(lab + "/description.txt", "r")
			except (IOError, FileNotFoundError, PermissionError, IsADirectoryError):
				return False
			return True

		#URL
		Err_runtime("URL request for getting lab status has not been implemented yet.")
		return False



	# CASE 2: SCHEDULER
	elif mode == MODE__SCHEDULER:
		if isPath(lab):

			#check activation flag
			if os.path.exists(lab + "/scheduler/.is_active"):
				print("Scheduler is active.")
				return True
			print("Scheduler is not active.")
			return False

		#URL
		Err_fatal("URL request for getting scheduler status has not been implemented yet.")
		return False



	# CASE 3: GROUP
	elif mode == MODE__GROUP:
		if isPath(lab):

			#check directory existence
			if os.path.isdir(lab + '/' + relative_path):
				return True
			return False

		#URL
		Err_fatal("URL request for getting group status has not been implemented yet.")
		return False



	# CASE 4: PROJECT
	elif mode == MODE__PROJECT:
		if isPath(lab):

			#check directory existence
			if os.path.isdir(lab + '/' + relative_path):
				return True
			return False

		#URL
		Err_fatal("URL request for getting project status has not been implemented yet.")
		return False



	# CASE 5: USER
	elif mode == MODE__USER:
		if isPath(lab):

			#check user config file existence
			if os.path.isdir(lab + "/users/" + relative_path + ".cfg"):
				return True
			return False

		#URL
		Err_fatal("URL request for getting user status has not been implemented yet.")
		return False



	# CASE 6: ACTION
	elif mode == MODE__ACTION:
		if isPath(lab):

			#check directory existence
			if os.path.isdir(lab + '/' + relative_path):
				return True
			return False

		#URL
		Err_fatal("URL request for getting action status has not been implemented yet.")
		return False



	# UNRECOGNIZED MODE
	else:
		Err_internal("Unknown mode '" + str(mode) + "' while trying to get status.")



#display
def printStatus(lab, mode, relative_path):

	# CASE 1: GENERAL
	if mode == MODE__GENERAL:
		if getStatus(lab, mode, relative_path):
			print("Lab found at '" + lab + "'.")

			#read description
			f = open(lab + "/description.txt", "r")
			content = f.read()
			f.close()

			#print it
			print("Description:")
			print(content)
		else:
			print("No lab found at '" + lab + "' (missing description file).")



	# CASE 2: SCHEDULER
	elif mode == MODE__SCHEDULER:
		if getStatus(lab, mode, relative_path):
			print("Scheduler is active.")
		else:
			print("Scheduler is not active.")



	# CASE 3: GROUP
	elif mode == MODE__GROUP:
		if getStatus(lab, mode, relative_path):
			print("Group directory exists.")
		else:
			print("Group directory not found on lab '" + lab + "'.")



	# CASE 4: PROJECT
	elif mode == MODE__PROJECT:
		if getStatus(lab, mode, relative_path):
			print("Project directory exists.")
		else:
			print("Project directory not found on lab '" + lab + "'.")



	# CASE 5: USER
	elif mode == MODE__USER:
		if getStatus(lab, mode, relative_path):
			print("User configuration file exists for '" + relative_path + "'.")
		else:
			print("No user configuration file found for '" + relative_path + "' in lab '" + lab + "'.")



	# CASE 6: ACTION
	elif mode == MODE__ACTION:
		if getStatus(lab, mode, relative_path):
			print("Action directory exists.")
		else:
			print("Action directory not found on lab '" + lab + "'.")



	# UNRECOGNIZED MODE
	else:
		Err_internal("Unknown mode '" + str(mode) + "' while trying to get status.")
