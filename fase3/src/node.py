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

    def startBroadcast(self, numberOfJumpsLeft):
        print("Node (The real mvp!) : startBroadcast")
        if(numberOfJumpsLeft > 0):
            for k in self.neighborsList:
                broadcastMessage = BroadcastMessage._make([BROADCAST, numberOfJumpsLeft])
                encodedBroadcastMessage = encode_message(broadcastMessage)
                self.UDPSocket.sendto(encodedBroadcastMessage, k)


    def askNeighborsIfTheyAreAlive(self):
        print("Node (The real mvp!) : askNeighborsIfTheyAreAlive")
        while True:
            # For each neighbor in the neighbors list, I need to send it a keep alive message
            self.neighborsListLock.acquire()
            for k in self.neighborsList:
                if(self.neighborsList[k][3] == MAX_NUMBER_OF_TRIES):
                    if(self.neighborsList[k][2] == True):
                        # If the neighbor has died, we need to start a broadcast
                        self.neighborsList[k][2] = False
                        self.neighborsList[k][3] = 0
                        self.startBroadcast(BROADCAST_JUMPS)
                    else:
                        # If the neighbors did not wake up, I stop bothering it
                        print("Node (The real mvp!) : <"+str(k)+"> has not wake up, lazy f#ck!")
                else:
                    print(str(k))
                    self.neighborsList[k][3] += 1
                    keepAliveMessage = TypeMessage._make([KEEP_ALIVE])
                    encodedKeepAliveMessage = encode_message(keepAliveMessage)
                    self.UDPSocket.sendto(encodedKeepAliveMessage, k)
            self.neighborsListLock.release()
            time.sleep(KEEP_ALIVE_RATE)


    def sendActualizations(self):
        print("Node (The real mvp!) : sendActualizations")
        while True:
            self.neighborsListLock.acquire()
            self.alcanzabilityTableLock.acquire()
            for neighbor in self.neighborsList:
                neighborData = self.neighborsList[neighbor]
                if(neighborData[2] == True):
                    # If the neighbor is alive, I can try to send it a actualization message
                    n = 0
                    data = []
                    for aTEntry in self.alcanzabilityTable:
                        aTEntryData = self.alcanzabilityTable[aTEntry]
                        if(aTEntry != neighbor):
                            n += 1
                            data.append((aTEntry[0], aTEntryData[0], aTEntry[1], (aTEntryData[2] + neighborData[1])))
                    if(n > 0):
                        # If I could create a actualization message I need to send it
                        actualizationMessage = ActualizationMessage._make([ACTUALIZATION, n, data])
                        encodedActualizationMessage = encode_message(actualizationMessage)
                        self.UDPSocket.sendto(encodedActualizationMessage, neighbor)
            self.neighborsListLock.release()
            self.alcanzabilityTableLock.release()
            time.sleep(ACTUALIZATION_RATE)

    def addNeigborToAlcanzabilityTable(self, neighbor):
        print("Node (The real mvp!) : addNeigborToAlcanzabilityTable")
        self.alcanzabilityTableLock.acquire()
        neighborData = self.neighborsList[neighbor]
        if(not(neighbor in self.alcanzabilityTable)):
            self.alcanzabilityTable[neighbor] = (neighborData[0], None, neighborData[1])
        else:
            actualNeighborData = self.alcanzabilityTable[neighbor]
            if(actualNeighborData[2] > neighborData[1]):
                self.alcanzabilityTable[neighbor] = (neighborData[0], None, neighborData[1])
        self.alcanzabilityTableLock.release()

    def processRecvMessages(self):
        print("Node (The real mvp!) : processRecvMessages")
        while True:
            queueMessage = self.messageQueue.get()
            message = queueMessage[0]
            senderAddr = queueMessage[1]
            if(message.type == KEEP_ALIVE):
                self.neighborsListLock.acquire()
                neighborData = self.neighborsList.get(senderAddr)
                if(neighborData != None):
                    keepAliveACKMessage = TypeMessage._make([KEEP_ALIVE_ACK])
                    encodedKeepAliveACKMessage = encode_message(keepAliveACKMessage)
                    self.UDPSocket.sendto(encodedKeepAliveACKMessage, senderAddr)
                    if(neighborData[2] == False):
                        neighborData[2] = True
                        neighborData[3] = 0
                        self.addNeigborToAlcanzabilityTable(senderAddr)
                else:
                    print("Node (The real mvp!) Error : Keep alive message from invalid neighbor!")
                self.neighborsListLock.release()
            elif(message.type == KEEP_ALIVE_ACK):
                self.neighborsListLock.acquire()
                neighborData = self.neighborsList.get(senderAddr)
                if(neighborData != None):
                    if(neighborData[2] == False):
                        neighborData[2] = True
                        # I need to add this neighbor to the alcanzabilityTable (is it aplies)
                        self.addNeigborToAlcanzabilityTable(senderAddr)
                    neighborData[3] = 0
                else:
                    print("Node (The real mvp!) Error : Keep alive ack message from invalid neighbor!")
                self.neighborsListLock.release()
            elif(message.type == ACTUALIZATION):
                neighborData = self.neighborsList.get(senderAddr)
                if(neighborData != None):
                    self.alcanzabilityTableLock.acquire()
                    for ind in message.data:
                        if((ind[0], ind[2]) in self.alcanzabilityTable):
                            # If I already know this node, I need to check if it's cost is less than my actual cost, If it is I need to replace it
                            actualATEntryData = self.alcanzabilityTable[(ind[0], ind[2])]
                            if(ind[3] < actualATEntryData[2]):
                                self.alcanzabilityTable[(ind[0], ind[2])] = (ind[1], (senderAddr[0], neighborData[0], senderAddr[1]), ind[3])
                        else:
                            # If I did not know this node I simply add it to the alcanzabiliy table
                            self.alcanzabilityTable[(ind[0], ind[2])] = (ind[1], (senderAddr[0], neighborData[0], senderAddr[1]), ind[3])
                    self.alcanzabilityTableLock.release()
                else:
                    print("Node (The real mvp!) Error : Actualization message from invalid neighbor!")
            elif(message.type == COST_CHANGE):
                self.neighborsListLock.acquire()
                neighborData = self.neighborsList.get(senderAddr)
                if(neighborData != None): #This is a option for error control
                    oldCost = neighborData[1]
                    neighborData[1] = message.cost #we register a new cost
                    self.addNeigborToAlcanzabilityTable(senderAddr)
                    if(message.cost > oldCost):
                        self.startBroadcast(BROADCAST_JUMPS)
                else:
                    print("Node (The real mvp!) Error : Invalid Cost Change Message!")
                self.neighborsListLock.release()
            else:
                self.messageQueue.put(queueMessage)

    def costChange(self):
        print("Write the address to cost change")
        goodData = False
        ip = input("IP: ") #We need the neighbor ip
        if(not is_valid_ipv4_address(ip)):
            print("Error: Invalid ip address")
        else:
            port = input("Port: ") #We need the neighbor port
            try:
                portInt = int(port)
            except ValueError:
                print_error_invalid_port()
            else:
                if(portInt < 0 or portInt > 65535):
                    print_error_invalid_port()
                else:
                    goodData = True
        if(goodData):     #If the data is good, we continue
            cost = input ("New Cost: ")
            try: 
                intCost = int(cost) #We need the new cost
            except ValueError:
                 print_error_invalid_cost()
            else:
                if(intCost < 20 or intCost > 100): #Validate the cost
                    print_error_invalid_cost()
                else:
                    link = (ip, int(port))  #We need the link 
                    costChangeMessage = CostChangeMessage._make([COST_CHANGE, intCost])
                    encodedCostChangeMessage = encode_message(costChangeMessage)
                    self.UDPSocket.sendto(encodedCostChangeMessage, link)
                    self.neighborsList[link][1] = intCost
                    neighborMask = self.neighborsList[link][0]
                    print(self.alcanzabilityTable[link])
                    self.addNeigborToAlcanzabilityTable(link) #We need the key of the neihgbor
                    print("Nice Job, take a cookie")

    def talkToTheHand(self):
        print("Node (The real mvp!) : talkToTheHand")
        global ignoring
        if(not ignoring):
            ignoring = True
            time.sleep(IGNORING_TIME)
            ignoring = False
            for neighbor in self.neighborsList:
                if(self.neighborsList[neighbor][2] == True):
                    self.addNeigborToAlcanzabilityTable(neighbor)

    def serverThreadHelper(self, encodedMessage, senderAddr):
        print("Node (The real mvp!) : serverThreadHelper")
        message = decode_message(encodedMessage)
        if(message != None):
            if(message.type != BROADCAST):
                global ignoring
                if(ignoring):
                    if(message.type != ACTUALIZATION and message.type != PURE_DATA):
                        self.messageQueue.put((message, senderAddr))
                    else:
                        print("\n\n\nNode (The real mvp!) : Ignoring this message <"+str(message)+">\n\n\n")
                else:
                    self.messageQueue.put((message, senderAddr))
            else:
                print("\n\n\nBroadcast!"+str(message.n)+"\n\n\n")
                # If the message type is BROADCAST we need to process it immediately
                # I need to start the "talk to the hand" thread
                talkToTheHandThread = Thread(target=self.talkToTheHand, args=())
                talkToTheHandThread.daemon = True
                talkToTheHandThread.start()
                # I need to empty the message queue and the alcanzability table (only if they are not already empty)
                with self.messageQueue.mutex:
                    self.messageQueue.queue.clear()
                self.alcanzabilityTableLock.acquire()
                if(bool(self.alcanzabilityTable)):
                    self.alcanzabilityTable.clear()
                self.alcanzabilityTableLock.release()
                # I need to propagate the broadcast message
                self.startBroadcast(message.n - 1)

    def serverThread(self):
        print("Node (The real mvp!) : serverThread")
        while True:
            encodedMessage, senderAddr = self.UDPSocket.recvfrom(2048)
            serverThreadHelperT = Thread(target=self.serverThreadHelper, args=(encodedMessage, senderAddr))
            serverThreadHelperT.daemon = True
            serverThreadHelperT.start()

    def printAlcanzabilityTable(self):
        self.alcanzabilityTableLock.acquire()
        print ("Alcanzability table : ['Who' : 'Through' : 'Cost']")
        for k in self.alcanzabilityTable:
            print("("+str(k[0])+", "+str(self.alcanzabilityTable[k][0])+", "+str(k[1])+")"+" : "+str(self.alcanzabilityTable[k][1])+" : "+str(self.alcanzabilityTable[k][2]))
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
                self.costChange()
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
