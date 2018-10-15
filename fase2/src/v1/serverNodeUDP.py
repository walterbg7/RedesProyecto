from socket import *
from serverNode import *

class ServerNodeUDP(ServerNode):
    
    # Constructor
    def __init__(self, port, table):
        ServerNode.__init__(self, port, table)
        print("ServerNodeUDP : Constructor :)")

    # Overwite the father class relevant methods!
    def run(self):
        print("ServerNode : Receiving shit and stuff!")
