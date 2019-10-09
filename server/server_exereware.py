import os
from SimpleXMLRPCServer import SimpleXMLRPCServer
import commands
import sqlite3
import hashlib as hash

BD = "../../cuckoo/sql/mibd.sqlite3"

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

def get_index_md5(md5):
	"""devuelve el riesgo de el md5, se limita la busqueda a el ultimo analisis de ese md5"""
	
	con = sqlite3.connect(get_path_bd())
	cursor = con.cursor()
	index = 0
	sql = """
		SELECT *
		FROM muestras
		WHERE `md5`=?
        ORDER BY `index` DESC
		LIMIT 1;
	"""
	for row in cursor.execute(sql,(md5,)):
		index = row[0]
	cursor.close()
	return index

def get_risk_index(index):
	"""devuelve el riesgo de un indice"""
	
	con = sqlite3.connect(get_path_bd())
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

def sendFile(arg,name):
    with open("temp/" + name, "wb") as handle:
        handle.write(arg.data)
        handle.close()
        result=commands.getoutput('python ~/cuckoo/utils/submit.py ./temp/' + name)
        md5 = md5sum("temp/" + name)
        index = get_index_md5(md5)
        return str(index) + ";" + str(get_risk_index(index))

server = SimpleXMLRPCServer(("localhost", 9876))
print ("Listening on port 9876...")
server.register_function(sendFile, "sendFile")
server.register_function(get_risk_index, "get_risk_index")
server.serve_forever()
