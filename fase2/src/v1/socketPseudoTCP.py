from queue import *
from socket import *
from random import randint
from threading import Thread
from collections import namedtuple

# Constants
SYNACK = 6
SYN = 4
ACK = 2
FIN = 1

Message = namedtuple("Message", ["originPort", "destinyPort", "SN", "RN", "headerSize", "SYN", "ACK", "FIN", "data"])

class SocketPseudoTCP:

    # Constructor
    def __init__(self):
        # Fields
        # SN, current message sequence number
        self.SN = 0
        # RN, current message responce number
        self.RN = 0
        # selfAddr, self ip addr and port
        self.selfAddr = ("", -1)
        # connectionAddr, connection ip addr and port
        self.connectionAddr = ("", -1)
        # messageQueue, Queue to store the recived message and sender IP addr to this sockect
        self.messageQueue = Queue()
        # connectionSockets, dictionary with key: a connectionAddr, and with value: instance of this class
        self.connectionSockets = {}
        # socketUDP, UDP socket use to actually send and recv messages
        self.socketUDP = socket(AF_INET, SOCK_DGRAM)
        print("SocketPseudoTCP : Constructor :)")

    # Methods

    # "Client" side
    # connect, starts and finnishes the 3-way handshake with the server socket
    def connect(self, serverAddr):
        print("SocketPseudoTCP : Connecting!")
        # I need to assign my connectionAddr
        self.connectionAddr = serverAddr
        # I need to create a new random port number (it is also a socket id) and make bind on it
        successfulBind = False
        while( not successfulBind ):
            self.selfAddr = ("", randint(1024, 65535))
            #self.selfAddr = ("", 80)
            print("Connecting! : this is my selfAddr " + str(self.selfAddr))
            try:
                self.bind(self.selfAddr)
            except Exception as e:
                print("Connecting Error! : Unsuccessful bind: " + str(e))
                continue
            successfulBind = True
        self.SN = self.selfAddr[1]%2
        # I need to send the SYN message to start the handshake process with the wanted serverSocket
        SYNMessage = Message._make([self.selfAddr[1], self.connectionAddr[1], self.SN, self.RN, 8, True, False, False, "".encode('utf-8')])
        print(str(SYNMessage))
        encodedSYNMessage = self.encodeMessage(SYNMessage)
        print(str(encodedSYNMessage))
        self.socketUDP.sendto(encodedSYNMessage, self.connectionAddr)
        # I need to wait for the SYNACK message from the server
        while True:
            try:
                queueMessage = self.messageQueue.get(True, 5)
            except Empty:
                print("Connecting timeout! : Well the server left me hanging ...")
                self.socketUDP.sendto(encodedSYNMessage, self.connectionAddr)
                continue
            # If I recived something, I need to check it is a SYNACK message
            SYNACKMessage = queueMessage[0]
            if((SYNACKMessage.SYN and SYNACKMessage.ACK) and (SYNACKMessage.RN != self.SN)):
                # If the message is what I was waiting for
                print("Connecting! : A valid SYNACK message just what I wanted, thanks Satan!")
                # I need to update the S&W data
                self.SN = SYNACKMessage.RN
                self.RN = (SYNACKMessage.SN + 1)%2
                self.printQueue(self.messageQueue)
                break
            else:
                print("Connecting! : Not a SYNACK message or invalid SYNACK message!")
                self.messageQueue.put(queueMessage)
                self.printQueue(self.messageQueue)
                continue
        # Finally I need to sent an ACK message to close the handshake
        specialACKMessage = Message._make([self.selfAddr[1], self.connectionAddr[1], self.SN, self.RN, 8, False, True, False, "".encode('utf-8')])
        print(str(specialACKMessage))
        encodedSpecialACKMessage = self.encodeMessage(specialACKMessage)
        print(str(encodedSpecialACKMessage))
        self.socketUDP.sendto(encodedSpecialACKMessage, self.connectionAddr)
        # I need to wait for the ACK message from the server
        while True:
            try:
                queueMessage = self.messageQueue.get(True, 5)
            except Empty:
                print("Connecting timeout! : Well the server left me hanging ...")
                self.socketUDP.sendto(encodedSpecialACKMessage, self.connectionAddr)
                continue
            # If I recived something, I need to check it is a SYNACK message
            ACKMessage = queueMessage[0]
            if((ACKMessage.ACK and not ACKMessage.SYN) and (ACKMessage.RN != self.SN)):
                # If the message is what I was waiting for
                print("Connecting! : A valid ACK message just what I wanted, thanks Satan!")
                # I need to update the S&W data
                self.SN = ACKMessage.RN
                self.RN = (ACKMessage.SN + 1)%2
                self.printQueue(self.messageQueue)
                break
            else:
                print("Connecting! : Not a ACK message or invalid ACK message!")
                self.messageQueue.put(queueMessage)
                self.printQueue(self.messageQueue)
                continue


    # send, sends a byte array or encoded message.
    def send(self, message):
        print("SocketPseudoTCP : Sending!")
        while True:
            continue

    # recv, recive the number of bytes passed as arg. Returns a the received message as encoded message o a byte array
    def recv(self, numberOfBytes):
        print("SocketPseudoTCP : Receiving!")
        while True:
            continue

    # close, closes the connection, ie delete the connection sockect from the connectionSockets dictionary.
    def close(self):
        print("SocketPseudoTCP : Closing!")

    # "Server" side
    # bind, calls the bind method of the UDP port and starts the despacher. It also initialize the self.messageQueue with the maximun size pass as arg.
    def bind(self, selfAddr):
        print("SocketPseudoTCP : Binding!")
        # I need to bind my socketUDP to the given selfAddr
        self.selfAddr = selfAddr
        self.socketUDP.bind(self.selfAddr)
        # If everything was just fine
        # I need to start the despacher thread
        despacherThread = Thread(target=self.despatch)
        despacherThread.daemon = True
        despacherThread.start()


    # listen, thread!, search the server socket messageQueue for a SYN message and proccess it.
    def listen(self, serverQueueSize):
        print("SocketPseudoTCP : Listening!")
        # I only start the listen thread
        listenerThread = Thread(target=self.listenThread)
        listenerThread.daemon = True
        listenerThread.start()

    def listenThread(self):
        print("SocketPseudoTCP : Listening Thread!")
        while True:
            # I need to check if there is a SYN message on my messageQueue and answer it with a SYNACK message
            queueMessage = self.messageQueue.get()
            SYNMessage = queueMessage[0]
            if(SYNMessage.SYN and (not SYNMessage.ACK)):
                # I need to check if I alrrady have a connection with the sender
                if(not (queueMessage[1], SYNMessage.originPort) in self.connectionSockets):
                    # If the SYN message is valid
                    print("Listening Thread! : Valid SYN message!")
                    # I need to store the new posible conection data
                    connectionSocket = SocketPseudoTCP()
                    connectionSocket.SN = randint(0, 1)
                    connectionSocket.RN = (SYNMessage.SN + 1) % 2
                    connectionSocket.selfAddr = self.selfAddr
                    self.connectionSockets[(queueMessage[1], SYNMessage.originPort)] = connectionSocket
                    # I need to send a SYNACK message in respond
                    SYNACKMessage = Message._make([connectionSocket.selfAddr[1],  SYNMessage.originPort, connectionSocket.SN, connectionSocket.RN, 8, True, True, False, "".encode('utf-8')])
                    print(str(SYNACKMessage))
                    encodedSYNACKMessage = self.encodeMessage(SYNACKMessage)
                    print(str(encodedSYNACKMessage))
                    self.socketUDP.sendto(encodedSYNACKMessage, (queueMessage[1], SYNMessage.originPort))
                    self.messageQueue.task_done()
                    self.printQueue(self.messageQueue)
                else:
                    # If the conection already existed, I need to drop the invalid SYN message
                    print("Listening Thread Error! : The connection already existed!")
                    self.messageQueue.task_done()
                    self.printQueue(self.messageQueue)
                    continue
            else:
                # If it is not a SYN message, I need to put the message again on my messageQueue and try again
                print("Listening Thread Error! : Not a SYN message!")
                self.messageQueue.put_nowait(queueMessage)
                self.messageQueue.task_done()
                self.printQueue(self.messageQueue)

    # accept, returns a instance of this class as the connection with the client socket that initiated the communication. Add the new connectionSocket (instance) to the connectionSockets dictionary
    def accept(self):
        print("SocketPseudoTCP : Accepting!")
        while True:
            # I need to check if there is a specal ACK message on my messageQueue and answer it with a regular ACK message
            queueMessage = self.messageQueue.get()
            specialACKMessage = queueMessage[0]
            if(specialACKMessage.ACK and not specialACKMessage.SYN):
                # If it is a special ACK message, I need to check if it is a valid one
                connectionSocket = self.connectionSockets.get((queueMessage[1], specialACKMessage.originPort))
                if(connectionSocket.SN != specialACKMessage.RN):
                    # It is a valid one, now I need to update the connectionSocket data
                    print("Connecting Error! : valid special ACK message!")
                    connectionSocket.SN = specialACKMessage.RN
                    connectionSocket.RN = (specialACKMessage.SN + 1)%2
                    connectionSocket.connectionAddr = (queueMessage[1], specialACKMessage.originPort)
                    # I need to sent a regular ACK messages
                    ACKMessage = Message._make([connectionSocket.selfAddr[1],  connectionSocket.connectionAddr[1], connectionSocket.SN, connectionSocket.RN, 8, False, True, False, "".encode('utf-8')])
                    print(str(ACKMessage))
                    encodedACKMessage = self.encodeMessage(ACKMessage)
                    print(str(encodedACKMessage))
                    self.socketUDP.sendto(encodedACKMessage, connectionSocket.connectionAddr)
                    self.messageQueue.task_done()
                    self.printQueue(self.messageQueue)
                    return(connectionSocket, connectionSocket.selfAddr)
                else:
                    # It is a invalid one, I need to drop this message and try again
                    print("Connecting Error! : Invalid special ACK message!")
                    self.messageQueue.task_done()
                    self.printQueue(self.messageQueue)
                    continue
            else:
                #If it is not a special ACK message, I need to put the message again on my messageQueue and try again
                print("Connecting Error! : Not a special ACK message!")
                self.messageQueue.put_nowait(queueMessage)
                self.messageQueue.task_done()
                self.printQueue(self.messageQueue)

    # Private methods
    # despatch, thread!, demultiplex all the messages send to the serverPort.
    def despatch(self):
        print("SocketPseudoTCP : Despatching!")
        while True:
            try:
                encodedMessage, senderAddr = self.socketUDP.recvfrom(2048)
            except Exception as e:
                print("Despatching Error! : " + str(e))
                continue
            # If everything was just fine
            # I need to demultiplex the recieved message
            print("Despatching! : " + str(encodedMessage))
            message = self.decodeMessage(encodedMessage)
            print("Despatching! : " + str(message))
            # First I need to check if the message if actually for me
            if(message.destinyPort == self.selfAddr[1]):
                print("Despatching! : The mesage is for me!")
                # Now I need to demultiplex the message
                # If the recieved message is a SYN or FIN it is for my messageQueue
                if(message.SYN or message.FIN):
                    self.messageQueue.put((message, senderAddr[0]))
                    self.printQueue(self.messageQueue);
                else:
                    print("Despatching! : Fisrt you get the data, then you get the power, then you get the women")
                    # I need to check if the sender is a known connection
                    if((senderAddr[0], message.originPort) in self.connectionSockets):
                        # If it is I need to check if the connection was already stablish
                        connectionSocket = self.connectionSockets.get((senderAddr[0], message.originPort));
                        if(connectionSocket.connectionAddr == ("", -1)):
                            self.messageQueue.put((message, senderAddr[0]))
                            self.printQueue(self.messageQueue);
                        else:
                            connectionSocket.messageQueue.put((message, senderAddr[0]))
                            self.printQueue(connectionSocket.messageQueue);
                    else:
                        # If it is no I need to check if the sender is my connectionAddr
                        if(self.connectionAddr[1] == message.originPort):
                            self.messageQueue.put((message, senderAddr[0]))
                            self.printQueue(self.messageQueue);
                        else:
                            print(":(")

    # encodeMessage
    def encodeMessage(self, message):
        print("Encoder : Encoding message!")
        # I need to encode the message parameter into a bytearray
        encodedMessage = ( message.originPort.to_bytes(2, byteorder='big') + message.destinyPort.to_bytes(2, byteorder='big')
        + message.SN.to_bytes(1, byteorder='big') + message.RN.to_bytes(1, byteorder='big') + message.headerSize.to_bytes(1, byteorder='big'))
        # If message is a SYNACK message
        if(message.SYN and message.ACK and not message.FIN):
            encodedMessage += SYNACK.to_bytes(1, byteorder='big')
        # If message is a SYN message
        elif(message.SYN):
            encodedMessage += SYN.to_bytes(1, byteorder='big')
        # If message is a ACK message
        elif(message.ACK):
            encodedMessage += ACK.to_bytes(1, byteorder='big')
        # If message is a FIN message
        elif(message.FIN):
            encodedMessage += FIN.to_bytes(1, byteorder='big')
        encodedMessage += message.data
        return encodedMessage

    # decodeMessage
    def decodeMessage(self, message):
        print("Decoder : Decoding message!")
        decodedMessageSYN = decodedMessageACK = decodedMessageFIN = False
        if(int(message[7]) == SYNACK):
            decodedMessageSYN = decodedMessageACK = True
        elif(int(message[7]) == SYN):
            decodedMessageSYN = True
        elif(int(message[7]) == ACK):
            decodedMessageACK = True
        elif(int(message[7]) == FIN):
            decodedMessageFIN = True
        decodedMessage = Message._make([ int.from_bytes(message[0:2], byteorder='big'), int.from_bytes(message[2:4], byteorder='big'),
        int(message[4]), int(message[5]), int(message[6]), decodedMessageSYN, decodedMessageACK, decodedMessageFIN, message[8:] ])
        return decodedMessage

    #printQueue
    def printQueue(self, queue):
        print(list(queue.queue))