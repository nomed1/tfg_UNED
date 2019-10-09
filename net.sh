#!/bin/bash

export INTERFAZ=eth0

echo "Probando maquinas virtuales..."
vboxmanage snapshot android44 restore android44_3
vboxmanage startvm android44
vboxmanage controlvm android44 poweroff



#iptables para cuckoodroid
echo "Actualizando iptables..."
sudo iptables -A FORWARD -o $INTERFAZ -i vboxnet0 -s 192.168.56.0/24 -m conntrack --ctstate NEW -j ACCEPT
sudo iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A POSTROUTING -t nat -j MASQUERADE

sudo sysctl -w net.ipv4.ip_forward=1
