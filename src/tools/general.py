#!/usr/bin/python3






# -------- IMPORTATIONS --------

#system
import sys
sys.path.append(".")

#tools
import config






# -------- DECLARATIONS --------

#installation directory
INSTALL_DIR = "/opt/TinyLabs"

#default editor
DEFAULT_EDITOR = "/usr/bin/nano" #"/usr/bin/vi"

#IDName characters allowed
IDNAME_ALLOWED_CHARACTERS = string.ascii_letters + "-_"

#permissions
GROUP_PERMISSIONS   = ("VIEW",  "ORGANIZE", "CONFIGURE") #sorted from the least permissive to the most one
PROJECT_PERMISSIONS = ("CLONE", "SUGGEST",  "PUSH"     )

#settings modes
MODE__GENERAL   = 0
MODE__SCHEDULER = 1
MODE__GROUP     = 2
MODE__PROJECT   = 3
MODE__USER      = 4
MODE__ACTION    = 5






# -------- STD TOOLS --------

#remove every indexes in given list
def Lst_removeAll(l, to_remove):
	result = []
	for i in range(len(l)):
		if i not in to_remove:
			result.append(l[i])
	return result

#any error
def Err_raise(prefix, msg):
	sys.stderr.write(prefix + " ERROR > " + msg + "\n")

#runtime error
def Err_runtime(msg):
	Err_raise("RUNTIME", msg)

#fatal error
def Err_fatal(msg, err_code=1):
	Err_raise("FATAL", msg)
	exit(err_code)

#internal
def Err_internal(msg):
	Err_raise("INTERNAL", msg)
	exit(255)

#filename without extension
def Path_name(path):
	if '.' in path:
		return '.'.join( path.split('.')[:-1] )
	return path






# -------- GENERIC --------

#FSE
def checkFSEList(fse_list):
	IS_DIR = 0
	NAME   = 1

	#for each fse
	for fse in fse_list:

		#this one MUST BE a directory
		if fse[IS_DIR]:
			if not os.path.isdir(fse[NAME]):
				return fse[NAME]

		#this one MUST BE a file
		else:
			if not os.path.isfile(fse[NAME]):
				return fse[NAME]

	#nothing abnormal => nothing to return
	return None #(yes I know, not required)

def listOnlyDirs(path):
	result = []
	for fse in os.listdir(path):
		if os.path.isdir(path):
			result.append(os.path.basename(fse))
	return result



#edit a file
def edit(path):
	editor_path = DEFAULT_EDITOR_PATH
	if "EDITOR" in os.environ.keys():
		editor_path = os.environ["EDITOR"]

	#edit file
	err = os.system(editor_path + ' ' + path)
	if err:
		Err_fatal("Unable to start editor '" + editor_path + "' with file '" + path + "'.")






# -------- SPECIFIC --------

#format
def checkIDName(name):
	for c in name:
		if c not in IDNAME_ALLOWED_CHARACTERS:
			return False
	return True



#path / URL
def isPath(lab):

	#absolute path
	if lab[0] == '/':
		return True

	#http/https/ssh protocols allowed
	try:
		protocol = lab.index(':')
		if protocol in ("http", "https", "ssh"):
			return False

		#unrecognized protocol
		Err_fatal("Unrecognized protocol '" + protocol + "'.")

	#relative path
	return True

def onlyPath(lab):
	if not isPath(lab):
		Err_fatal("This service requires lab access by path only (no URL).")



#listing elements
def listUsers(lab):

	#path address
	if isPath(lab):
		return listOnlyDirs(lab + "/users")

	#URL address
	Err_fatal("URL request for getting user list has not been implemented yet.")

def listActions(lab, project_path):

	#path address
	if isPath(lab):
		return listOnlyDirs(lab + '/' + project_path + "/actions")

	#URL address
	Err_fatal("URL request for getting action list has not been implemented yet.")



#status
def checkStatus(lab):

	#path address
	if isPath(lab):
		if not os.path.isfile(lab + "/description.txt"): #access to description.txt is enough for a simple status check
			Err_fatal("Unable to get lab status.")

	#URL address
	Err_fatal("URL request for checking status has not been implemented yet")

def getStatus(lab):

	#path address
	if isPath(lab):

		#read description file
		try:
			f = open(lab + "/description.txt", "r")
			content = f.read()
			f.close()
		except (IOError, FileNotFoundError, PermissionError, IsADirectoryError):
			Err_fatal("Unable to access to lab description.")

		#print it
		print("Description:")
		print(content)

	#URL address
	Err_fatal("URL request for getting status hase not been implemented yet.")
