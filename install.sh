#!/bin/bash

sudo apt-get update
sudo apt-get upgrade

sudo apt-get install curl git python python-pip python-dev libffi-dev libssl-dev mongodb python-dpkt  python-virtualenv -y

sudo apt-get install qemu-kvm libvirt-bin ubuntu-vm-builder bridge-utils python-libvirt -y

sudo apt-get install android-tools-adb android-tools-fastboot -y

#cuckoodroid
cd ~/
unzip ~/tfg/cuckoo.zip -d ~/

#requirements
sudo apt-get install python-bson
sudo pip install sqlalchemy==0.9.9
sudo pip install bson
sudo pip install jinja2==2.8
sudo pip install pymongo==3.0.3
sudo pip install bottle
sudo pip install pefile
sudo pip install django==1.8.4
sudo pip install chardet==2.3.0
sudo pip install nose
sudo pip install requests
sudo pip install androguard==3.0
sudo pip install protobuf

# tcpdump

sudo apt-get install tcpdump -y
sudo setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump
sudo apt-get install libcap2-bin -y
sudo chmod +s /usr/sbin/tcpdump

# yara + pydeep(machine learning) + volatility

sudo apt-get install yara ssdeep libfuzzy-dev volatility -y
cd ~/tfg
git clone https://github.com/kbandla/pydeep.git
cd ~/tfg/pydeep
sudo python setup.py install

#virtualbox

cd ~/tfg
wget https://download.virtualbox.org/virtualbox/6.0.10/virtualbox-6.0_6.0.10-132072~Ubuntu~trusty_amd64.deb
sudo dpkg -i ~/tfg/virtualbox-6.0_6.0.10-132072~Ubuntu~trusty_amd64.deb
sudo apt-get install -f -y

#extension_pack

cd ~/tfg
wget https://download.virtualbox.org/virtualbox/6.0.10/Oracle_VM_VirtualBox_Extension_Pack-6.0.10.vbox-extpack
sudo VBoxManage extpack install ~/tfg/Oracle_VM_VirtualBox_Extension_Pack-6.0.10.vbox-extpack

#descargar, descomprimir y registrar MV android44 en virtualbox
cd ~/tfg
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1sfSuFk58CRD0KjuYiHDZ-jVaSM3TFT5L' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1sfSuFk58CRD0KjuYiHDZ-jVaSM3TFT5L" -O ~/tfg/android44.zip && rm -rf /tmp/cookies.txt

unzip ~/tfg/android.zip -d ~/tfg

VBoxManage hostonlyif create
VBoxManage registervm ~/tfg/android44/android44.vbox

#iptables

sudo iptables -A FORWARD -o INTERFAZ -i vboxnet0 -s 192.168.56.0/24 -m conntrack --ctstate NEW -j ACCEPT
sudo iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A POSTROUTING -t nat -j MASQUERADE

sudo sysctl -w net.ipv4.ip_forward=1

echo "###########################################################"
echo "El entorno ha sido instalado."
echo "Puede existir alguna dependencia rota"
echo "y que necesite instalar con sudo pip install"
echo "El entorno de cuckoo esta configurado para la MV descargada"
echo "Tambien se han resuelto fallos de codigo en cuckoodroid"
echo "lea la memoria del prototipo si tiene problemas"
