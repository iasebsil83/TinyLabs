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
from ... import *





# -------- EXECUTION --------

#main
def tinylabs_cui(args):

	# PARSING

	#for each argument
	indexes_to_remove = []
	for a in range(len(args)):

		#option detected
		if args[a][0] == '-': # (args can't contain empty strings)

			#help menu
			if args[a] in ("-h", "--help"):
				print("Usage: tinylabs cui [options] <lab>")
				print("Launch a Console User Interface concerning given lab.")
				print()
				print("Options:")
				print("  -h, --help : Show this help menu.")
				print()
				print("NOTE: The <lab> argument can be given either by path or URL.")
				print()
				exit(0)

			#undefined option
			else:
				Err_fatal("Unknown option '" + args[a] + "'.")

	#update argument list
	args = Lst_removeAll(args, indexes_to_remove)

	#no arguments left
	if len(args) == 0:
		Err_fatal("Missing lab path or URL.")
	lab = args[0]



	# RUN CUI

	#run CUI
	print("CUI for lab '" + lab + "' launched.")
	print("CUI for lab '" + lab + "' terminated.")

	#end of execution
	exit(0)
