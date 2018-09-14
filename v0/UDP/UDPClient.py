from socket import *
serverName = str(input("Ingrese un ip, please: "))
serverPort = int(input("Ingrese un puerto, please: "))
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input("Input lowercase sentence: ")
clientSocket.sendto(message.encode('utf-8'), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print ("From Server: " + modifiedMessage.decode('utf-8'))
clientSocket.close()
