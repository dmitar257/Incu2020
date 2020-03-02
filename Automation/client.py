import socket
import readline
def Main():
 host="192.168.10.20"
 port=5000
 mySocket=socket.socket()
 mySocket.connect((host,port))
 message=input("Client>")
         
 while message !='q':
   mySocket.send(message.encode())
   data = mySocket.recv(1024).decode()
   print('Server>' + data)
   message = input("Client>")
 mySocket.close()

if __name__=='__main__':
  Main()
