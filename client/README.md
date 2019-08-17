cliente exereWare para la subida masiva de muestras desde una carpeta o extrayendolas directamente de un smartphone para analizar sus apks. 

###client_exereware.py  
Sirve para enviar lotes muestras usando RPC al servidor. Si no se cambia en el código supondrá que la ip del servidor es localhost y que se está ejecutando el servidor en la misma maquina, sino pues abra el puerto 9876 del servidor e indique su ip en el código del cliente.  

###exere_fix_adb.py  
Si el cliente no detecta el teléfono conectado lo que hace es agregarlo al sistema para que lo reconozca, requiere permisos root, por tanto ejecutelo con sudo.  

Si utiliza el client_exereware.py e intenta usarlo con el telefono pero no lo detecta, intente agregarlo lanzando:  

~~~
sudo python exere_fix_adb.py
~~~  
