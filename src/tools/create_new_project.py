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

#create new project
def createNewProject(lab, project_path):
	if isPath(lab):
		project_name      = os.path.basename(project_path)
		full_project_path = lab + '/' + project_path

		#check existence
		if os.path.exists(full_project_path):
			Err_fatal("Could not create project at location '" + full_project_path + "', element already exists.")

		#check project name
		checkIDName(project_name)

		#beginning message
		print("Starting project creation at '" + full_project_path + "'...")

		#copy lab template
		if shutil.copy2(INSTALL_DIR + "/templates/default/project", full_project_path):
			Err_fatal("Error creating new project (could not copy default template to destination).")

		#end message
		print("New project successfully created at '" + full_project_path + "'.")
		return

	#URL
	Err_fatal("URL request for project creation has not been implemented yet.")
