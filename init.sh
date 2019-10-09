#!/bin/bash

sh ~/tfg/net.sh

xterm -e "cd ~/cuckoo;python cuckoo.py -d" &
xterm -e "cd ~/cuckoo;python utils/web.py" &
xterm -e "cd ~/tfg/server;python server_exereware.py" &
gnome-terminal --tab --command="bash -c 'cd ~/tfg/client/; python exereware_client.py -h; $SHELL'" &

cd ~/tfg/riskindroid
source vriskindroid/bin/activate
python3 app/app.py

