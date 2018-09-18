import sys
import argparse
from threading import Thread
from socket import *
from utilities import *

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
    def askUserMessage(self):
        print("ClientNode : Give it to me!")
    
    # Pack the message given by the user in the requested format: n (2 bytes), ip (4 bytes), mask(1 byte), cost (3 bytes)
    # Returns the packed message
    def packMessage(self):
        print("ClientNode : Packing the message ...")

    # Send the packed message past by the user and send it to the destination also past by the user.	
    def sendMessage(self):
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
    
    def receiveMessage(self):
        print("ServerNode : Receiving shit and stuff!")

    def unpackMessage(self):
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
    def __init__(self, isPseudoBGP, ip, mask, port):
        self.isPseudoBGP = isPseudoBGP
        self.ip = ip
        self.mask = mask
        self.port = port
        #self.alcanzabilityTable = decided structure
        print("Node (The real mvp!) : Constructor ")
    
    def printAlcanzabilityTable(self):
        print("Node : Table :v")    

    # This is the method that execute everything the program need to work
    def run(self):
        print("Node : I basically do everything")

# Program main funtion
if __name__ == '__main__':
    # We need to parse the arguments pass by the user
    parser = argparse.ArgumentParser(description='choose the type of node you want to use')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-tcp", "--pseudoBGP", action="store_true")
    group.add_argument("-udp", "--intAS", action="store_true")
    parser.add_argument("ip", help="recive the node ip address")
    parser.add_argument("mask", help="recive the subnet mask, it must be a integer between 8 and 30", type=int)
    parser.add_argument("port", help="recive the server port number", type=int)
    args = parser.parse_args()
    print ("ip address: " + args.ip + "\nsubnet mask: " + str(args.mask) + "\nport number: " + str(args.port))

    # We need to make sure the arg pass by the user are valid

    # We need to check if the user select a node type
    if(not args.pseudoBGP and not args.intAS):
        # If the user did not select a node type, the node type will be pseudoBGP by default
        args.pseudoBGP = True

    # We need to check if the subnet mask pass by the user is valid, ie is in the range [8, 30]
    if(args.mask < 8 or args.mask > 30):
        print_error_invalid_mask()
        sys.exit(-1)
    print ("The provided subnet mask is valid! Hooray!")

    # We need to check if the port pass by the user is valid, ie is in the range [1, 65535]
    if(args.port < 0 or args.port > 65535):
        print_error_invalid_port()
        sys.exit(-1)
    print ("The provided port is valid! Hooray!")

    # We need to check if the ip address pass by the user is a valid ip address
    if(not validate_ip_address(args.ip)):
        print_error_invalid_ip()
        sys.exit(-1)
    print ("The provided ip address is valid! Hooray!")

    # If all the arguments pass by the user are valid, we continue creating the node and executing it
    node = Node(args.pseudoBGP, args.ip, args.mask, args.port)
    node.run()

    print('Main Terminating...')	
