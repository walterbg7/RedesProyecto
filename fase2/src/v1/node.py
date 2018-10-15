import sys
import argparse
from utilities import *
from clientNodeUDP import *
from serverNodeUDP import *

class Node():
    
    # Constructor
    def __init__(self, isPseudoBGP, ip, port):
        self.isPseudoBGP = isPseudoBGP
        self.ip = ip
        self.port = port
        self.alcanzabilityTable = {}
        print("Node (The real mvp!) : Constructor ")

    # This is the method that execute everything the program need to work
    def run(self):
        #print("Node : I basically do everything")
        # We need to create the corresponding client node and server node
        
        # I always create an UDP node, because it's fase two!
        self.serverNode = ServerNodeUDP(self.port, self.alcanzabilityTable)
        self.clientNode = ClientNodeUDP(self.ip, self.port)

        # We need to put the server instance (thread) to run concurrently
        self.serverNode.daemon = True
        self.serverNode.start()
        # We need to start the interaction with the user
        beingDeleted = False
        while(not beingDeleted):
            option = input(clientMenu)
            try:
                option = int(option)
            except ValueError:
                print_error_option()
            if(option == 0):
                self.clientNode.stop()
                beingDeleted = True
            elif(option == 1):
                self.clientNode.run()
            else:
                print_error_option()


# Program main funtion
if __name__ == '__main__':
    # We need to parse the arguments pass by the user
    parser = argparse.ArgumentParser(description='choose the type of node you want to use')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-tcp", "--pseudoBGP", action="store_true")
    group.add_argument("-udp", "--intAS", action="store_true")
    parser.add_argument("ip", help="recive the node ip address")
    parser.add_argument("port", help="recive the server port number", type=int)
    args = parser.parse_args()
    print ("ip address: " + args.ip + "\nport number: " + str(args.port))

    # We need to make sure the arg pass by the user are valid

    # We need to check if the user select a node type
    if(not args.pseudoBGP and not args.intAS):
        # If the user did not select a node type, the node type will be pseudoBGP by default
        args.intAS = True

    # We need to check if the subnet mask pass by the user is valid, ie is in the range [8, 30]
    #if(args.mask < 8 or args.mask > 30):
    #    print_error_invalid_mask()
    #    sys.exit(-1)
    #print ("The provided subnet mask is valid! Hooray!")

    # We need to check if the port pass by the user is valid, ie is in the range [1, 65535]
    if(args.port < 0 or args.port > 65535):
        print_error_invalid_port()
        sys.exit(-1)
    print ("The provided port is valid! Hooray!")

    # We need to check if the ip address pass by the user is a valid ip address
    if(is_valid_ipv4_address(args.ip)):
        print ("The provided ip address is valid! Hooray!")
    else:
        print_error_invalid_ip()
        sys.exit(-1)

    # If all the arguments pass by the user are valid, we continue creating the node and executing it
    node = Node(args.pseudoBGP, args.ip, args.port)
    node.run()

    print('Main Terminating...')
