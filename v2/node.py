import sys
import argparse
from threading import Thread
from socket import *
from utilities import *

# Clases
############################################# Clients #############################################
class ClientNode():

    # Constructor
    def __init__(self):
        print("ClientNode : Constructor :)")
        pass

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
            return -1
        if(n <= 0):
            print_error_invalid_n()
            return -1
        clientMessage = ""
        clientMessage += str(n) + "/"
        for i in range (n):
            clientMessage += input("l: ") + "/"
        return clientMessage
    
    # Pack the message given by the user in the requested format: n (2 bytes), ip (4 bytes), mask(1 byte), cost (3 bytes)
    # Returns the packed message
    def packMessage(self, message):
        #print(message)
        print("ClientNode : Packing the message ...")
        # If the message is a deleting node message
        if(message == "0"):
            packedMessage = (0).to_bytes(1, byteorder='little')
            return packedMessage
        else:
            messageTokens = message.split('/')
            #print(messageTokens)
            try:
                n = int(messageTokens[0])
            except ValueError:
                    print_error_invalid_n()
                    return -1
            packedMessage = n.to_bytes(2, byteorder='little')
            endOfMessage = n * 3
            i = 1
            while(i < endOfMessage):
                # We need to check the ip pass by the user is valid
                if(validate_ip_address(messageTokens[i])):
                    # I need to pack the ip address
                    ipTokens = messageTokens[i].split('.')
                    #print(ipTokens)
                    for indIp in range(0,4):
                        #print(ipTokens[indIp])
                        packedMessage += int(ipTokens[indIp]).to_bytes(1, byteorder='little')
                else:
                    print_error_invalid_ip()
                    return -1
                try:
                    mask = int(messageTokens[i+1])
                except ValueError:
                    #print (messageTokens[i+1])
                    print_error_invalid_mask()
                    return -1
                if(mask < 8 or mask > 30):
                    print_error_invalid_mask()
                    return -1
                else:
                    #print(mask)
                    packedMessage += mask.to_bytes(1, byteorder='little')
                try:
                    cost = int(messageTokens[i+2])
                except ValueError:
                    print_error_invalid_cost()
                    return -1
                if(cost < 0):
                    print_error_invalid_cost()
                    return -1
                else:
                    #print(cost)
                    packedMessage += cost.to_bytes(3, byteorder='little')
                i += 3
            return packedMessage

    # Send the packed message past by the user and send it to the destination also past by the user.	
    def sendMessage(self, serverName, serverPort, message):
        print("ClientNode : Sending message")

    def run(self):
        print("ClientNode : Running!")
        print("ClientNodeUDP : Sending message")
        # First we need to ask the user who do he/she wants to send the message
        serverName = input(askIPAddressMessage)
        try:
            serverPort = int(input(askPortMessage))
        except ValueError:
            print_error_invalid_port()
            return
        # We need to verify the ip address and port number past by the user?

        # We need to ask the user for the message he/she wants to send
        userMessage = self.askUserMessage()
        if(userMessage == -1):
            print_error_invalid_message()
            return
        #print(userMessage)
        
        # We need to pack the message in order to send it
        packedMessage = self.packMessage(userMessage)
        if(packedMessage == -1):
            print_error_invalid_message()
            return
        #print(packedMessage)

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
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        #clientSocket.sendto(message.encode('utf-8'), (serverName, serverPort))
        clientSocket.sendto(message, (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        print ("From Server: " + modifiedMessage.decode('utf-8'))
        clientSocket.close()

class ClientNodeTCP(ClientNode):

    #Constructor
    def __init__(self):
        ClientNode.__init__(self)
        #We need to keep a list of conections
        self.conections = {}
        print("ClientNodeTCP : Constructor :)")

    # Overwrite father class send method
    def sendMessage(self, serverName, serverPort, message):
       # We need to send the message
        print("Holy shit, Python!")
        idConection = str(serverName) + "-" + str(serverPort)
        if(idConection in self.conections):
            print("Existing connection")
            try:
                self.conections[idConection].send(message)
                modifiedSentence = self.conections[idConection].recv(1024)
                print ("From Server: " + modifiedSentence.decode('utf-8'))
                if message[0] == 0:
                    self.conections[idConection].close()
                    del self.conections[idConection]
            except:
                print("The conection with",idConection,"has expired, try again")
                del self.conections[idConection]                
        else:
            print("New connection")
            clientSocket = socket(AF_INET, SOCK_STREAM)
            self.conections[idConection] = clientSocket
            try:
                clientSocket.connect((serverName, serverPort))
                clientSocket.send(message)
                modifiedSentence = clientSocket.recv(1024)
                print ("From Server: " + modifiedSentence.decode('utf-8'))
                if message == "0":
                    clientSocket.close()
            except Exception as e:
                print("No connection can be established: ",e)

############################################# Servers #############################################
class ServerNode(Thread):

    # Constructor
    def __init__(self, port, table):
        Thread.__init__(self)
        self.port = port
        self.alcanzabilityTable = table
        print("ServerNode : Constructor :)")
    
    def run(self):
        print("ServerNode : Receiving messages and stuff!")
        print("ServerNode : I'm dying!")

    def unpackMessage(self, packedMessage):
        print("ServerNode : Unpacking the message ...")
        #print(packedMessage)
        n = int.from_bytes(packedMessage[0:2], byteorder='little')
        message = ""
        message = str(n) + "/"
        #print(n)
        endOfPackedMessage = n*8+2
        ind = 2
        while(ind < endOfPackedMessage):
            ipAddress = ""
            i = 0
            for i in range(4):
                ipPart = packedMessage[ind+i]
                ipAddress += str(ipPart)
                if(i < 3):
                    ipAddress += "."
            #print(ipAddress)
            message += ipAddress + "/"
            ind += 4
            mask = packedMessage[ind]
            message += str(mask) + "/"
            #print(mask)
            cost = int.from_bytes(packedMessage[ind+1:ind+3], byteorder='little')
            message += str(cost) + "/"
            #print(cost)
            ind += 4
        return(message)

    # Update the alcanzavility table structure with the data of the recieved message
    # This method should be another thread by it self, one thread for conection    
    def proccessMessage(self, clientAddr, msj):
        aTLock.acquire()
        print("ServerNode : this thread is proccesing the message!")
        if(msj == "0"):
            # Delete clientAddr to the alcanzabilityTable
            for itr in self.alcanzabilityTable:
                if(itr[0] == clientAddr):
                    del itr
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
        aTLock.release()

class ServerNodeUDP(ServerNode):
    
    # Constructor
    def __init__(self, port, table):
        ServerNode.__init__(self, port, table)
        # Missing alcanzability table field
        print("ServerNodeUDP : Constructor :)")

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
            #message = self.unpackMessage(packedMessage.decode('utf-8'))
            message = self.unpackMessage(packedMessage)
            #print("Client ip: " + str(clientAddress) + "\nClient message: " + message)
            # We need to create a thread to proccess the recived message
            conectionThread = Thread(target=self.proccessMessage, args=(clientAddress, message))
            conectionThread.start()
            serverSocket.sendto("✓✓".encode('utf-8'), clientAddress)
        print("ServerNode : I'm dying!")

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
                clientSocket.sendto("✓✓".encode('utf-8'), addrs)
                if message == 0:
                  break
            except Exception as e:
                print("The conection with",addrs,"has expired") 
                break

############################################# General #############################################
class Node():
    
    # Constructor
    def __init__(self, isPseudoBGP, ip, mask, port):
        self.isPseudoBGP = isPseudoBGP
        self.ip = ip
        self.mask = mask
        self.port = port
        self.alcanzabilityTable = []
        #self.printAlcanzabilityTable()
        print("Node (The real mvp!) : Constructor ")
    
    def printAlcanzabilityTable(self):
        aTLock.acquire()
        print ("Alcanzability Table: ")
        print (["Network Address","Mask","Cost", "Origin"])
        for index in range(len(self.alcanzabilityTable)):
            print(self.alcanzabilityTable[index])    
        aTLock.release()

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
