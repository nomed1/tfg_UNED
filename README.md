# título : Análisis de Malware en smartphones Android. Prototipo de integración y automatización
Desarrollo para seguimiento del prototipo para el tfg para la UNED: exereWare  
alumno: Buenaventura Salcedo  
director: Antonio Sanz  
codirector: Roberto Hernandez  
profesor de apoyo: Rafael Pastor  

## Instalación y puesta en marcha  
IMPORTANTE: Use con Ubuntu 16.04(Recomendadísimo) para otras versiones necesitará resolver dependencias  
Lea cuidadosamente las instrucciones que le ofrece en la ejecución install.sh y haga lo que se le indica:  
Para instalar solo el entorno de cuckoodroid y probar su funcionamiento:  

~~~
cd ~/  
git clone https://github.com/nomed1/tfg_UNED/ tfg  
sudo chmod +x ~/tfg/install.sh  
~/tfg/install.sh  
~~~
Vaya a la carpeta de cuckoo y láncelo:
~~~
python ~/cuckoo/cuckoo.py -d  
~~~
Para enviar una muestra y ver resultados (después podrá utilizar el cliente de exereWare):    
~~~
python ~/cuckoo/utils/web.py  
~~~
A continuación abra un navegador y vaya a la dirección 127.0.0.1:8080  
También puede enviar muestras con:  
~~~
python ~/cuckoo/utils/submit.py ruta_de_la_muestra_apk  
~~~  
### IMPORTANTE: agregue al arranque el script net.sh para levantar las interfaces e iptables en cada reinicio del PC servidor  

## Uso exereWare  
exereWare es una propuesta de integración con cuckoodroid que funciona como cliente-servidor que usa RPC a través del puerto 9876.  
Para ponerlo en funcionamiento cuckoodroid debe estar en estado de espera como se indicó más arriba y a continuación desde otra terminal en el servidor debe ponerse en escucha con:  
~~~  
python ~/tfg/server/server_exereware.py
~~~  
Una vez que el servidor esta levantado podemos lanzar el cliente para buscar las muestras en una carpeta, pasarle una lista de rutas para cada muestra, conectando un telefono al PC y extrayendo directamente las muestras o una lista de ellas. Puede consultar todas las opciones con el parámetro -h. El cliente se lanza con:
~~~  
python ~/tfg/client/exereware_client.py [opciones] <argumentos>  
~~~
Aquí puede ver un video de funcionamiento para exereWare alpha 0.1 https://www.youtube.com/watch?v=Qi4z1KGmm98  
## Descripción de ficheros y carpetas:  
propuesta_plan.txt --> El plan de trabajo propuesto al codirector.  
install.sh         --> Descarga cuckoodroid ya configurado e instala todas sus dependencias.  
net.sh             --> Levanta interfaz vboxnet0 y lanza las reglash iptables despues de cada reinicio  
cuckoo.zip         --> Cuckoodroid configurado para trabajar con la MV android44 que puede encontrar en:  
https://drive.google.com/open?id=1sfSuFk58CRD0KjuYiHDZ-jVaSM3TFT5L  
client             --> carpeta que contiene el cliente de exereWare, contiene ayuda.  
server             --> carpeta que contiene el servidor de escucha de exereWare, contiene ayuda.  
memoria            --> capítulos para organizar la memoria del TFG.
