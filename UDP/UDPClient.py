from socket import *
serverName = "hotsname"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input("Input lowercase sentence: ")
clientSocket.sendto(message.encode('utf-8'), ("", serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print ("From Server: " + modifiedMessage.decode('utf-8'))
clientSocket.close()
