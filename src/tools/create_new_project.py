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

		#copy project template
		try:
			shutil.copytree(INSTALL_DIR + "/templates/default/project", full_project_path)
		except (IOError, IsADirectoryError, FileNotFoundError):
			Err_fatal("Error creating new project (could not copy default template to destination).")

		#replace action #PATH# in template
		f = open(full_project_path + "/actions/settings.cfg", "r")
		content = f.read()
		f.close()
		content = content.replace("#PATH#", project_path + "/actions")
		f = open(full_project_path + "/actions/settings.cfg", "w")
		f.write(content)
		f.close()

		#find name for symlink to scheduler trigger (step 1: get the list of existing numbers)
		new_number = 0
		numbers_taken = []
		for fse in os.path.listdir(lab + "/scheduler/triggers"):
			if os.path.isfile(fse) and Path_extension(fse) == "cfg" and isHexName(fse):
				numbers_taken.append( int(Path_name(fse), 16) )

		#find name for symlink to scheduler trigger (step 2: count until the greatest one)
		if len(numbers_taken) != 0:
			numbers_taken.sort()
			new_number = -1
			for n in range(numbers_taken[-1]+1):
				if n not in numbers_taken: #if one is missing : TAKING IT !
					new_number = n
					break

			#find name for symlink to scheduler trigger (step 3: if no missing number found, take the next value)
			if new_number == -1:
				new_number = numbers_taken[-1] + 1

		#create symlink for scheduler trigger
		if os.symlink(full_project_path + "/actions/settings.cfg", lab + "/scheduler/triggers/" + hex(new_number)[2:] + ".cfg"):
			Err_fatal("Unable to create symbolic link for scheduler triggering.")

		#end message
		print("New project successfully created at '" + full_project_path + "'.")
		return

	#URL
	Err_fatal("URL request for project creation has not been implemented yet.")
