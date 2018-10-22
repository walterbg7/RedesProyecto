from socketPseudoTCP import *
serverPort = int(input("Ingrese un numero de puerto para el servidor, please: "))
serverSocket = SocketPseudoTCP()
serverSocket.bind(("", serverPort))
serverSocket.listen(1)
print ("El servidor esta listo para recibir mensajes")
while (1):
	connectionSocket, addr = serverSocket.accept()
	fileContent = connectionSocket.recv(1024)
	print (str(addr))
	print (str(fileContent))
	newFile = open("recievedFile.txt", 'w')
	if(not newFile):
		print("¡No se puedo crear el archivo!")
	newFile.write(fileContent.decode('utf-8'))
	newFile.close()
	#connectionSocket.send("Yes".encode('utf-8'))
	#connectionSocket.close()
