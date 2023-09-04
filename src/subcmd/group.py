#!/usr/bin/python3






# -------- IMPORTATIONS --------

#system
import os, sys
SRC_DIR = os.path.dirname(os.getcwd())
if SRC_DIR not in sys.path:
	sys.path.append(SRC_DIR)

#tools
from tools.general          import *
from tools.status           import *
from tools.check_contents   import *
from tools.create_new_group import *





# -------- EXECUTION --------

#main
def tinylabs_group(args):

	# INITIALIZATION

	#define possible services
	SERVICE__CHECK_CFG  = 0
	SERVICE__EDIT_CFG   = 1
	SERVICE__CHECK_INT  = 2
	SERVICE__NEW_GROUP  = 3
	SERVICE__GET_STATUS = 4

	#options
	service = SERVICE__GET_STATUS



	# PARSING

	#for each argument
	indexes_to_remove = []
	args = args[1:]
	for a in range(len(args)):

		#option detected
		if args[a][0] == '-': # (args can't contain empty strings)

			#help menu
			if args[a] in ("-h", "--help"):
				print("Usage: tinylabs group [options] <lab> <group_path>")
				print("Deploy & manage groups in your labs as you want.")
				print()
				print("Options:")
				print("  -c, --check-cfg  : Check group configuration.")
				print("  -e, --edit-cfg   : Edit group configuration.")
				print("  -h, --help       : Show this help menu.")
				print("  -i, --check-int  : Check group integrity (fs structure + content).")
				print("  -n, --new        : Create a new group.")
				print("  -s, --status     : Get group status.")
				print("                     If no option is given, this one is set.")
				print()
				print("WARNING: <group_path> must be RELATIVE from the lab root directory.")
				print()
				print("NOTE: The <lab> argument can be given either by path or URL.")
				print()
				exit(0)

			#option : check group config
			elif args[a] in ("-c", "--check-cfg"):
				service = SERVICE__CHECK_CFG

				#remove from arguments
				indexes_to_remove.append(a)

			#option : edit group config
			elif args[a] in ("-e", "--edit-cfg"):
				service = SERVICE__EDIT_CFG

				#remove from arguments
				indexes_to_remove.append(a)

			#option : check group integrity
			elif args[a] in ("-i", "--check-int"):
				service = SERVICE__CHECK_INT

				#remove from arguments
				indexes_to_remove.append(a)

			#option : create new group
			elif args[a] in ("-n", "--new"):
				service = SERVICE__NEW_GROUP

				#remove from arguments
				indexes_to_remove.append(a)

			#option : get group status
			elif args[a] in ("-s", "--status"):
				service = SERVICE__GET_STATUS

				#remove from arguments
				indexes_to_remove.append(a)

			#undefined option
			else:
				Err_fatal("Unknown option '" + args[a] + "'.")

	#update argument list
	args = Lst_removeAll(args, indexes_to_remove)

	#no arguments left
	if len(args) == 0:
		Err_fatal("Missing lab path or URL.")
	if len(args) == 1:
		Err_fatal("Missing group path.")
	lab        = args[0]
	group_path = args[1]



	# DISTRIBUTE TO CORRECT SERVICE

	#case 1 : check config
	if service == SERVICE__CHECK_CFG:
		checkSettings(lab, MODE__GROUP, group_path + "/settings.cfg")

	#case 2 : edit config
	elif service == SERVICE__EDIT_CFG:
		if isPath(lab):
			edit(lab + '/' + group_path + "/settings.cfg")
			return

		#URL
		Err_fatal("URL request for editing group settings has not been implemented yet.")

	#case 3 : create new group
	elif service == SERVICE__NEW_GROUP:
		createNewGroup(lab, group_path)

	#case 4 : check group integrity
	elif service == SERVICE__CHECK_INT:
		checkIntegrity(lab, MODE__GROUP, group_path)

	#case 5 : get status
	elif service == SERVICE__GET_STATUS:
		printStatus(lab, MODE__GROUP, group_path)

	#end of execution
	exit(0)
