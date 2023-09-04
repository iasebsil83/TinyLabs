#!/usr/bin/python3






# -------- IMPORTATIONS --------

#system
import sys, os
SRC_DIR = os.path.dirname(os.getcwd())
if SRC_DIR not in sys.path:
	sys.path.append(SRC_DIR)






# -------- TOOLS --------

#display (format is DDDHHMMSS for Days, hours, minutes, seconds)
def dateFormat_toPrintable(date, short=False):
	if short:
		return date[0:3] + 'd' + date[3:5] + 'h' + date[5:7] + 'm' + date[7:9] + 's'
	return date[0:3] + " day(s), " + date[3:5] + " hour(s), " + date[5:7] + " minute(s) and " + date[7:9] + " second(s)"

def dateFormat_toSeconds(date):
	return \
		int(date[0:3]) * (60*60*24) + \
		int(date[3:5]) * (60*60   ) + \
		int(date[5:7]) *  60        + \
		int(date[7:9])
