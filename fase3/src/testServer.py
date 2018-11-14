from utilities import *
from socket import *


message = Message._make([12000, 60000, REQUEST, "nada".encode('utf-8')])

clientSocket = socket(AF_INET, SOCK_DGRAM) #We create a UDP socket
clientSocket.bind(("127.0.0.1", 12000))

message1 = encodeMessage(message)
clientSocket.sendto(message1, ("127.0.0.1", 60000))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print ("From Server: ", decodeMessage(modifiedMessage))
clientSocket.close()
