from utilities import *

class ClientNode():

    # Constructor
    def __init__(self, ip, mask, port):
        self.ip = ip
        self.mask = mask
        self.port = port
        print("ClientNode : Constructor")
        pass

    def packMessage(self, packedMessage):
        pass

    # Send the packed message past by the user and send it to the destination also past by the user.
    def sendMessage(self, serverName, serverPort, message):
        pass

    def run(self):
        pass

    def stop(self):
        pass
