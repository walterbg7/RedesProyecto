from socket import *
from clientNode import *

class ClientNodeUDP(ClientNode):

    # Constructor
    def __init__(self, ip, mask, port):
        ClientNode.__init__(self, ip, mask, port)
        print("ClientNodeUDP : Constructor")
