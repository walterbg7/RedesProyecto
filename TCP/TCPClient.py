from socket import *
serverName = "servername"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = input("Input lowercase sentence: ")
clientSocket.send(sentence)
modifiedSentence = clientSocket.recv(1024)
print ("From Server: " + modifiendSentence)
clientSocket.close()
