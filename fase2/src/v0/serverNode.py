from threading import Thread
from utilities import *

class ServerNode(Thread):

    # Constructor
    def __init__(self, port, table):
        Thread.__init__(self)
        self.port = port
        self.alcanzabilityTable = table
        print("ServerNode : Constructor :)")
    
    def run(self):
        print("ServerNode : Receiving shit and stuff!")
        print("ServerNode : I'm dying!")
