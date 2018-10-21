from utilities import *

class ClientNode():

    # Constructor
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
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
            messageRow = input("l: ")
            if(not validateRow(messageRow)):
                return -1
            clientMessage += messageRow + "/"
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
                if(is_valid_ipv4_address(messageTokens[i])):
                    # I need to pack the ip address
                    ipTokens = messageTokens[i].split('.')
                    #print(ipTokens)
                    for indIp in range(0,4):
                        #print(ipTokens[indIp])
                        packedMessage += int(ipTokens[indIp]).to_bytes(1, byteorder='little')
                else:
                    print_error_invalid_ip()
                    return -1
                #'''
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
        # First we need to ask the user who do he/she wants to send the message
        serverName = input(askIPAddressMessage)
        if(not is_valid_ipv4_address(serverName)):
            print_error_invalid_ip()
            return
        try:
            serverPort = int(input(askPortMessage))
        except ValueError:
            print_error_invalid_port()
            return
        if(serverPort < 0 or serverPort > 65535):
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

    def stop(self):
        print("ClientNode: Stoping!")
