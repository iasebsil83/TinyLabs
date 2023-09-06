#!/usr/bin/python3






# -------- IMPORTATIONS --------

#system
import os, sys
SRC_DIR = os.path.dirname(os.getcwd())
if SRC_DIR not in sys.path:
	sys.path.append(SRC_DIR)

#tools
from tools.general           import *
from tools.status            import *
from tools.check_contents    import *
from tools.create_new_action import *





# -------- EXECUTION --------

#main
def tinylabs_action(args):

	# INITIALIZATION

	#define possible services
	SERVICE__CHECK_CFG  = 0
	SERVICE__EDIT_CFG   = 1
	SERVICE__CHECK_INT  = 2
	SERVICE__NEW_ACTION = 3
	SERVICE__GET_STATUS = 4

	#options
	service = SERVICE__GET_STATUS



	# PARSING

	#for each argument
	indexes_to_remove = []
	for a in range(len(args)):

		#option detected
		if args[a][0] == '-': # (args can't contain empty strings)

			#help menu
			if args[a] in ("-h", "--help"):
				print("Usage: tinylabs action [options] <lab> <action_path>")
				print("Deploy & manage actions of your labs as you want.")
				print()
				print("Options:")
				print("  -c, --check-cfg  : Check action configuration (common to the whole project).")
				print("  -e, --edit-cfg   : Edit action configuration (common to the whole project).")
				print("  -h, --help       : Show this help menu.")
				print("  -i, --check-int  : Check action integrity (fs structure + content).")
				print("  -n, --new        : Create a new action.")
				print("  -s, --status     : Get action status.")
				print("                     If no option is given, this one is set.")
				print()
				print("WARNING: <action_path> must be RELATIVE from the lab root directory.")
				print()
				print("NOTE: The <lab> argument can be given either by path or URL.")
				print()
				exit(0)

			#option : check action config
			elif args[a] in ("-c", "--check-cfg"):
				service = SERVICE__CHECK_CFG

				#remove from arguments
				indexes_to_remove.append(a)

			#option : edit action config
			elif args[a] in ("-e", "--edit-cfg"):
				service = SERVICE__EDIT_CFG

				#remove from arguments
				indexes_to_remove.append(a)

			#option : check action integrity
			elif args[a] in ("-i", "--check-int"):
				service = SERVICE__CHECK_INT

				#remove from arguments
				indexes_to_remove.append(a)

			#option : create new action
			elif args[a] in ("-n", "--new"):
				service = SERVICE__NEW_ACTION

				#remove from arguments
				indexes_to_remove.append(a)

			#option : get action status
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
		Err_fatal("Missing action path.")
	lab          = args[0]
	action_path  = args[1]
	project_path = os.path.dirname(os.path.dirname( action_path ))



	# DISTRIBUTE TO CORRECT SERVICE

	#case 1 : check config
	if service == SERVICE__CHECK_CFG:
		checkSettings(lab, MODE__ACTION, project_path + "/actions/settings.cfg")

	#case 2 : edit config
	elif service == SERVICE__EDIT_CFG:
		if isPath(lab):
			edit(lab + '/' + project_path + "/actions/settings.cfg")
			return

		#URL
		Err_fatal("URL request for editing action settings has not been implemented yet.")

	#case 3 : create new action
	elif service == SERVICE__NEW_ACTION:
		createNewAction(lab, action_path)

	#case 4 : check action integrity
	elif service == SERVICE__CHECK_INT:
		checkIntegrity(lab, MODE__ACTION, action_path)

	#case 5 : get status
	elif service == SERVICE__GET_STATUS:
		printStatus(lab, MODE__ACTION, action_path)

	#end of execution
	exit(0)
