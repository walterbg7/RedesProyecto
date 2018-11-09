from threading import Thread
from utilities import *

class ServerNode(Thread):

    # Constructor
    def __init__(self, port, table, ip):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.alcanzabilityTable = table
        self.strH = "ServerNode : ip: "+str(self.ip)+", port: "+str(self.port)
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
