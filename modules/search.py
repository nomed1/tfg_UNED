#!/usr/bin/python
# -*- coding: utf-8 -*-

from glob import glob
from os import path

list_files = []

def search(dir,ext):
    """Busca recursivamente los ficheros con extension
    y devuelve una lista con ellos"""

    elements = glob(dir + "/" + "*")
    vector = dir.split('/')
    for element in elements:
        if path.isdir(element):
            search(element,ext)
        elif path.isfile(element):
            vector = element.split('/')
            extension = vector[-1].split('.')
            if ext == extension[-1]:
                list_files.append("/".join(vector))

def init_search(dir,ext):
    search(dir,ext)
    return list_files

#if __name__ == '__main__':
#    search(".","apk")
#    print list_files
