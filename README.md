# título : Análisis de Malware en smartphones Android. Prototipo de integración y automatización
Desarrollo para seguimiento del prototipo para el tfg para la UNED: exereWare  
alumno: Buenaventura Salcedo  
director: Antonio Sanz  
codirector: Roberto Hernandez  
profesor de apoyo: Rafael Pastor  
## Instalación y puesta en marcha  
IMPORTANTE: Use con Ubuntu 14.04(Recomendado) o 16.04, para otras versiones necesitará resolver dependencias python 2.7  
Para instalar solo el entorno de cuckoodroid y probar su funcionamiento:  
~~~
cd ~/  
git clone https://github.com/nomed1/tfg_UNED/ tfg  
sudo chmod +x ~/tfg/install.sh  
~/tfg/install.sh  
~~~
Vaya a la carpeta de cuckoo y lancelo:
~~~
python ~/cuckoo/cuckoo.py -d  
~~~
Para enviar una muestra y ver resultados (después podrá utilizar el cliente de exereWare):    
~~~
python ~/cuckoo/utils/web.py  
~~~
A continuación abra un navegador y vaya a la direccion 127.0.0.1:8080  
También puede enviar muestras con:  
~~~
python ~/cuckoo/utils/submit.py ruta_de_la_muestra_apk  
~~~
## Descripcion de ficheros y carpetas:  
propuesta_plan.txt --> El plan de trabajo propuesto al codirector  
install.sh --> Descarga cuckoodroid ya configurado e instala todas sus dependencias.
