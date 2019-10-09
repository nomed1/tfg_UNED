cliente exereWare para la subida masiva de muestras desde una carpeta o extrayendolas directamente de un smartphone para analizar sus apks.  
# Revisiones  
None
### exereware_client.py  
Sirve para enviar lotes muestras usando RPC al servidor. Si no se cambia en el código supondrá que la ip del servidor es localhost y que se está ejecutando el servidor en la misma maquina, sino pues abra el puerto 9876 del servidor e indique su ip en el código del cliente.  
### exere_fix_adb.py  
Si el cliente no detecta el teléfono conectado lo que hace es agregarlo al sistema para que lo reconozca, requiere permisos root, por tanto ejecutelo con sudo.  

Si utiliza el client_exereware.py e intenta usarlo con el telefono pero no lo detecta, intente agregarlo lanzando:  

~~~
sudo python exere_fix_adb.py
~~~  

tasks.txt es un fichero que registra los ficheros enviados con el siguiente formato:  
id_task_en_el_servidor;md5;fecha;ruta_fichero_apk  
el fichero se utiliza despues para poder conocer los riesgos de cada apk y poder conocer el id
del report que queremos descargar.  

### muestras  
Contiene unas muestras para analizar, cuidado es malware para android.  
### imágenes  
![Vista cliente](/images/cliente_01.png "exereware_client") 
