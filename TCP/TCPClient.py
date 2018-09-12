from socket import *
serverName = "servername"
serverPort = 13000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(("", serverPort))
sentence = input("Ingrese en minusculas el mensaje: ")
clientSocket.sendall(sentence.encode('utf-8'))
modifiedSentence = clientSocket.recv(1024)
print ("Desde el Servidor: " + modifiedSentence.decode('utf-8'))
clientSocket.close()
