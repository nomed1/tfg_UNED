#!/usr/bin/python

import requests
import os
import sys
import time
import sqlite3
import hashlib as hash
import fileinput

BD = "../../../sql/mibd.sqlite3"

def get_path_bd():
	""" devuelve la ruta absoluta de la base de datos"""
	
	return os.path.join(os.path.dirname(os.path.abspath(__file__)),BD)

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

def calculate_risk(fi):
	"""Recibe la ruta de una muestra y devuelve el riesgo"""
	
	r = requests.post('http://127.0.0.1:5000/upload', files={'file': open(fi, 'rb')})

	web = r.text
	lines = web.split('\n')

	for line in lines:
		if "var riskVal = " in line:
			value = line.strip().replace(";","").replace("var riskVal = ","")
	return value

def get_risk(index,bd):
	"""devuelve el riesgo de un indice"""
	
	con = sqlite3.connect(bd)
	cursor = con.cursor()
	risk = 0
	sql = """
		SELECT *
		FROM muestras
		WHERE `index`=?
		LIMIT 1;
	"""
	for row in cursor.execute(sql,(index,)):
		risk = row[2]
	cursor.close()
	return risk
	
def add_register(index,md5,risk,bd):
	"""inserta en la base de datos bd, el indice, el md5 y el riesgo de una muestra"""
	
	con = sqlite3.connect(bd)
	cursor = con.cursor()
	sql = """
		INSERT INTO muestras
		(`index`,`md5`,`risk`)
		VALUES
		(?,?,?);
		"""
	cursor.execute(sql,(index,md5,risk))
	con.commit()
	cursor.close()
	return 0

def my_replace(file,orig,index):
	risk = get_risk(index,get_path_bd())
	dest = "<td id='MY__ID1'>DANGER SCORE: "+str(risk)+"/100</td>"
	for line in fileinput.input(file, inplace=1):
		if orig in line:
			line = line.replace(line,dest)
		sys.stdout.write(line)

#if __name__ == "__main__":
#	print get_path_bd()
#	add_register(1,"abc",3.9,get_path_bd())
#	print md5sum("/home/nomed/tfg/client/muestras/bot.apk")
#	print get_risk(1,get_path_bd())
	
