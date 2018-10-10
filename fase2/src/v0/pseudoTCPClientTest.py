from socketPseudoTCP import *
while(1):
    serverName = str(input("Ingrese un ip, please: "))
    serverPort = int(input("Ingrese un puerto, please: "))
    clientSocket = SocketPseudoTCP()
    clientSocket.connect((serverName, serverPort))
    sentence = input("Ingrese en minusculas el mensaje: ")
    clientSocket.send(sentence.encode('utf-8'))
    modifiedSentence = clientSocket.recv(1024)
    print ("Desde el Servidor: " + modifiedSentence.decode('utf-8'))
    clientSocket.close()
