from socket import *
from serverNode import *

class ServerNodeUDP(ServerNode):

    # Constructor
    def __init__(self, port, table, ip):
        ServerNode.__init__(self, port, table, ip)
        # Missing alcanzability table field
        strB = "Server is UDP"
        writeOnBita(strB, self.strH)
        print("ServerNodeUDP : Constructor :)")

    # Overwite the father class relevant methods!
    def run(self):
        strB = "The server is ready to receive"
        writeOnBita(strB, self.strH)
        print("ServerNode : Receiving shit and stuff!")
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(("", self.port))
        print ("The server is ready to receive")
        while (1):
            # We need to recieve the packed message from the client
            packedMessage, clientAddress = serverSocket.recvfrom(2048)
            # We need to unpack the recieved message
            #message = self.unpackMessage(packedMessage.decode('utf-8'))
            message = self.unpackMessage(packedMessage)
            strB = "Client ip: " + str(clientAddress) + "\nClient message: " + message
            writeOnBita(strB, self.strH)
            #print("Client ip: " + str(clientAddress) + "\nClient message: " + message)
            # We need to create a thread to proccess the recived message
            conectionThread = Thread(target=self.proccessMessage, args=(clientAddress, message))
            conectionThread.start()
            serverSocket.sendto("✓✓".encode('utf-8'), clientAddress)
        print("ServerNode : I'm dying!")
