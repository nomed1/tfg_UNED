#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

def logo():
	print """
            ▓█████    ▒██   ██▒   ▓█████     ██▀███     ▓█████
            ▓█   ▀    ▒▒ █ █ ▒░   ▓█   ▀    ▓██ ▒ ██▒   ▓█   ▀
            ▒███      ░░  █   ░   ▒███      ▓██ ░▄█ ▒   ▒███
            ▒▓█  ▄     ░ █ █ ▒    ▒▓█  ▄    ▒██▀▀█▄     ▒▓█  ▄
            ░▒████▒   ▒██▒ ▒██▒   ░▒████▒   ░██▓ ▒██▒   ░▒████▒
            ░░ ▒░ ░   ▒▒ ░ ░▓ ░   ░░ ▒░ ░   ░ ▒▓ ░▒▓░   ░░ ▒░ ░
             ░ ░  ░   ░░   ░▒ ░    ░ ░  ░     ░▒ ░ ▒░    ░ ░  ░
               ░       ░    ░        ░        ░░   ░       ░
        """
def header():
	print """
            EXERE Open Source Project
            Module Client for exereWare: TFG UNED 2019
            Recopile apks from a directory or smartphone
            and send to analyzer Server
            Buenaventura Salcedo telegram: @nomed1
        """

def usage ( ):
	print "Usage: %s [options]" % sys.argv[0]
	print """
            Options:
	-h                see this help
	-r <dir>          recursive search for apks in <dir> to analyze
	-f <f1,f2,...fn>  list of files to analyze
	-a                select all apks from a smartphone
	-d                select only donwloads apks on the smartphone
 	-l <p1,p2,...pn>  select only apks in list on the smartphone
        -v                show availables apks on the smartphone

    """

if __name__ == "__main__":

	logo()
	cabecera()
	usage()
