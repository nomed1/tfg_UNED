#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import re
import time
import getopt
import hashlib as hash

class Command:
    """Clase para lanzar los comandos adb"""

    comannd = ''
    out = ''
    def __init__(self,command):
		self.command = command
		self.out = os.popen(command).read()

    def getOut(self):
		return self.out

    def getCommand(self):
		return self.command

class Fields:
    """Clase para almacenar la informacion de un telefono"""
    device = ''
    marca = ''
    modelo = ''
    alias = ''
    versionAndroid =''
    versionCompilacion = ''
    versionPersonalizacion= ''
    versionModem = ''
    versionLinux=''
    pathInterno = ''
    pathExterno = ''
    def __init__(self,device):
        """Formatea los campos de la informacion del telefono"""

        self.device = device
		#com = Command("adb -s " + device + " shell cat /system/build.prop")
        com = Command("adb -s " + device + " shell getprop")
        lines = com.getOut().split('\n')
        for line in lines:
            line = line.replace('[','')
            line = line.replace(']','')
            line = line.replace(': ','=')
            line = line.split('=')
            if 'ro.product.manufacturer' in line[0]:
                self.marca = line[1]
            if 'ro.product.model' in line[0]:
				self.modelo = line[1]
            if 'ro.product.modelalias' in line[0]:
				self.alias = line[1]
            if 'ro.build.version.release' in line[0]:
				self.versionAndroid = line[1]
            if 'ro.build.display.id' in line[0]:
				self.versionCompilacion = line[1]
            if 'ro.build.version.incremental' in line[0]:
				self.versionPersonalizacion = line[1]
            if 'gsm.version.baseband' in line[0]:
				self.versionModem = line[1]
            if 'internal_sd_path' in line[0]:
				self.pathInterno = line[1]
            if 'external_sd_path' in line[0]:
				self.pathExterno = line[1]
        com = Command("adb -s " + device + " shell cat /proc/version")
        self.versionLinux = com.getOut().strip()

    def __str__(self):
        """Devuelve todo en forma de cadena"""

        cadena = """
	Device ID={}
	Manufacturer={}
	Modelo={}
	Alias={}
	Version Android={}
	Version Compilation={}
	Version Personalizacion={}
	Version Modem={}
	Version Linux={}
	Path Storage Internal={}
	Path Storage External={}
		""".format(
			self.device,
			self.marca,
			self.modelo,
			self.alias,
			self.versionAndroid,
			self.versionCompilacion,
			self.versionPersonalizacion,
			self.versionModem,
			self.versionLinux,
			self.pathInterno,
			self.pathExterno)
        return cadena

def getDevices():
	"""Get the list of id devices"""

	lista = []
	com = Command("adb devices")
	lines = com.getOut().split("\n")[1:]

	#get only valid lines with strin device

	for line in lines:
		if 'device' in line:
			sp = line.split('\t')
			lista.append(sp[0])
	return lista


def pulling(device,origen, destino):
	com = "adb -s " + device + " pull " + origen + " " + destino
	return Command(com)

def triage_basic(device,info_path):
    #print "Show general information from device"
    #print (objetos[i-1])

    print "Getting and saving build.prop from device"
    com = Command("adb -s " + device + " shell  getprop >> " + info_path + "/" + "getprop.txt")

    print "Getting and saving partitions available info from device"
    com = Command("adb -s " + device + " shell df >> " + info_path + "/" + "df.txt")

    print "Getting and saving mounts info from device"
    com = Command("adb -s " + device + " shell mount >> " + info_path + "/" + "mount.txt")

    print "Getting and saving process info from device"
    com = Command("adb -s " + device + " shell ps >> " + info_path + "/" + "ps.txt")

    print "Getting and saving list package and apks info from device"
    com = Command("adb -s " + device + " shell  \"pm list package -f\" >> " + info_path + "/" + "pm_list.txt")

    print "Getting and saving hosts info from device"
    com = Command("adb -s " + device + " shell  \"cat /etc/hosts\" >> " + info_path + "/" + "hosts.txt")

    print "Getting and saving ip info from device"
    com = Command("adb -s " + device + " shell  \"ip addr\" >> " + info_path + "/" + "ip_addr.txt")

    print "Getting and saving conections info from device"
    com = Command("adb -s " + device + " shell  netstat >> " + info_path + "/" + "netstat.txt")

    #print "Getting and saving dump info from device"
    #print "!!!!!! this operation will be take a minute please wait !!!!!!"
    #com = Command("adb -s " + device + " shell dumpsys >> " + info_path + "/" + "dumpsys.txt")

    #esto hay que sincronizarlo de alguna manera para que pare
    #print "Getting and saving logcat info from device 20 seconds"
    #com = Command("adb -s " + device + " shell logcat  >> " + info_path + "/" + "logcat.txt")

def get_all_apks(apps_path):
    """Descarga todas las apks del telefono a la carpeta de trabajo"""

    print("Now all apks will be saved in " + apps_path)
    com = Commad("adb -s " + device + " shell \"pm list package -f\"")
    lines = com.getOut().split('\n')

    for line in lines:
        if line != "":
            element = line[8:].split('=')
            #lista.append(elemento)
            dest = element[0].split('/')[-1]
            out = pulling(device, element[0], apps_path + "/" + element[1] + "/" + dest)
            print("Pulling " + element[0] + " = OK")

def get_list_package(device,mode):
    """Lista las apks, si mode=-d limita a las descargadas"""

    #podriamos usar sed para quitar los 8 primeros caracteres, pero no es compatible con windows
    com = Command("adb -s " + device + " shell \"pm list package -f " + mode + "\"")

    lines = com.getOut().split('\n')
    list = []
    for line in lines:
        if line != "":
            ##element = line[8:].split('=')
            ##list.append(element)
            clean = line[8:] #saca la cadena Package:
            index = clean.rfind('=')
            element = [clean[:index],clean[index+1:]]
            list.append(element)
            #dest = element[0].split('/')[-1]
            #out = pulling(device, element[0], apps_path + "/" + element[1] + "/" + dest)
            #print("Pulling " + element[0] + " = OK")
    return list

def get_apks(device,apps_path,lista):
    """Bucle de descarga de las apks de la lista en la ruta pasada"""

    for element in lista:
        dest = element[0].split('/')[-1]
        out = pulling(device, element[0], apps_path + "/" + element[1] + "/" + dest)
        print("Pulling " + element[0] + " = OK")

def connection():
    devices = getDevices() #recupera lista de telefonos conectados al PC
    if len(devices) == 0:
        print "No device connected or authorized"
        print "Try in a shell: adb devices"
        print "If id = ????????????? lunch: sudo python exere_fix_adb"
        print "this can fix your phone in your linux system"
        sys.exit(3)
    else:
        objets = []
        print "Available devices\n"
        for index, device in enumerate(devices):
            c = Fields(device)
            objets.append(c)
            print "[" + str(index+1) + "] " + c.alias + " - " + device

        i = int(input("\nChoose a number device to work: "))
        return objets[i-1].device
