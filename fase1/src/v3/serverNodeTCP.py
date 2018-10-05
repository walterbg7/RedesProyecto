from socket import *
from serverNode import *

class ServerNodeTCP(ServerNode):

    #Constructor
    def __init__(self, port, table):
        ServerNode.__init__(self, port, table)
        # Missing alcanzability table field
        print("ServerNodeTCP : Constructor :)")
    
    # Overwite the father class relevant methods!
    def run(self):
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind(("", self.port))
        serverSocket.listen(1)
        print("ServerNode : Receiving shit and stuff!")
        while (1):
	        connectionSocket, addr = serverSocket.accept()
	        newConection = Thread(target=self.onNewClient, args = (connectionSocket, addr))
	        newConection.start()
        print("ServerNode : I'm dying!")

    def onNewClient(self, clientSocket, addrs):
       while(1):
            # We need to recieve the packed message from the client
            try:
                packedMessage, clientAddress = clientSocket.recvfrom(2048)
                # We need to unpack the recieved message             
                message = self.unpackMessage(packedMessage)
                print("Client ip: " + str(addrs) + "\nClient message: " + message)
                # We need to create a thread to proccess the recived message
                conectionThread = Thread(target=self.proccessMessage, args=(addrs, message))
                conectionThread.start()
                clientSocket.send("✓✓".encode('utf-8'))
                if(message == "0"):
                    connectionSocket.close()
                    break
            except Exception as e:
                print("The conection with",addrs,"has expired") 
                break
