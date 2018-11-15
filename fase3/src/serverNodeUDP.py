from socket import *
from serverNode import *
from queue import *

class ServerNodeUDP(ServerNode):

    # Constructor
    def __init__(self, ip, mask, port, table, listN):
        ServerNode.__init__(self, ip, mask, port, table, listN)
        self.serverSocket = socket(AF_INET, SOCK_DGRAM) #We create a UDP socket
        self.serverSocket.bind((self.ip, self.port))
        self.strNeighbors = ""
        self.ack_Queue = Queue()
        print("ServerNodeUDP : Constructor")

    def getNeighborsFromServer(self):
        # We create a neighbor request message
        message = Message._make([self.port, 60000, REQUEST, "".encode('utf-8')])
        encodedMessage = encodeMessage(message)
        noNeighbors = True
        while(noNeighbors):
            # Send the message to the dealer
            try:
                self.serverSocket.sendto(encodedMessage, (SERVERD_IP, SERVERD_PORT))
            except Exception as e:
                print("ServerNodeUDP : Error asking for my neighbors", str(e))
                continue
            # Wait for the answer
            try:
                modifiedMessage, serverAddress = self.serverSocket.recvfrom(2048)
            except:
                print("ServerNodeUDP : Error receiving message from serverDispatcher", str(e))
            recvMessage = decodeMessage(modifiedMessage)
            print ("ServerNodeUDP : From Dealer: ", recvMessage)
            if(recvMessage.flag == REQUEST_ACK):
                noNeighbors = False
                self.strNeighbors = recvMessage.data.decode('utf-8')
                myNeighborsTokens = self.strNeighbors.split(MESSAGES_DIVIDER)
                myNeighborsTokens.pop(len(myNeighborsTokens)-1)
                for ind in myNeighborsTokens:
                    myNeighborInfo =  ind.split(MESSAGE_PARTS_DIVIDER)
                    tupleK = (myNeighborInfo[0], int(myNeighborInfo[1]))
                    tupleV = (myNeighborInfo[2], False)
                    self.neighborsList[tupleK] = tupleV
                print(self.neighborsList)
            else:
                print("ServerNodeUDP : Error no REQUEST_ACK message")
                continue

    def contactNeighbors(self):
        for itr in self.neighborsList:
            contactNeighborsThread = Thread(target=self.contactNeighbor, args=(itr))
            contactNeighborsThread.start()

    def contactNeighbor(self, neighborIP, neighborPort):
        message = Message._make([self.port, neighborPort, KEEP_ALIVE, "Esta vivo?".encode('utf-8')])
        encodedMessage = encodeMessage(message)
        noACK = True
        numTimeOuts = 0
        numIter = 0
        # Send the message to the neighbor
        try:
            self.serverSocket.sendto(encodedMessage, (neighborIP, neighborPort))
        except Exception as e:
            print("ServerNodeUDP : Error contacting the neighbor", str(e))
        while(noACK and numTimeOuts < 4 and numIter < 3):
            # Wait for the answer
            try:
                recvMessage = self.ack_Queue.get(True, 5)
            except Empty:
                print("ServerNodeUDP : Error receiving message from neighbor")
                numTimeOuts += 1
                # Send the message to the neighbor
                try:
                    self.serverSocket.sendto(encodedMessage, (neighborIP, neighborPort))
                except Exception as e:
                    print("ServerNodeUDP : Error contacting the neighbor", str(e))
                    numIter += 1
                continue
            print ("ServerNodeUDP : From Neighbor: ", recvMessage)
            if(recvMessage.flag == NORMAL_ACK and recvMessage.originPort == neighborPort):
                noACK = False
                tupleK = (neighborIP, neighborPort)
                oldTupleV = self.neighborsList.get(tupleK)
                if(oldTupleV is None):
                    print("Algo anda mal")
                    #print(tupleK)
                else:
                    print("******* Node: "+str(tupleK)+" is Alive *******")
                    tupleV = (oldTupleV[0], True)
                    self.neighborsList[tupleK] = tupleV
            else:
                self.ack_Queue.put(recvMessage)
                print("ServerNodeUDP : Error no ACK message from the neighbor")

    def run(self):
        self.getNeighborsFromServer()
        contactNeighborsThread = Thread(target=self.contactNeighbors, args=())
        contactNeighborsThread.start()
        print("ServerNodeUDP : Receiving stuff")
        while(1):
            # We need to recieve the packed message from the client
            packedMessage, clientAddress = self.serverSocket.recvfrom(2048)
            # We need to decode the recieved message
            message = decodeMessage(packedMessage)
            redirectMessageThread = Thread(target=self.redirectMessage, args=(message, clientAddress[0]))
            redirectMessageThread.start()
            continue

    def redirectMessage(self, message, clientIP):
        if(message.flag == KEEP_ALIVE):
            clientAddress = (clientIP, int(message.originPort))
            print("From ODIN: "+str(message))
            #Proccess the message
            messageACK = Message._make([self.port, clientAddress[1], NORMAL_ACK, "Si estoy vivo".encode('utf-8')])
            ackMessage = encodeMessage(messageACK) #We need to decode the message
            self.serverSocket.sendto(ackMessage, clientAddress)
        else:
            if(message.flag == NORMAL_ACK):
                self.ack_Queue.put(message)
