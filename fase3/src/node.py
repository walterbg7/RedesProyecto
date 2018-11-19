import sys
import argparse
from utilities import *
from threading import Thread

class Node():

    # Constructor
    def __init__(self, ip, mask, port):
        self.ip = ip
        self.mask = mask
        self.port = port
        self.alcanzabilityTable = {}
        self.neighborsList = {}
        self.header = "Node (The real mvp!) : ip: "+self.ip+", mask: "+str(self.mask)+", port: "+str(self.port)
        self.UDPSocket = socket(AF_INET, SOCK_DGRAM)
        self.UDPSocket.bind((self.ip, self.port))
        print("Node (The real mvp!) : Constructor")

    def printAlcanzabilityTable(self):
        aTLock.acquire()
        print ("Alcanzability Table: ")
        aTLock.release()

    def askForNeighbors(self):
        # I need to create a REQUEST message and send it to the server dispatcher
        requestMessage = Message._make([REQUEST, None, None])
        encodedRequestMessage = encodeMessage(requestMessage)
        # I need to send the REQUEST message to the server and wait for the REQUEST_ACK message
        noNeighbors = True
        while(noNeighbors):
            try:
                self.UDPSocket.sendto(encodedRequestMessage, (SERVER_DISPATCHER_IP, SERVER_DISPATCHER_PORT))
            except Exception as e:
                writeOnLog("Node (The real mvp!) : Error asking for my neighbors " + str(e), self.header)
                continue
            try:
                encodedRecvMessage, serverDispatcherAddress = self.UDPSocket.recvfrom(2048)
            except:
                writeOnLog("Node (The real mvp!) : Error receiving message from server dispatcher " + str(e), self.header)
            recvMessage = decodeMessage(encodedRecvMessage)
            writeOnLog("Node (The real mvp!) : From server: " + str(recvMessage), self.header)
            if(recvMessage.flag == REQUEST_ACK):
                noNeighbors = False
                myNeighbors = recvMessage.data.decode('utf-8')
                myNeighborsTokens = myNeighbors.split(MESSAGE_LINES_DIVIDER)
                for ind in myNeighborsTokens:
                    myNeighborTokens = ind.split(MESSAGE_PARTS_DIVIDER)
                    try:
                        myNeighborIP = myNeighborTokens[0]
                        myNeighborMask = int(myNeighborTokens[1])
                        myNeighborPort = int(myNeighborTokens[2])
                        myNeighborCost = int(myNeighborTokens[3])
                        self.neighborsList[(myNeighborIP, myNeighborPort)] = (myNeighborMask, myNeighborCost, False)
                    except Exception as e:
                        continue
            else:
                writeOnLog("Node (The real mvp!) : Error no REQUEST_ACK message", self.header)
                continue

    def serverThread(self):
        writeOnLog("Node (The real mvp!) : serverThread", self.header)
        # First I need to ask the server dispatcher for my neighbors
        self.askForNeighbors()
        # Once I know my neighbors I need create the thread that check if they are alive
        # I need to create a thread that check the status of my neighbors and send actualizations
        # Finnally I need to keep receiving messages from my UDP port and process them by their flag 

    # This is the method that execute everything the program need to work
    def run(self):
        #print("Node : I basically do everything")
        # We need to put the server instance (thread) to run concurrently
        serverT = Thread(target=self.serverThread, args=())
        serverT.daemon = True
        serverT.start()
        # We need to start the interaction with the user
        beingDeleted = False
        while(not beingDeleted):
            option = input(clientMenu)
            try:
                option = int(option)
            except ValueError:
                print_error_option()
            if(option == 0):
                beingDeleted = True
            elif(option == 1):
                print("This option is temporarily disabled")
            elif(option == 2):
                self.printAlcanzabilityTable()
            else:
                print_error_option()


# Program main funtion
if __name__ == '__main__':
    # We need to parse the arguments pass by the user
    parser = argparse.ArgumentParser(description='this program create a node with the recived arguments as input')
    parser.add_argument("ip", help="recive the node ip address")
    parser.add_argument("mask", help="recive the node subnet mask", type=int)
    parser.add_argument("port", help="recive the server port number", type=int)
    args = parser.parse_args()
    print ("Node : ip address: " + args.ip + ", port number: " + str(args.port))

    # We need to make sure the arg pass by the user are valid

    # We need to check if the ip address pass by the user is a valid ip address
    if(is_valid_ipv4_address(args.ip)):
        print ("The provided ip address is valid! Hooray!")
    else:
        print_error_invalid_ip()
        sys.exit(-1)

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

    # If all the arguments pass by the user are valid, we continue creating the node and executing it
    node = Node(args.ip, args.mask, args.port)
    node.run()

    print('Main Terminating...')
