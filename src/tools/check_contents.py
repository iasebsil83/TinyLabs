#!/usr/bin/python3






# -------- IMPORTATIONS --------

#system
import sys, os
SRC_DIR = os.path.dirname(os.getcwd())
if SRC_DIR not in sys.path:
	sys.path.append(SRC_DIR)

#tools
import tools.config  as config
from   tools.general import *






# -------- SETTINGS --------

#settings.cfg files
def checkSettings(lab, mode, filename): #filename is RELATIVE to lab path (or URL)
	name        = os.path.basename( os.path.dirname(filename) )
	error_found = False

	#read content
	if isPath(lab):
		cfg = config.readFile(lab + '/' + filename)
	else:
		Err_fatal("URL request for reading distant settings files has not been implemented yet.")

	#for each cfg field
	for cfg_field in cfg.keys():



		# CASE 1: GENERAL
		if mode == MODE__GENERAL:

			#specific analysis
			if cfg_field == "URL_ACCESS":
				match = re.match("(NO|REQUIRE_TOKEN|OPEN)", cfg[cfg_field])
			#elif cfg_field == "":
			#	match = re.match("", cfg[cfg_field])
			#elif cfg_field == "":
			#	match = re.match("", cfg[cfg_field])
			#elif cfg_field == "":
			#	match = re.match("", cfg[cfg_field])

			#error case 1 : invalid field
			else:
				Err_runtime("Invalid config field '" + cfg_field + "' for general 'settings.cfg'.")
				error_found = True
				continue

			#error case 2 : invalid value
			if not match:
				Err_runtime("Field '" + cfg_field + "' in general 'settings.cfg' does not match allowed expression.")
				error_found = True



		# CASE 2: SCHEDULER
		if mode == MODE__SCHEDULER:

			#specific analysis
			if cfg_field == "DELAY_BETWEEN_CHECK":
				match = re.match("[0-9]{9}", cfg[cfg_field])
			elif cfg_field == "TRIGGER_NUMBER_MAX":
				match = re.match("[0-9]+", cfg[cfg_field])
			#elif cfg_field == "":
			#	match = re.match("", cfg[cfg_field])
			#elif cfg_field == "":
			#	match = re.match("", cfg[cfg_field])

			#error case 1 : invalid field
			else:
				Err_runtime("Invalid config field '" + cfg_field + "' for scheduler 'settings.cfg'.")
				error_found = True
				continue

			#error case 2 : invalid value
			if not match:
				Err_runtime("Field '" + cfg_field + "' in scheduler 'settings.cfg' does not match allowed expression.")
				error_found = True



		# CASE 3: GROUP
		if mode == MODE__GROUP:

			#error case 1 : invalid field
			if cfg_field not in listUsers(lab):
				Err_runtime("Invalid user IDName '" + cfg_field + "' in 'settings.cfg' of group '" + name + "'.")
				error_found = True
				continue

			#error case 2 : invalid value
			if cfg[cfg_field] not in GROUP_PERMISSIONS:
				Err_runtime("Unknown permission for user '" + cfg_field + "' of group '" + name + "' : '" + cfg[cfg_field] + "'.")
				error_found = True



		# CASE 4: PROJECT
		elif mode == MODE__PROJECT:

			#specific analysis
			if cfg_field == "NON_CONTRIBUTOR_PERMISSION":
				match = re.match("(" + '|'.join(PROJECT_PERMISSIONS) + ")", cfg[cfg_field])
			#elif cfg_field == "":
			#	match = re.match("", cfg[cfg_field])
			#elif cfg_field == "":
			#	match = re.match("", cfg[cfg_field])
			#elif cfg_field == "":
			#	match = re.match("", cfg[cfg_field])

			#error case 1 : invalid field
			else:
				Err_runtime("Invalid config field ' + cfg_field + ' for project '" + name + "'.")
				error_found = True
				continue

			#error case 2 : invalid value
			if not match:
				Err_runtime("Field '" + cfg_field + "' for project '" + name + "' does not match allowed expression.")
				error_found = True



		# CASE 5: USER
		elif mode == MODE__USER:

			#specific analysis
			if cfg_field == "DEFAULT_PAGE":
				match = re.match("(OVERVIEW|GROUPS|PROJECTS)", cfg[cfg_field])
			#elif cfg_field == "":
			#	match = re.match("", cfg[cfg_field])
			#elif cfg_field == "":
			#	match = re.match("", cfg[cfg_field])
			#elif cfg_field == "":
			#	match = re.match("", cfg[cfg_field])

			#error case 1 : invalid field
			else:
				Err_runtime("Invalid config field ' + cfg_field + ' for user '" + name + "'.")
				error_found = True
				continue

			#error case 2 : invalid value
			if not match:
				Err_runtime("Field '" + cfg_field + "' for user '" + name + "' does not match allowed expression.")
				error_found = True



		# CASE 6: ACTION
		elif mode == MODE__ACTION:
			project_path = os.path.dirname(os.path.dirname(filename))
			project_name = os.path.basename(project_path)

			#error case 1 : invalid field
			if cfg_field not in listActions(lab, project_path):
				Err_runtime("Invalid action IDName '" + cfg_field + "' in action settings of project '" + project_name + "'.")
				error_found = True
				continue

			#error case 2 : invalid value
			if not re.match("(MANUAL|EVERY[0-9]{9}|EACH[0-9]{9}|ANY_PUSH|TAG_PUSH.+)", cfg[cfg_field]):
				Err_runtime("Invalid trigger pattern for action '" + cfg_field + "' in project '" + project_name + "'.")
				error_found = True



		# UNRECOGNIZED MODE
		else:
			Err_internal("Unknown mode '" + str(mode) + "' in settings check.")

	#errors found
	if error_found:
		Err_fatal("Errors found in config file '" + filename + "', stopping here.")






