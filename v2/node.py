import sys
import argparse
import threading
from threading import Thread
from socket import *
from utilities import *

# Clases
############################################# Clients #############################################
class ClientNode():

    # Constructor
    def __init__(self):
        print("ClientNode : Constructor :)")

    # Ask the user for the message he/she wants to send to other nodes.
    # First we ask for the number of lines of the message(n)
    # Then we ask for each line of the message
    # Finally this method returns a str with the format desided((n)\n(<ip>/<mask>/<cost>)\n...)
    def askUserMessage(self):
        print("ClientNode : Give it to me!")
        print(askClientMessage)
        n = input(askNMessage)
        try:
            n = int(n)
        except ValueError:
            print_error_invalid_n()
            return
        clientMessage = ""
        clientMessage += str(n) + "/"
        for i in range (n):
            clientMessage += input("l: ") + "/"
        return clientMessage
    
    # Pack the message given by the user in the requested format: n (2 bytes), ip (4 bytes), mask(1 byte), cost (3 bytes)
    # Returns the packed message
    def packMessage(self, message):
        print("ClientNode : Packing the message ...")
        return message

    # Send the packed message past by the user and send it to the destination also past by the user.	
    def sendMessage(self, serverName, serverPort, message):
        print("ClientNode : Sending message")

    def run(self):
        print("ClientNode : Running!")
        print("ClientNodeUDP : Sending message")
        # First we need to ask the user who do he/she wants to send the message
        serverName = input(askIPAddressMessage)
        serverPort = int(input(askPortMessage))
        # We need to verify the ip address and port number past by the user?

        # We need to ask the user for the message he/she wants to send
        userMessage = self.askUserMessage()
        print(userMessage)
        
        # We need to pack the message in order to send it
        packedMessage = self.packMessage(userMessage)
        print(packedMessage)

        # We need to sent the message
        self.sendMessage(serverName, serverPort, packedMessage)

