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
        print("ClientNodeUDP : Sending stuff!")
