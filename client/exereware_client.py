#!/usr/bin/python
# -*- coding: utf-8 -*-
import xmlrpclib
import sys
import os
import getopt
import time
import hashlib as hash


from modules.artfile import logo,header,usage
from modules.search import init_search
from modules.mobile import connection,getDevices,pulling,Fields,Command,triage_basic, get_list_package, get_all_apks, get_apks
from modules.operations import validate_path,get_list_files_dir, get_list_files_arg

URL = "http://localhost"
PORT = "9876"
# TASK file in csv format
TASKS = "tasks.txt"

def md5sum(fi):
	""" generate hash of file fichero"""
	TAM = 65536	
	md5 = hash.md5()
	with open(fi, 'rb') as f:
		buf = f.read(TAM)
		while len(buf) > 0:
			md5.update(buf)
			buf = f.read(TAM)
	return md5.hexdigest()

def send_files(list_files):
    """Envia la lista de ficheros al servidor"""
    
    #print "%s" % list_files
    proxy = xmlrpclib.Server(URL + ":" + PORT + "/")
    file = open(TASKS,"a+")
    linesw = []
    for f in list_files:
        print "Sending..." + f
        with open(f, "rb") as handle:
            md5 = md5sum(f)
            date = time.strftime("%d-%m-%y %H:%M:%S")  
            file_binary = xmlrpclib.Binary(handle.read())
            ret = proxy.sendFile(file_binary,f.split('/')[-1]).split(";")
            index = ret[0]
            risk = ret[1]
            linew = str(index) + ";" + md5 + ";" + date + ";" + f + ";" + risk + ";\n"
            file.write(linew)
        print "file sended OK with id task = " + str(index) + " --> SCORE = " + str(risk) + "/100"
    file.close()   
        
def send_files1(list_files):
    """Envia la lista de ficheros al servidor"""
    
    #print "%s" % list_files
    proxy = xmlrpclib.Server(URL + ":" + PORT + "/")
    for f in list_files:
        print "Sending..." + f
        with open(f, "rb") as handle:
            file_binary = xmlrpclib.Binary(handle.read())
        proxy.sendFile(file_binary,f.split('/')[-1])
        
def init_process(mode):
    """Inicia el proceso de conexion y captura de apks"""

    device = connection()

    #si existe la carpeta renombra la vieja con la fecha_hora actual
    if os.path.exists(device):
        now = time.strftime("%Y%m%d_%H%M%S")
        print "Folder " + device + " already exists"
        os.rename(device,device + "_" + now)
        print "Renamed to: " + device + "_" + now

    info_path = device + "/" + "info"
    apps_path = device + "/" + "apps"
    os.makedirs(info_path)
    os.makedirs(apps_path)

    #crea el triage del telefono en la carpeta info_path
    print "Performing triage and will be save in " + info_path
    triage_basic(device,info_path)
    #captura los apks en la carpeta apps_path
    print "Now is getting and making backup apks before send to Server exereWare"
    get_apks(device,apps_path,get_list_package(device,mode))
    #envia los apks recopilados en la carpeta de trabajo actual al servidor
    return device


def show_apks_availables():
    device = connection()
    for i in get_list_package(device,""): #recuperamos los nombres de todas las apks
        print i

def show_risk(file_task):
    """Imprime los riesgos de cada fichero con su id_task y ruta"""
    st = ""
    print ('{0:10} {1:20} {2:10} {3:20}'.format("ID_TASK","DATE","SCORE","NAME"))
    print ('{0:10} {1:20} {2:10} {3:20}'.format("-------","-----","-----","----"))
    with open(file_task) as file:
        for line in file:
            li = line.split(";")
            index = li[0]
            md5 = li[1]
            fecha = li[2]
            file = li[3].split('/')[-1]
            score = li[4] + "%"
            print ('{0:10} {1:20} {2:10} {3:20}'.format(index,fecha,score,file))

if __name__ == "__main__":

    logo()
    header()
    params = ""
    try:
        options, arguments = getopt.getopt(sys.argv[1:], "hrfadvxl:")
        #print options
        #print arguments
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for option,argument in options:
        if option in ('-h'):
            usage()
            sys.exit(1)
        if option in ('-r'):
            params = sys.argv[2]
            print "Procesing apks from recursive mode folder " + params
            send_files(get_list_files_dir(params,"apk")) #pasamos la extension apk
        if option in ('-f'):
            params = sys.argv[2]
            print "Procesing apks from list targets"
            send_files(get_list_files_arg(params)) #pasamos la lista de apks
        if option in ('-l'):
            params = sys.argv[2]
            #aqui falta procesar la lista
            #send_files(get_list_files_dir(device,"apk"))
        if option in ('-d'):
            print "Processing apks from Downloaded Aplications Section"
            params = init_process("-d") #mode -d las apks que tiene descargadas el telefono
            send_files(get_list_files_dir(params,"apk"))#params es el device
        if option in ('-a'):
            print "Processing all apks from Smartphone"
            params = init_process("") #mode vacio todas las apks del telefono
            send_files(get_list_files_dir(params,"apk"))#params es el device
        if option in ('-v'):
            print "Showing apks available on the Smartphone"
            show_apks_availables()
        if option in ('-x'):
            print "Getting danger score from apks processed in tasks.txt log file"
            show_risk("tasks.txt")
