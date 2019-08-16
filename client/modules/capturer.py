#!/usr/bin/python

import os
import sys
import subprocess
import re
import time
import getopt
import hashlib as hash

import infor
import hasheador

class Comando:
	comando = ''
	salida = ''
	def __init__(self,comando):
		self.comando = comando
		self.salida = os.popen(comando).read()

	def getSalida(self):
		return self.salida

	def getComando(self):
		return self.comando

def pulling(device,origen, destino):
	com = "adb -s " + device + " pull " + origen + " " + destino
	return Comando(com)

def logo():
	print ("""
            ▓█████    ▒██   ██▒   ▓█████     ██▀███     ▓█████
            ▓█   ▀    ▒▒ █ █ ▒░   ▓█   ▀    ▓██ ▒ ██▒   ▓█   ▀
            ▒███      ░░  █   ░   ▒███      ▓██ ░▄█ ▒   ▒███
            ▒▓█  ▄     ░ █ █ ▒    ▒▓█  ▄    ▒██▀▀█▄     ▒▓█  ▄
            ░▒████▒   ▒██▒ ▒██▒   ░▒████▒   ░██▓ ▒██▒   ░▒████▒
            ░░ ▒░ ░   ▒▒ ░ ░▓ ░   ░░ ▒░ ░   ░ ▒▓ ░▒▓░   ░░ ▒░ ░
             ░ ░  ░   ░░   ░▒ ░    ░ ░  ░     ░▒ ░ ▒░    ░ ░  ░
               ░       ░    ░        ░        ░░   ░       ░
        """)
def cabecera():
	print("""
            EXERE Open Source Project
            Modulo 10
            Get info and apks from a device (no root required)
            telegram @nomed1 - xpressmoviles@gmail.com
            www.eltallerdelosandroides.com


        """)

if __name__ == "__main__":

	logo()
	cabecera()

	devices = infor.getDevices()

	if len(devices) == 0:
		print("No device connected or authorized")
		sys.exit(2)
	else:
		objetos = []
		print("Available devices\n")
		for index, device in enumerate(devices):
			c = infor.Campos(device)
			objetos.append(c)
			print("[" + str(index+1) + "] " + c.alias + " - " + device)

		i = int(input("\nChoose a number device to work: "))

		device = objetos[i-1].device

		if "win" in sys.platform:
			separador = '\\'
		else:
			separador = '\/'

		ruta_informacion = device + separador + "informacion"
		ruta_aplicaciones = device + separador + "aplicaciones"

		if os.path.exists(device):
			print("!!!ERROR 3: Folder " + device + " already exists, please make backup with another name and try again")
			sys.exit(3)
		else:
			os.makedirs(ruta_informacion)
			os.makedirs(ruta_aplicaciones)



		print("Show general information from device")
		print (objetos[i-1])

		print("All info will be saved in folder " + ruta_informacion)

		print("Getting and saving build.prop from device")
		com = Comando("adb -s " + device + " shell  \"cat /system/build.prop\" >> " + ruta_informacion + separador + "build_prop.txt")

		print("Getting and saving partitions available info from device")
		com = Comando("adb -s " + device + " shell df >> " + ruta_informacion + separador + "df.txt")

		print("Getting and saving mounts info from device")
		com = Comando("adb -s " + device + " shell mount >> " + ruta_informacion + separador + "mount.txt")

		print("Getting and saving process info from device")
		com = Comando("adb -s " + device + " shell ps >> " + ruta_informacion + separador + "ps.txt")

		print("Getting and saving list package and apks info from device")
		com = Comando("adb -s " + device + " shell  \"pm list package -f\" >> " + ruta_informacion + separador + "pm_list.txt")

		print("Getting and saving hosts info from device")
		com = Comando("adb -s " + device + " shell  \"cat /etc/hosts\" >> " + ruta_informacion + separador + "hosts.txt")

		print("Getting and saving ip info from device")
		com = Comando("adb -s " + device + " shell  \"ip addr\" >> " + ruta_informacion + separador + "ip_addr.txt")

		print("Getting and saving conections info from device")
		com = Comando("adb -s " + device + " shell  netstat >> " + ruta_informacion + separador + "netstat.txt")

		print("Getting and saving dump info from device")
		print("!!!!!! this operation will be take a minute please wait !!!!!!")
		com = Comando("adb -s " + device + " shell dumpsys >> " + ruta_informacion + separador + "dumpsys.txt")

	###### Now capturing apks

		print("Now all apks will be saved in " + ruta_aplicaciones)
		com = Comando("adb -s " + device + " shell \"pm list package -f\"")
		lineas = com.getSalida().split('\n')
		#lista = []

		for linea in lineas:
			if linea != "":
				elemento = linea[8:].split('=')
				#lista.append(elemento)
				destino = elemento[0].split('/')[-1]
				salida = pulling(device, elemento[0], ruta_aplicaciones + separador + elemento[1] + separador + destino)
				print("Pulling " + elemento[0] + " = OK")

		com = Comando("python hasheador.py -d " + device)
		print("Hashing folder " + device + " = OK")
