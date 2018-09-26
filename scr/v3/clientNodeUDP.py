from socket import *
from clientNode import *

class ClientNodeUDP(ClientNode):

    # Constructor
    def __init__(self, ip, port):
        ClientNode.__init__(self, ip, port)
        print("ClientNodeUDP : Constructor :)")

    # Overwrite father class send method
    def sendMessage(self, serverName, serverPort, message):
        # We need to send the message
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        #clientSocket.sendto(message.encode('utf-8'), (serverName, serverPort))
        clientSocket.sendto(message, (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        print ("From Server: " + modifiedMessage.decode('utf-8'))
        clientSocket.close()
