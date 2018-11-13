from socket import *
from serverNode import *

class ServerNodeUDP(ServerNode):

    # Constructor
    def __init__(self, ip, mask, port, table):
        ServerNode.__init__(self, ip, mask, port, table)
        print("ServerNodeUDP : Constructor")
