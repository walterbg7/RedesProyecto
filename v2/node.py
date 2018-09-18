import sys
import argparse
from threading import Thread
from socket import *

# Clases
class ClientNode():

    # Constructor
    def __init__(self):
        print("ClientNode : Constructor :)")

    # Ask the user for the message he/she wants to send to other nodes.
    # Fisrt we need to ask for the receiver node ip and port
    # Then we ask for the number of lines of the message(n)
    # Then we ask for each line of the message
    # Finally this method returns a str with the format desided((n)\n(<ip>/<mask>/<cost>)\n...)
    def askUserMessage():
        print("ClientNode : Give it to me!")
    
    # Pack the message given by the user in the requested format: n (2 bytes), ip (4 bytes), mask(1 byte), cost (3 bytes)
    # Returns the packed message
    def packMessage():
        print("ClientNode : Packing the message ...")

    # Send the packed message past by the user and send it to the destination also past by the user.	
    def sendMessage():
        print("ClientNode : Sending message")

class ClientNodeUDP():

    # Constructor
    def __init__(self):
        ClientNode.__init__(self)
        print("ClientNodeUDP : Constructor :)")

    # Overwrite father class send method

class ClientNodeTCP():

    #Constructor
    def __init__(self):
        ClientNode.__init__(self)
        print("ClientNodeTCP : Constructor :)")

    # Overwrite father class send method

class ServerNode(Thread):

    # Constructor
    def __init__(self, port):
        Thread.__init__(self)
        self.port = port
        # Missing alcanzability table field
        print("ServerNode : Constructor :(")
    
    def receiveMessage():
        print("ServerNode : Receiving shit and stuff!")

    def unpackMessage():
        print("ServerNode : Unpacking the message ...")

    # Update the alcanzavility table structure with the data of the recieved message
    # This method should be another thread by it self, one thread for conection    
    def proccessMessage():
        print("ServerNode : this thread is proccesing the message!")

class ServerNodeUDP(ServerNode):
    
    # Constructor
    def __init__(self, port):
        ServerNode.__init__(self, port)
        # Missing alcanzability table field
        print("ServerNodeUDP : Constructor :(")

    # Overwite the father class relevant methods!

class ServerNodeTCP(ServerNode):

    #Constructor
    def __init__(self, port):
        ServerNode.__init__(self, port)
        # Missing alcanzability table field
    print("ServerNodeTCP : Constructor :(")
    
    # Overwite the father class relevant methods!

class Node():
    
    # Constructor
    def __init__(self, nodeType, ip, mask, port):
        self.nodeType = nodeType
        self.ip = ip
        self.mask = mask
        self.port = port
        #self.alcanzabilityTable = decided structure
        print("Node (The real mvp!) : Constructor ")
    
    def printAlcanzabilityTable():
        print("Node : Table :v")    


    # This is the method that execute everything the program need to work
    def run():
        print("Node : I basically do everything")

# Program main funtion
if __name__ == '__main__':
    c0 = ClientNodeUDP()
    c1 = ClientNodeTCP()
    s0 = ServerNodeUDP(12000)
    s1 = ServerNodeTCP(5000)
    n0 = Node("PseudoBGP", "125.0.0.1", 30, 12000)

    print('Main Terminating...')	
