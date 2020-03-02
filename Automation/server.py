import socket
import re
import datetime
from ncclient import manager
import xml.dom.minidom
import pprint
import socket
import json


op_types={
        "undefined":-1,
        "calc":0,
        "time":1,
        "sh_version":2,
        "set_hostname":3
        }

def getTime():
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S")
    
def getEvaluation(expr):
    try:
        return eval(expr)
    except:
        raise Exception("The expression could not be evaluated !") 


def checkOperation(args):  #checks which command server received and argument number validity
        if len(args)==0:
            return op_types['undefined']
        if args[0] == "time":
            if len(args) != 1:
                raise Exception("Time command needs no argument!")
            return op_types['time']
        elif re.search("^calc(?:u|ul|ula|ulat|ulato|ulator)?$",args[0]):
            if len(args) != 2:
                raise Exception("Calculate command needs only one argument (expression)!")
            return op_types['calc']
        elif re.search("^sh(?:o|ow)?$",args[0]): #show command is entered
            if len(args)==1:
                raise Exception("Show command must have some arguments!")
            if re.search("^ver(?:s|si|sio|sion)?$",args[1]): #show version command is entered
                if len(args) != 2:
                    raise Exception("Wrong number of arguments!")
                return op_types["sh_version"]
        elif re.search("^hos(?:t|tn|tna|tnam|tname)?$",args[0]):
            if len(args) != 2:
                raise Exception("Wrong number of arguments!")
            return op_types["set_hostname"]

        return op_types['undefined']

def connect(node): #connects to the edge device
    try:
        m = manager.connect(
                host = node,
                port = '22',
                username = 'admin',
                password = 'cisco!123',
                hostkey_verify = False,
                device_params={'name':'nexus'},
                allow_agent=False,
                look_for_keys=False
                )
        print("Successfully connected to the: ",node)
        return m
    except:
        raise Exception("Could not connect to the: " + node)

def getVersion(node):
    device_connection = connect(node)
    try:
        version_filter = '''
                       <show xmlns="http://www.cisco.com/nxos:1.0">
                          <version>
                          </version>
                        </show>
        '''
        netconf_output = device_connection.get(('subtree', version_filter))
        xml_doc = xml.dom.minidom.parseString(netconf_output.xml)
        version = xml_doc.getElementsByTagName("mod:nxos_ver_str")[0].firstChild.nodeValue
        return version
    except:
        raise Exception("Unable to get this node version!")
        

def setHostname(hName,node):
    device_connection = connect(node)
    try:
        hostname_filter = '''
                       <configure xmlns="http://www.cisco.com/nxos:1.0">
                         <__XML__MODE__exec_configure>
                            <hostname>
                              <name>%s</name>
                            </hostname>
                          </__XML__MODE__exec_configure>
                        </configure>
         '''
        configuration=''
        configuration+='<config>'
        configuration+=hostname_filter % hName
        configuration+='</config>'
        device_connection.edit_config(target='running',config=configuration)
        print("Config pushed successfully!")
    except:
        raise Exception("Unable to change this node's hostname")

def Main():
  host="localhost"
  port=5000
  node="192.168.10.30"
  mySocket=socket.socket()
  mySocket.bind(('',port))
  mySocket.listen(5)
  conn,addr=mySocket.accept()
  print("Connection from:"+str(addr))
  while True:
     message=conn.recv(1024).decode()
     response_msg=""
     if message:
        try:
            args = message.split()
            opCode = checkOperation(args)
            if opCode == op_types['time']:
                response_msg = getTime()
            elif opCode == op_types['calc']:
                response_msg=str(eval(args[1]))
            elif opCode == op_types['sh_version']:
                response_msg ="Version: " + getVersion(node)
            elif opCode == op_types['set_hostname']:
                setHostname(args[1],node)
                response_msg = "Hostname changed to: "+args[1]
            else:
                response_msg="Unrecognized command!"
        except Exception as exc:
            response_msg = exc.args[0]
     else:
        break
     conn.send(response_msg.encode())
  conn.close()

if __name__=='__main__':
    Main()
