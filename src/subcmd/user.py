#!/usr/bin/python3






# -------- IMPORTATIONS --------

#system
import os, sys
SRC_DIR = os.path.dirname(os.getcwd())
if SRC_DIR not in sys.path:
	sys.path.append(SRC_DIR)

#tools
from tools.general         import *
from tools.status          import *
from tools.check_contents  import *
from tools.create_new_user import *





# -------- EXECUTION --------

#main
def tinylabs_user(args):

	# INITIALIZATION

	#define possible services
	SERVICE__CHECK_CFG  = 0
	SERVICE__EDIT_CFG   = 1
	SERVICE__CHECK_INT  = 2
	SERVICE__NEW_USER   = 3
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
				print("Usage: tinylabs user [options] <lab> <user_idname>")
				print("Manage users of your labs as you want.")
				print()
				print("Options:")
				print("  -c, --check-cfg  : Check user configuration.")
				print("  -e, --edit-cfg   : Edit user configuration.")
				print("  -h, --help       : Show this help menu.")
				print("  -i, --check-int  : Check user integrity (fs structure + content).")
				print("  -n, --new        : Create a new user.")
				print("  -s, --status     : Get user status.")
				print("                     If no option is given, this one is set.")
				print()
				print("NOTE: The <lab> argument can be given either by path or URL.")
				print()
				exit(0)

			#option : check user config
			elif args[a] in ("-c", "--check-cfg"):
				service = SERVICE__CHECK_CFG

				#remove from arguments
				indexes_to_remove.append(a)

			#option : edit user config
			elif args[a] in ("-e", "--edit-cfg"):
				service = SERVICE__EDIT_CFG

				#remove from arguments
				indexes_to_remove.append(a)

			#option : check user integrity
			elif args[a] in ("-i", "--check-int"):
				service = SERVICE__CHECK_INT

				#remove from arguments
				indexes_to_remove.append(a)

			#option : create new user
			elif args[a] in ("-n", "--new"):
				service = SERVICE__NEW_USER

				#remove from arguments
				indexes_to_remove.append(a)

			#option : get user status
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
		Err_fatal("Missing user idname.")
	lab          = args[0]
	user_idname  = args[1]



	# DISTRIBUTE TO CORRECT SERVICE

	#case 1 : check config
	if service == SERVICE__CHECK_CFG:
		checkSettings(lab, MODE__USER, "users/" + user_idname + "/settings.cfg")

	#case 2 : edit config
	elif service == SERVICE__EDIT_CFG:
		if isPath(lab):
			edit(lab + "/users/" + user_idname + "/settings.cfg")
			return

		#URL
		Err_fatal("URL request for editing user settings has not been implemented yet.")

	#case 3 : create new user
	elif service == SERVICE__NEW_USER:
		createNewUser(lab, user_idname)

	#case 4 : check user integrity
	elif service == SERVICE__CHECK_INT:
		checkIntegrity(lab, MODE__USER, use_idname)

	#case 5 : get status
	elif service == SERVICE__GET_STATUS:
		printStatus(lab, MODE__USER, user_idname)

	#end of execution
	exit(0)
