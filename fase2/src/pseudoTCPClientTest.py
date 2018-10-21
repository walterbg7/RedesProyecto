from socketPseudoTCP import *
import sys
serverName = str(input("Ingrese un ip, please: "))
serverPort = int(input("Ingrese un puerto, please: "))
clientSocket = SocketPseudoTCP()
clientSocket.connect((serverName, serverPort))
filename = input("Ingrese el nombre del archicho de texto que desea enviar: ")
file = open(filename, 'r')
if(not file):
    print("¡Digite un nombre de archivo valido!")
    sys.exit(-1)
fileContent = file.read()
file.close()
clientSocket.send(fileContent.encode('utf-8'))
modifiedSentence = clientSocket.recv(1024)
print ("Desde el Servidor: " + modifiedSentence.decode('utf-8'))
clientSocket.close()
