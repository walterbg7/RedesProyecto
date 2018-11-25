import sys
import argparse
import time
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
        encodedRequestMessage = encode_message(requestMessage)
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
                for it in  requestACKMessage.data:
                    self.neighborsList[(it[0], it[2])] = [it[1], it[3], False, 0]
                break
            else:
                print("Node (The real mvp!) Error: The recieved message was not a REQUEST_ACK message")
                continue
        # Once I know my neighbors, I can: start checking if they are alive, start sending actualizations
        aNITAAThread = Thread(target=self.askNeighborsIfTheyAreAlive, args=())
        aNITAAThread.daemon = True
        aNITAAThread.start()
        sendActualizationsThread = Thread(target=self.sendActualizations, args=())
        sendActualizationsThread.daemon = True
        sendActualizationsThread.start()
        processRecvMessagesThread = Thread(target=self.processRecvMessages, args=())
        processRecvMessagesThread.daemon = True
        processRecvMessagesThread.start()

    def askNeighborsIfTheyAreAlive(self):
        print("Node (The real mvp!) : askNeighborsIfTheyAreAlive")
        while True:
            # For each neighbor in the neighbors list, I need to send it a keep alive message
            for k in self.neighborsList:
                if(self.neighborsList[k][3] == MAX_NUMBER_OF_TRIES):
                    if(self.neighborsList[k][2] == True):
                        # If the neighbor has died, we need to start a broadcast
                        self.neighborsList[k][2] = False
                        self.neighborsList[k][3] = 0
                    else:
                        # If the neighbors did not wake up, I stop bothering it
                        print("Node (The real mvp!) : <"+str(k)+"> has not wake up, lazy f#ck!")
                else:
                    print(str(k))
                    self.neighborsList[k][3] += 1
                    keepAliveMessage = TypeMessage._make([KEEP_ALIVE])
                    encodedKeepAliveMessage = encode_message(keepAliveMessage)
                    self.UDPSocket.sendto(encodedKeepAliveMessage, k)
            time.sleep(KEEP_ALIVE_RATE)


    def sendActualizations(self):
        pass

    def processRecvMessages(self):
        print("Node (The real mvp!) : processRecvMessages")
        while True:
            queueMessage = self.messageQueue.get()
            message = queueMessage[0]
            senderAddr = queueMessage[1]
            if(message.type == KEEP_ALIVE):
                neighborData = self.neighborsList.get(senderAddr)
                if(neighborData != None):
                    keepAliveACKMessage = TypeMessage._make([KEEP_ALIVE_ACK])
                    encodedKeepAliveACKMessage = encode_message(keepAliveACKMessage)
                    self.UDPSocket.sendto(encodedKeepAliveACKMessage, senderAddr)
                    if(neighborData[2]==False):
                        neighborData[2] = True
                        neighborData[3] = 0
                else:
                    print("Node (The real mvp!) Error : Keep alive message from invalid neighbor!")
            elif(message.type == KEEP_ALIVE_ACK):
                neighborData = self.neighborsList.get(senderAddr)
                if(neighborData != None):
                    neighborData[3] = 0
                else:
                    print("Node (The real mvp!) Error : Keep alive ack message from invalid neighbor!")
            else:
                self.messageQueue.put(queueMessage)

    def serverThreadHelper(self, encodedMessage, senderAddr):
        print("Node (The real mvp!) : serverThreadHelper")
        message = decode_message(encodedMessage)
        if(message != None):
            if(message.type != BROADCAST):
                if(ignoring):
                    if(message.type != ACTUALIZATION and message.type != PURE_DATA):
                        self.messageQueue.put((message, senderAddr))
                    else:
                        print("Node (The real mvp!) : Ignoring this message <"+str(message)+">")
                else:
                    self.messageQueue.put((message, senderAddr))
            else:
                # If the message type is BROADCAST we need to process it immediately
                pass

    def serverThread(self):
        print("Node (The real mvp!) : serverThread")
        while True:
            encodedMessage, senderAddr = self.UDPSocket.recvfrom(2048)
            serverThreadHelperT = Thread(target=self.serverThreadHelper, args=(encodedMessage, senderAddr))
            serverThreadHelperT.daemon = True
            serverThreadHelperT.start()

    def printAlcanzabilityTable(self):
        self.alcanzabilityTableLock.acquire()
        print ("Alcanzability table : ")
        self.alcanzabilityTableLock.release()

    def printNeighborsList(self):
        self.neighborsListLock.acquire()
        print ("Neighbors list : ")
        for k in self.neighborsList:
            print(str(k)+" : "+str(self.neighborsList[k]))
        self.neighborsListLock.release()

    def printMessageQueue(self):
        print ("Message queue : ")
        for ind in list(self.messageQueue.queue):
            print(ind)

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