# -------- ALL --------

#complete check
def checkIntegrity(lab, mode, relative_path):

	#path address
	if isPath(lab):
		IS_DIR  = True
		IS_FILE = False



		# CASE 1: GENERAL
		if mode == MODE__GENERAL:
			first_incorrect_fse = checkFSEList([
				(IS_DIR,  lab),
				(IS_FILE, lab + "/settings.cfg"),
				(IS_FILE, lab + "/icon.png"),
				(IS_FILE, lab + "/description.txt"),
				(IS_FILE, lab + "/tokens.cfg")
			])
			if first_incorrect_fse:
				Err_fatal("Missing element '" + first_incorrect_fse + "' in lab.")

			#check content
			checkSettings(lab, mode, "settings.cfg")



		# CASE 2: SCHEDULER
		if mode in (MODE__SCHEDULER, MODE__GENERAL):
			first_incorrect_fse = checkFSEList([
				(ID_DIR,  lab + "/scheduler"),
				(IS_FILE, lab + "/scheduler/settings.cfg"),
				(IS_DIR,  lab + "/scheduler/triggers")
			])
			if first_incorrect_fse:
				Err_fatal("Missing element '" + first_incorrect_fse + "' in scheduler.")

			#check content
			checkSettings(lab, mode, "scheduler/settings.cfg")



		# CASE 3: GROUP
		if mode in (MODE__GROUP, MODE__GENERAL):

			#path given => local interaction
			if relative_path:
				if not os.path.isdir(lab + "/projects"):
					Err_fatal("Missing projects/ directory in lab.")

				#check files existence
				first_incorrect_fse = checkFSEList([
					(IS_DIR,  lab + '/' + relative_path),
					(IS_FILE, lab + '/' + relative_path + "/settings.cfg")
				])
				if first_incorrect_fse:
					Err_fatal("Missing element '" + first_incorrect_fse + "' in group.")

				#check content
				checkSettings(lab, mode, relative_path + "/settings.cfg")

			#no path given => general interaction
			else:
				Err_runtime("Could not check integrity of all groups for the moment, skipping them.")



		# CASE 4: PROJECT
		if mode in (MODE__PROJECT, MODE__GENERAL):

			#path given => local interaction
			if relative_path:
				if not os.path.isdir(lab + "/projects"):
					Err_fatal("Missing projects/ directory in lab.")

				#check files existence
				first_incorrect_fse = checkFSEList([
					(IS_DIR,  lab + '/' + relative_path),
					(IS_FILE, lab + '/' + relative_path + "/settings.cfg"),
					(IS_FILE, lab + '/' + relative_path + "/contributors.cfg"),
					(IS_DIR,  lab + '/' + relative_path + "/repository"),
					(IS_DIR,  lab + '/' + relative_path + "/actions"),
					(IS_FILE, lab + '/' + relative_path + "/icon.png")
				])
				if first_incorrect_fse:
					Err_fatal("Missing element '" + first_incorrect_fse + "' in project.")

				#check content
				checkSettings(lab, mode, relative_path + "/settings.cfg")

			#no path given => general interaction
			else:
				Err_runtime("Could not check integrity of all projects for the moment, skipping them.")



		# CASE 5: USER
		if mode in (MODE__USER, MODE__GENERAL):
			if not os.path.isdir(lab + "/users"):
				Err_fatal("Missing users/ directory in lab.")

			#path given => local interaction
			if relative_path:

				#check files existence
				first_incorrect_fse = checkFSEList([
					(IS_FILE, lab + "/users/" + relative_path + "/settings.cfg"),
					(IS_FILE, lab + "/users/" + relative_path + "/icon.png")
				])
				if first_incorrect_fse:
					Err_fatal("Missing element '" + first_incorrect_fse + "' concerning user '" + relative_path + "'.")

				#check content
				checkSettings(lab, mode, "users/" + relative_path + "/settings.cfg")

			#no path given => general interaction
			else:

				#for each user
				users_error = False
				user_list   = listUsers(lab)
				for user in user_list:

					#check files existence
					first_incorrect_fse = checkFSEList([
						(IS_FILE, lab + "/users/" + user + "/settings.cfg"),
						(IS_FILE, lab + "/users/" + user + "/icon.png")
					])
					if first_incorrect_fse:
						Err_runtime("Missing element '" + first_incorrect_fse + "' concerning user '" + user + "'.")
						users_error = True

					#check content
					checkSettings(lab, mode, "users/" + user + "/settings.cfg")

				#error(s) occured before
				if users_error:
					Err_fatal("Problem(s) occured checking every user's integrity, not going further.")



		# CASE 6: ACTION
		if mode in (MODE__ACTION, MODE__GENERAL):

			#path given => local interaction
			if relative_path:
				if not os.path.isdir(lab + "/projects"):
					Err_fatal("Missing projects/ directory in lab.")

				#get some paths
				actions_dir  = os.path.dirname(relative_path)
				project_dir  = os.path.dirname(actions_dir)
				project_name = os.path.basename(project_dir)

				#check files existence
				first_incorrect_fse = checkFSEList([
					(IS_DIR,  lab + '/' + actions_dir),
					(IS_FILE, lab + '/' + project_dir + "/settings.cfg"),
					(IS_DIR,  lab + '/' + relative_path),
					(IS_FILE, lab + '/' + relative_path + "/run.sh")
				])
				if first_incorrect_fse:
					Err_runtime("Missing element '" + first_incorrect_fse + "' in actions of project '" + project_name + "'.")

				#check content
				checkSettings(lab, mode, actions_dir + "/settings.cfg")

			#no path given => general interaction
			else:
				Err_runtime("Could not check integrity of all actions for the moment, skipping them.")



		# UNRECOGNIZED MODE
		else:
			Err_internal("Unknown mode '" + str(mode) + "' in integrity check.")

		#no problem detected
		print("Lab integrity is OK.")

	#URL address
	Err_fatal("URL status check has not been implemented yet.")
