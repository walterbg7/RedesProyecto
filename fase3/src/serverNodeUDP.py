from socket import *
from serverNode import *

class ServerNodeUDP(ServerNode):

    # Constructor
    def __init__(self, port, table, ip):
        ServerNode.__init__(self, port, table, ip)
        print("ServerNodeUDP : Constructor")
