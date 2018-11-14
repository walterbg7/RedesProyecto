from threading import Thread
from utilities import *

class ServerNode(Thread):

    # Constructor
    def __init__(self, ip, mask, port, table, nList):
        Thread.__init__(self)
        self.ip = ip
        self.mask = mask
        self.port = int(port)
        self.alcanzabilityTable = table
        self.neighborsList = nList
        self.strH = "ServerNode : ip: "+self.ip+", port: "+str(self.mask)+", port: "+str(self.port)
        print("ServerNode : Constructor")

    def unpackMessage(self, packedMessage):
        pass

    # Update the alcanzavility table structure with the data of the recieved message
    # This method should be another thread by it self, one thread for conection
    def proccessMessage(self, clientAddr, msj):
        pass

    def run(self):
        pass

    def stop(self):
        pass
