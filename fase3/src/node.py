import sys
import argparse
from utilities import *
from queue import *
from threading import *

class Node():

    # Constructor
    def __init__(self, ip, mask, port):
        self.ip = ip
        self.mask = mask
        self.port = port
        self.alcanzabilityTable = {}
        self.neighborsList = {}
        self.alcanzabilityTableLock = Lock()
        self.neighborsListLock = Lock()
        self.messageQueue = Queue()
        self.UDPSocket = socket(AF_INET, SOCK_DGRAM)
        self.UDPSocket.bind((self.ip, self.port))
        print("Node (The real mvp!) : Constructor")

    def askForNeighbors(self):
        print("Node (The real mvp!) : askForNeighbors")
        # We need to send a request message to the server dispatcher
        requestMessage = TypeMessage._make([REQUEST])
        encodedRequestMessage = encodeMessage(requestMessage)
        noNeighbors = True
        while(noNeighbors):
            self.UDPSocket.sendto(encodedRequestMessage, (SERVER_DISPATCHER_IP, SERVER_DISPATCHER_PORT))
            try:
                queueMessage = self.messageQueue.get(True, TIMEOUT)
            except Empty:
                print("Node (The real mvp!) Error: No answer from server dispatcher, how rude!")
                continue
            requestACKMessage = queueMessage[0]
            if(requestACKMessage.type == REQUEST_ACK):
                noNeighbors = False
                print(requestACKMessage.data)
                break
            else:
                print("Node (The real mvp!) Error: The recieved message was not a REQUEST_ACK message")
                continue
        # Once I know my neighbors, I can: start checking if they are alive, start sending actualizations


    def serverThread(self):
        print("Node (The real mvp!) : serverThread")
        while True:
            enodedMessage, senderAddr = self.UDPSocket.recvfrom(2048)
            message = decodeMessage(encodeMessage)
            if(message.type != BROADCAST):
                self.messageQueue.put((message, senderAddr))
            else:
                # If the message type is BROADCAST we need to process it immediately
                continue

    def printAlcanzabilityTable(self):
        self.alcanzabilityTableLock.acquire()
        print ("Alcanzability table : ")
        self.alcanzabilityTableLock.release()

    def printNeighborsList(self):
        self.neighborsListLock.acquire()
        print ("Neighbors list : ")
        print(str(self.neighborsList))
        self.neighborsListLock.release()

    def printMessageQueue(self):
        print ("Message queue : ")
        print(list(self.messageQueue.queue))

    def run(self):
        # We need to create the thread that will receive all the messages from the UDP socket
        serverThreadT = Thread(target=self.serverThread, args=())
        serverThreadT.daemon = True
        serverThreadT.start()
        # We need to create the thread that will ask for my neighbors
        askForNeighborsT = Thread(target=self.askForNeighbors, args=())
        askForNeighborsT.daemon = True
        askForNeighborsT.start()
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
            # Debugging
            elif(option == 18):
                self.printNeighborsList()
            elif(option == 19):
                self.printMessageQueue()
            else:
                print_error_option()
