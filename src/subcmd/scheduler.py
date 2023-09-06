#!/usr/bin/python3






# -------- IMPORTATIONS --------

#system
import os, sys
SRC_DIR = os.path.dirname(os.getcwd())
if SRC_DIR not in sys.path:
	sys.path.append(SRC_DIR)

#delay
from time import sleep

#tools
import tools.config         as config
from   tools.general        import *
from   tools.status         import *
from   tools.dateFormat     import *
from   tools.check_contents import *





# -------- ACTIVATION --------

#activate - deactivate
def scheduler_activate(lab):
	if isPath(lab):

		#check scheduler status before
		if getStatus(lab, MODE__SCHEDULER, None):
			Err_fatal("Scheduler is already active.")

		#activate scheduler
		scheduler_cfg = config.read(lab + "/scheduler/.is_active")
		print("Activated scheduler.")
		print("    Checking lab actions with periods of " + dateFormat_toPrintable(scheduler_cfg["DELAY_BETWEEN_CHECK"]) + '.')

		#for the moment, stuck execution here <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< TEMPORARY
		while os.path.exists(lab + "scheduler/.is_active"):
			scheduler_run(lab)
			sleep(scheduler_cfg["DELAY_BETWEEN_CHECK"])

		#set activation flag (empty file)
		open(lab + "/scheduler/.is_active", 'w')
		return

	#URL
	Err_fatal("URL request for activating scheduler has not been implemented yet.")

def scheduler_deactivate(lab):
	if isPath(lab):

		#check scheduler status
		if not getStatus(lab, MODE__SCHEDULER, None):
			Err_fatal("Scheduler is not active.")

		#deactivate scheduler
		print("Deactivated scheduler.")

		#reset activation flag (remove file)
		if os.path.remove(lab + "/scheduler/.is_active"):
			Err_fatal("Unable to remove activation flag file at '" + lab + "/scheduler/.is_active'.")
		return

	#URL
	Err_fatal("URL request for deactivating scheduler has not been implemented yet.")






# -------- EXECUTION --------

#scheduler execution <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< TEMPORARILY HERE
def scheduler_run(lab):
	PWD = os.getcwd()

	#for each trigger file
	for fse in os.path.listdir(lab + "/scheduler/triggers"):

		#criteria for being a triggerable by scheduler
		if os.path.isfile(fse) and Path_extension(fse) == "cfg" and hasHexName(fse):
			cfg = config.read(fse)

			#get into targetted directory
			if os.chdir( cfg["path"] ):
				Err_runtime("[Scheduler] Could not get into directory '" + cfg["path"] + "'.")
				continue

			#for each action found (we must be in ".../actions" until now)
			cfg.pop("path")
			for action in cfg.keys():
				err_before = os.system("echo '[$(date)] Action begin.' " + action + "/out.log")
				err        = os.system(action + "/run.sh > " + action + "/out.log 2> " + action + "/err.log")
				err_after  = os.system("echo '[$(date)] Action ended.' > " + action + "/out.log")

				#small errors
				if err_before:
					Err_runtime("[Scheduler] Unable to write beginning message to action '" + action + "'.")
				if err_after:
					Err_runtime("[Scheduler] Unable to write end message to action '" + action + "'.")

				#write also return code
				f = open(action + "/err.code", "w")
				f.write(str(err))
				f.close()

			#get back to previous location in case paths are relative (they should NOT but anyway)
			if os.chdir(PWD):
				Err_runtime("[Scheduler] Unable to get back to previous location.")



#main
def tinylabs_scheduler(args):

	# INITIALIZATION

	#define possible services
	SERVICE__ACTIVATE    = 0
	SERVICE__CHECK_CFG   = 1
	SERVICE__DEACTIVATE  = 2
	SERVICE__EDIT_CFG    = 3
	SERVICE__CHECK_INT   = 4
	SERVICE__GET_STATUS  = 5

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
				print("Usage: tinylabs scheduler [options] <lab>")
				print("Manage your lab's scheduler as you want.")
				print()
				print("Options:")
				print("  -a, --activate   : Activate scheduler.")
				print("  -c, --check-cfg  : Check scheduler configuration.")
				print("  -d, --deactivate : Deactivate scheduler.")
				print("  -e, --edit-cfg   : Edit scheduler configuration.")
				print("  -h, --help       : Show this help menu.")
				print("  -i, --check-int  : Check scheduler integrity (fs structure + content).")
				print("  -s, --status     : Get scheduler status.")
				print("                     If no option is given, this one is set.")
				print()
				print("NOTE: The <lab> argument can be given either by path or URL.")
				print()
				exit(0)

			#option : activate scheduler
			elif args[a] in ("-a", "--activate"):
				service = SERVICE__ACTIVATE

				#remove from arguments
				indexes_to_remove.append(a)

			#option : check scheduler config
			elif args[a] in ("-c", "--check-cfg"):
				service = SERVICE__CHECK_CFG

				#remove from arguments
				indexes_to_remove.append(a)

			#option : deactivate scheduler
			elif args[a] in ("-d", "--deactivate"):
				service = SERVICE__DEACTIVATE

				#remove from arguments
				indexes_to_remove.append(a)

			#option : edit scheduler config
			elif args[a] in ("-e", "--edit-cfg"):
				service = SERVICE__EDIT_CFG

				#remove from arguments
				indexes_to_remove.append(a)

			#option : check scheduler integrity
			elif args[a] in ("-i", "--check-int"):
				service = SERVICE__CHECK_INT

				#remove from arguments
				indexes_to_remove.append(a)

			#option : get scheduler status
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
	lab = args[0]



	# DISTRIBUTE TO CORRECT SERVICE

	#case 1 : activate scheduler
	if service == SERVICE__ACTIVATE:
		scheduler_activate(lab)

	#case 2 : check config
	if service == SERVICE__CHECK_CFG:
		checkSettings(lab, MODE__SCHEDULER, "/scheduler/settings.cfg")

	#case 3 : deactivate scheduler
	if service == SERVICE__DEACTIVATE:
		scheduler_deactivate(lab)

	#case 4 : edit config
	elif service == SERVICE__EDIT_CFG:
		if isPath(lab):
			edit(lab + "/scheduler/settings.cfg")
		else:
			Err_fatal("URL request for editing scheduler configuration has not been implemented yet.")

	#case 5 : check integrity
	elif service == SERVICE__CHECK_INT:
		checkIntegrity(lab, MODE__SCHEDULER, None)

	#case 6 : get status
	elif service == SERVICE__GET_STATUS:
		printStatus(lab, MODE__SCHEDULER, None)

	#end of execution
	exit(0)
