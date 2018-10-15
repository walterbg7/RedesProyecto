from socket import *
from serverNode import *

class ServerNodeUDP(ServerNode):
    
    # Constructor
    def __init__(self, port, table, ip):
        ServerNode.__init__(self, port, table, ip)
        # Missing alcanzability table field
        fileLock.acquire()
        fileBi = open("bitacora.txt", 'r+')
        fileBi.read()
        fileBi.write("Server, ip: "+str(self.ip)+", port: "+str(self.port)+"\n")
        fileBi.write("Server is UDP\n")
        fileBi.write("\n\n")
        fileBi.close()
        fileLock.release()
        print("ServerNodeUDP : Constructor :)")

    # Overwite the father class relevant methods!
    def run(self):
        fileLock.acquire()
        fileBi = open("bitacora.txt", 'r+')
        fileBi.read()
        fileBi.write("Server, ip: "+str(self.ip)+", port: "+str(self.port)+"\n")
        fileBi.write("The server is ready to receive\n")
        fileBi.write("\n\n")
        fileBi.close()
        fileLock.release()
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
            fileLock.acquire()
            fileBi = open("bitacora.txt", 'r+')
            fileBi.read()
            fileBi.write("Server, ip: "+str(self.ip)+", port: "+str(self.port)+"\n")
            fileBi.write("New Message\n")
            fileBi.write("Client ip: " + str(clientAddress) + "\nClient message: " + message+"\n")
            fileBi.write("\n\n")
            fileBi.close()
            fileLock.release()
            #print("Client ip: " + str(clientAddress) + "\nClient message: " + message)
            # We need to create a thread to proccess the recived message
            conectionThread = Thread(target=self.proccessMessage, args=(clientAddress, message))
            conectionThread.start()
            serverSocket.sendto("✓✓".encode('utf-8'), clientAddress)
        print("ServerNode : I'm dying!")
