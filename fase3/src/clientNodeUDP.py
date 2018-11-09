from socket import *
from clientNode import *

class ClientNodeUDP(ClientNode):

    # Constructor
    def __init__(self, ip, port):
        ClientNode.__init__(self, ip, port)
        print("ClientNodeUDP : Constructor")
