#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

from modules.search import init_search

def validate_path(path):
    """Comprobaciones de ficheros y direcciones"""
    if path == "":
        #print "ERROR 1: need path for a directory"
        #usage()
        #sys.exit(1)
        return False
    elif not os.path.exists(path):
        #print "ERROR 2: path %s not found" % path
        #usage()
        #sys.exit(1)
        return False
    return True

def get_list_files_dir(path,ext):
    """Obtiene la lista de ficheros con extension ext del path"""
    if validate_path(path): # si el path no existe aborta
        return init_search(path,ext)
    else:
        print "ERROR 1: path %s not found" % path
        usage()
        sys.exit(1)

def get_list_files_arg(list_apks):
    """Comprueba si existen los apks y devuelve lista limpia"""
    l = list_apks.split(",")
    nl = []
    for i in l:
        if validate_path(i):
            nl.append(i)
        else:
            print "WARNING: file %s is not going to be analyzed because it does not exist" % i
    return nl
