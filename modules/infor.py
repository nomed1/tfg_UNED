#!/usr/bin/python

import os
import sys
import subprocess
import re
import time
import getopt
import hashlib as hash

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

class Campos:

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
		self.device = device
		#com = Comando("adb -s " + device + " shell cat /system/build.prop")
		com = Comando("adb -s " + device + " shell getprop")
		lineas = com.getSalida().split('\n')
		for linea in lineas:
			linea = linea.replace('[','')
			linea = linea.replace(']','')
			linea = linea.replace(': ','=')
			linea = linea.split('=')
			if 'ro.product.manufacturer' in linea[0]:
				self.marca = linea[1]
			if 'ro.product.model' in linea[0]:
				self.modelo = linea[1]
			if 'ro.product.modelalias' in linea[0]:
				self.alias = linea[1]
			if 'ro.build.version.release' in linea[0]:
				self.versionAndroid = linea[1]
			if 'ro.build.display.id' in linea[0]:
				self.versionCompilacion = linea[1]
			if 'ro.build.version.incremental' in linea[0]:
				self.versionPersonalizacion = linea[1]
			if 'gsm.version.baseband' in linea[0]:
				self.versionModem = linea[1]
			if 'internal_sd_path' in linea[0]:
				self.pathInterno = linea[1]
			if 'external_sd_path' in linea[0]:
				self.pathExterno = linea[1]
		com = Comando("adb -s " + device + " shell cat /proc/version")
		self.versionLinux = com.getSalida().strip()


	def __str__(self):
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
	com = Comando("adb devices")
	lineas = com.getSalida().split("\n")[1:]

	#get only valid lines with strin device

	for linea in lineas:
		if 'device' in linea:
			sp = linea.split('\t')
			lista.append(sp[0])
	return lista

def getDevicesModel(devices):
	"""Get the list of devices with model"""

	for dev in devices:
		com = Comando("adb -s " + dev + " shell cat /system/build.prop")
		lineas = com.getSalida().split("\n")
		for linea in lineas:
			if 'ro.product.manufacturer' in linea:
				print (linea.split('=')[1])

def getDeviceInfo(device):
	"""Get all info of a device"""

	com = Comando("adb -s " + device + " cat /system/build.prop")
	for linea in com.getSalida():
		for campo in campos:
			if campo in linea:
				print(linea)

if __name__ == "__main__":

	devices = getDevices()

	if len(devices) == 0:
		print("No device connected or authorized")
		sys.exit(2)
	else:
		objetos = []
		print("Available devices\n")
		for index, device in enumerate(devices):
			c = Campos(device)
			objetos.append(c)
			print("[" + str(index+1) + "] " + c.alias + " - " + device)


		i = int(input("\nChoose a number to report: "))
		print(objetos[i-1])
