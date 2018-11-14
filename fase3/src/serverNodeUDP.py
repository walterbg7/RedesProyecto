from socket import *
from serverNode import *

class ServerNodeUDP(ServerNode):

    # Constructor
    def __init__(self, ip, mask, port, table, listN):
        ServerNode.__init__(self, ip, mask, port, table, listN)
        print("ServerNodeUDP : Constructor")

    def run(self):
        clientSocket = socket(AF_INET, SOCK_DGRAM) #We create a UDP socket
        clientSocket.bind((self.ip, self.port))
        #We create a neighbor request message
        message = Message._make([self.port, 60000, 1, "".encode('utf-8')])
        message1 = encodeMessage(message)
        #Send the message to the dealer
        clientSocket.sendto(message1, ("127.0.0.1", 60000))
        #Wait for the answer
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        recvMessage = decodeMessage(modifiedMessage)
        print ("From Dealer: ", recvMessage)
        myNeighbors = recvMessage.data.decode('utf-8')
        myNeighborsList = myNeighbors.split(" ")
        #We Need to eliminate the last element in the list
        myNeighborsList.pop(len(myNeighborsList)-1)
        print ("My Neighbors: ", str(myNeighborsList))
        for i in myNeighborsList:
            neighborInfo = i.split("/")
            tupleNeighbor = (neighborInfo[0], neighborInfo[1], neighborInfo[2], "Inactive")
            self.neighborsList.append(tupleNeighbor)
        print(self.neighborsList)
        pass
