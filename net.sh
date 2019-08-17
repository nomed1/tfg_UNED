#!/bin/bash

#levantar vboxnet0

sudo ifconfig vboxnet0 192.168.56.1 netmask 255.255.255.0 up

#iptables para cuckoodroid

sudo iptables -A FORWARD -o INTERFAZ -i vboxnet0 -s 192.168.56.0/24 -m conntrack --ctstate NEW -j ACCEPT
sudo iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A POSTROUTING -t nat -j MASQUERADE

sudo sysctl -w net.ipv4.ip_forward=1
