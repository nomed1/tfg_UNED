import os
from SimpleXMLRPCServer import SimpleXMLRPCServer
import commands
def sendFile(arg,name):
    with open("temp/" + name, "wb") as handle:
        handle.write(arg.data)
        handle.close()
        result=commands.getoutput('python ~/cuckoo/utils/submit.py ./temp/' + name)
        return True


server = SimpleXMLRPCServer(("localhost", 9876))
print ("Listening on port 9876...")
server.register_function(sendFile, "sendFile")
server.serve_forever()
