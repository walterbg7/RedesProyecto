from socketPseudoTCP import *
serverPort = int(input("Ingrese un numero de puerto para el servidor, please: "))
serverSocket = SocketPseudoTCP()
serverSocket.bind(("", serverPort))
serverSocket.listen(1)
print ("El servidor esta listo para recibir mensajes")
while (1):
	connectionSocket, addr = serverSocket.accept()
	sentence = connectionSocket.recv(1024)
	print (str(addr))
	print (str(sentence))
	capitalizedSentence = sentence.upper()
	connectionSocket.send(capitalizedSentence)
	connectionSocket.close()