class ClientNodeUDP(ClientNode):

    # Constructor
    def __init__(self):
        ClientNode.__init__(self)
        print("ClientNodeUDP : Constructor :)")

    # Overwrite father class send method
    def sendMessage(self, serverName, serverPort, message):
        # We need to send the message
        print("Holy shit, Python!")
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.sendto(message.encode('utf-8'), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        print ("From Server: " + modifiedMessage.decode('utf-8'))
        clientSocket.close()

class ClientNodeTCP(ClientNode):

    #Constructor
    def __init__(self):
        ClientNode.__init__(self)
        print("ClientNodeTCP : Constructor :)")

    # Overwrite father class send method
    def sendMessage(self, serverName, serverPort, message):
        # We need to send the message
        print("Holy shit, Python!")
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        clientSocket.send(message.encode('utf-8'))
        modifiedSentence = clientSocket.recv(1024)
        print ("From Server: " + modifiedSentence.decode('utf-8'))
        clientSocket.close()

############################################# Servers #############################################
class ServerNode(Thread):

    # Constructor
    def __init__(self, port, table):
        Thread.__init__(self)
        self.port = port
        self.alcanzabilityTable = table
        print("ServerNode : Constructor :(")
    
    def run(self):
        print("ServerNode : Receiving shit and stuff!")
        print("ServerNode : I'm dying!")

    def unpackMessage(self, packedMessage):
        print("ServerNode : Unpacking the message ...")
        return packedMessage

    # Update the alcanzavility table structure with the data of the recieved message
    # This method should be another thread by it self, one thread for conection    
    def proccessMessage(self, clientAddr, msj):
        self.lock.acquire()
        print("ServerNode : this thread is proccesing the message!")
        if(int(msg[0]) == 0):
            ## Borrar ipEmisor de la lista de conexiones
            print("No me quiero ir Señor Nodo")
        else:
            msg = msj.split('/')
            maximo = int(msg[0]) * 3
            i = 1
            while(i < maximo):
                tupla = []
                tupla.append(clientAddr)
                tupla.append(str(msg[i]))
                tupla.append(str(msg[i+1]))
                tupla.append(str(msg[i+2]))
                if(len(self.alcanzabilityTable) == 0):
                    self.alcanzabilityTable.append(tupla)
                else:
                    found = False
                    for it in self.alcanzabilityTable:
                        if(it[1] == tupla[1] and it[2] == tupla[2]):
                            if(int(it[3]) > int(tupla[3])):
                                it[3] = tupla[3]
                            found = True
                            break
                    if(not found):
                        self.alcanzabilityTable.append(tupla)
                i += 3
            self.lock.release()

class ServerNodeUDP(ServerNode):
    
    # Constructor
    def __init__(self, port, table):
        ServerNode.__init__(self, port, table)
        # Missing alcanzability table field
        print("ServerNodeUDP : Constructor :(")

    # Overwite the father class relevant methods!
    def run(self):
        print("ServerNode : Receiving shit and stuff!")
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(("", self.port))
        print ("The server is ready to receive")
        while (1):
            # We need to recieve the packed message from the client
            packedMessage, clientAddress = serverSocket.recvfrom(2048)
            # We need to unpack the recieved message
            message = self.unpackMessage(packedMessage)
            print("Client ip: " + clientAddress + "\nClient message: " + message)
            # We need to create a thread to proccess the recived message
            conectionThread = Thread(target=self.proccessMessage, args=(clientAddress, message))
            conectionThread.start()
            serverSocket.sendto("✓✓", clientAddress)
        print("ServerNode : I'm dying!")

class ServerNodeTCP(ServerNode):

    #Constructor
    def __init__(self, port, table):
        ServerNode.__init__(self, port, table)
        # Missing alcanzability table field
        print("ServerNodeTCP : Constructor :(")
    
    # Overwite the father class relevant methods!
    def run(self):
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind(("", self.port))
        serverSocket.listen(1)
        print("ServerNode : Receiving shit and stuff!")
        while (1):
	        connectionSocket, addr = serverSocket.accept()
	        message = connectionSocket.recv(1024)
	        print (str(addr))
	        print (str(message))
	        capitalizedSentence = message.upper()
	        connectionSocket.send(capitalizedSentence)
	        connectionSocket.close()
        print("ServerNode : I'm dying!")

############################################# General #############################################
class Node():
    
    # Constructor
    def __init__(self, isPseudoBGP, ip, mask, port):
        self.isPseudoBGP = isPseudoBGP
        self.ip = ip
        self.mask = mask
        self.port = port
        self.lock = threading.Lock()
        self.alcanzabilityTable = []
        #self.printAlcanzabilityTable()
        print("Node (The real mvp!) : Constructor ")
    
    def printAlcanzabilityTable(self):
        self.lock.acquire()
        print ("Alcanzability Table: ")
        print (["Network Address","Mask","Cost", "Origin"])
        for index in range(len(self.alcanzabilityTable)):
            print(self.alcanzabilityTable[index])    
        self.lock.release()

    # This is the method that execute everything the program need to work
    def run(self):
        #print("Node : I basically do everything")
        # We need to create the corresponding client node and server node
        if(self.isPseudoBGP):
            self.serverNode = ServerNodeTCP(self.port, self.alcanzabilityTable)
            self.clientNode = ClientNodeTCP()
        else:
            self.serverNode = ServerNodeUDP(self.port, self.alcanzabilityTable)
            self.clientNode = ClientNodeUDP()
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
                beingDeleted = True
            elif(option == 1):
                self.clientNode.run()
            elif(option == 2):
                self.printAlcanzabilityTable()
            else:
                print_error_option()


############################################# Main #############################################
# Program main funtion
if __name__ == '__main__':
    # We need to parse the arguments pass by the user
    parser = argparse.ArgumentParser(description='choose the type of node you want to use')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-tcp", "--pseudoBGP", action="store_true")
    group.add_argument("-udp", "--intAS", action="store_true")
    parser.add_argument("ip", help="recive the node ip address")
    parser.add_argument("mask", help="recive the subnet mask, it must be a integer between 8 and 30", type=int)
    parser.add_argument("port", help="recive the server port number", type=int)
    args = parser.parse_args()
    print ("ip address: " + args.ip + "\nsubnet mask: " + str(args.mask) + "\nport number: " + str(args.port))

    # We need to make sure the arg pass by the user are valid

    # We need to check if the user select a node type
    if(not args.pseudoBGP and not args.intAS):
        # If the user did not select a node type, the node type will be pseudoBGP by default
        args.pseudoBGP = True

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

    # We need to check if the ip address pass by the user is a valid ip address
    if(not validate_ip_address(args.ip)):
        print_error_invalid_ip()
        sys.exit(-1)
    print ("The provided ip address is valid! Hooray!")

    # If all the arguments pass by the user are valid, we continue creating the node and executing it
    node = Node(args.pseudoBGP, args.ip, args.mask, args.port)
    node.run()

    print('Main Terminating...')
