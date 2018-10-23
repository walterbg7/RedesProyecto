from queue import *
from socket import *
from utilities import *
from random import randint
from threading import Thread
from collections import namedtuple
import math

# Constants
SYNACK = 6
SYN = 4
ACK = 2
ACKSTART = 18
ACKEND = 11
FIN = 1
START =16
END = 8

Message = namedtuple("Message", ["originPort", "destinyPort", "SN", "RN", "headerSize", "SYN", "ACK", "FIN", "START", "END", "data"])

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


        writeOnLog("Log", "", "", "", "SocketPseudoTCP : Constructor :)", 0)

    # Methods

    # "Client" side
    # connect, starts and finnishes the 3-way handshake with the server socket
    def connect(self, serverAddr):
        writeOnLog("Log", "", "", "","SocketPseudoTCP : Connecting!",0)
        # I need to assign my connectionAddr
        self.connectionAddr = serverAddr
        # I need to create a new random port number (it is also a socket id) and make bind on it
        successfulBind = False
        while( not successfulBind ):
            self.selfAddr = ("", randint(1024, 65535))
            #self.selfAddr = ("", 80)
            writeOnLog("Log", "", "", "","Connecting! : this is my selfAddr " + str(self.selfAddr), 0)
            try:
                self.bind(self.selfAddr)
            except Exception as e:
                writeOnLog("Log", "", "", "", "Connecting Error! : Unsuccessful bind: " + str(e), 0)
                continue
            successfulBind = True
        self.SN = self.selfAddr[1]%2
        # I need to send the SYN message to start the handshake process with the wanted serverSocket
        SYNMessage = Message._make([self.selfAddr[1], self.connectionAddr[1], self.SN, self.RN, 8, True, False, False, False, False, "".encode('utf-8')])
        encodedSYNMessage = self.encodeMessage(SYNMessage)
        writeOnLog("Log", self.selfAddr, self.connectionAddr, "Connect: SYN message", SYNMessage)
        self.socketUDP.sendto(encodedSYNMessage, self.connectionAddr)
        # I need to wait for the SYNACK message from the server
        while True:
            try:
                queueMessage = self.messageQueue.get(True, 5)
            except Empty:
                writeOnLog("Log", "", "", "", "Connecting timeout! : Well the server left me hanging ...",0)
                self.socketUDP.sendto(encodedSYNMessage, self.connectionAddr)
                continue
            # If I recived something, I need to check it is a SYNACK message
            SYNACKMessage = queueMessage[0]
            if((SYNACKMessage.SYN and SYNACKMessage.ACK) and (SYNACKMessage.RN != self.SN)):
                # If the message is what I was waiting for
                writeOnLog("Log", "", "", "","Connecting! : A valid SYNACK message just what I wanted, thanks Satan!",0)
                # I need to update the S&W data
                writeOnLog("Log", self.connectionAddr, self.selfAddr, "Connect: response of SYN message, valid SYNACK message", queueMessage)
                self.SN = SYNACKMessage.RN
                self.RN = (SYNACKMessage.SN + 1)%2
                self.printQueue(self.messageQueue)
                break
            else:
                writeOnLog("Log", "", "", "","Connecting! : Not a SYNACK message or invalid SYNACK message!",0)
                writeOnLog("Log", self.connectionAddr, self.selfAddr, "Connect: response of SYN message, Not a SYNACK message or invalid SYNACK message", queueMessage)
                self.messageQueue.put(queueMessage)
                self.printQueue(self.messageQueue)
                continue
        # Finally I need to sent an ACK message to close the handshake
        specialACKMessage = Message._make([self.selfAddr[1], self.connectionAddr[1], self.SN, self.RN, 8, False, True, False, False, False, "".encode('utf-8')])
        encodedSpecialACKMessage = self.encodeMessage(specialACKMessage)
        writeOnLog("Log", self.selfAddr, self.connectionAddr, "Connect: response of SYNACK message", specialACKMessage)
        self.socketUDP.sendto(encodedSpecialACKMessage, self.connectionAddr)
        # I need to wait for the ACK message from the server
        while True:
            try:
                queueMessage = self.messageQueue.get(True, 5)
            except Empty:
                writeOnLog("Log", "", "", "","Connecting timeout! : Well the server left me hanging ...", 0)
                writeOnLog("Log", self.selfAddr, self.connectionAddr, "Connect: response of SYNACK message, forwarded", specialACKMessage)
                self.socketUDP.sendto(encodedSpecialACKMessage, self.connectionAddr)
                continue
            # If I recived something, I need to check it is a SYNACK message
            ACKMessage = queueMessage[0]
            if(ACKMessage.ACK and not ACKMessage.SYN):
                if(ACKMessage.RN != self.SN):
                    # If the message is what I was waiting for
                    writeOnLog("Log", "", "", "", "Connecting! : A valid ACK message just what I wanted, thanks Satan!", 0)
                    # I need to update the S&W data
                    writeOnLog("Log", self.connectionAddr, self.selfAddr,"Connect: ACK of response of SYNACK message, connection stablieshed", specialACKMessage)
                    self.SN = ACKMessage.RN
                    self.RN = (ACKMessage.SN + 1)%2
                    break
                else:
                    writeOnLog("Log", self.connectionAddr, self.selfAddr,"Connect: ACK of response of SYNACK message, invalid ACK message", specialACKMessage)
                    writeOnLog("Log", "", "", "","Connecting! : Invalid ACK message!", 0)
                    continue
            else:
                writeOnLog("Log", "", "", "","Connecting! : Not a ACK message!", 0)
                writeOnLog("Log", self.connectionAddr, self.selfAddr,"Connect: ACK of response of SYNACK message, is not a ACK message", specialACKMessage)
                self.messageQueue.put(queueMessage)
                self.printQueue(self.messageQueue)
                continue
        writeOnLog("Log", "", "", "", "Connecting! : CLIENT SN: " + str(self.SN) + " CLIENT RN:" +  str(self.RN), 0)


    # send, sends a byte array or encoded message.
    def send(self, message):
        writeOnLog("Log", "", "", "", "SocketPseudoTCP : Sending!", 0)
        lenMessage = len(message)
        numPackages = math.ceil(lenMessage / 8)
        lastPackages = numPackages -1
        currentPart = 0 #We need to know the current part of the message
        partOfMessage = bytearray()
        firstMessage = True
        for number in range(0, lastPackages):
            #We are going to send data of 8 bytes
            partOfMessage = message[currentPart:(currentPart + 8)]
            currentPart += 8
            finalMessage = Message._make([self.selfAddr[1], self.connectionAddr[1], self.SN, self.RN, 8, False, False, False, firstMessage, False, partOfMessage])
            firstMessage = False
            packedMessage = self.encodeMessage(finalMessage)
            writeOnLog("Log", self.selfAddr, self.connectionAddr, "Send: send a package of message", finalMessage)
            self.sendMessage(packedMessage)
            partOfMessage = bytearray()

        partOfMessage = message[currentPart:]
        finalMessage = Message._make([self.selfAddr[1], self.connectionAddr[1], self.SN, self.RN, 8, False, False, False, firstMessage, True, partOfMessage])
        packedMessage = self.encodeMessage(finalMessage)
        writeOnLog("Log", self.selfAddr, self.connectionAddr, "Send: send a package of message", finalMessage)
        self.sendMessage(packedMessage)

    def sendMessage(self, packedMessage):
        writeOnLog("Log", "", "", "", "Sending Message! : My SN " + str(self.SN) + "  My RN "+ str(self.RN), 0)
        trySend = 1
        self.socketUDP.sendto(packedMessage, self.connectionAddr)
        while True:
            try:
                queueMessage = self.messageQueue.get(True, 2)
            except Empty:
                if trySend == 5:
                    break
                writeOnLog("Log", "", "", "", "Sending Message timeout! : Well the server left me hanging ...", 0)
                writeOnLog("Log", self.selfAddr, self.connectionAddr, "Send: send a package of message, forwarded", packedMessage)
                self.socketUDP.sendto(packedMessage, self.connectionAddr)
                continue
            # If I recived something, I need to check it is a ACK message
            ACKMessage = queueMessage[0]
            if((ACKMessage.ACK) and (ACKMessage.RN != self.SN)):
                # If the message is what I was waiting for
                writeOnLog("Log", self.connectionAddr, self.selfAddr, "Send: ACK of package sended", ACKMessage)
                writeOnLog("Log", "", "", "", "Sending Message Full delivery! : A valid ACK message just what I wanted, thanks Satan!", 0)
                # I need to update the S&W data
                self.SN = ACKMessage.RN
                #self.RN = (self.RN + 1)%2
                self.printQueue(self.messageQueue)
                break
            else:
                writeOnLog("Log", self.connectionAddr, self.selfAddr, "Send: Invalid ACK of package sended", ACKMessage)
                writeOnLog("Log", "", "", "", "Sending Message Fail delivery!! : Not a ACK message or invalid ACK message!", 0)
                #self.messageQueue.put(queueMessage)
                self.printQueue(self.messageQueue)
                continue

    # recv, recive the number of bytes passed as arg. Returns a the received message as encoded message o a byte array
    def recv(self, numberOfBytes):
        writeOnLog("Log", "", "", "", "SocketPseudoTCP : Receiving!", 0)
        numTimeOuts = 0
        messageRecived = bytearray()
        firstPacket = True
        writeOnLog("Log", "", "", "", "Receiving! : My SN " + str(self.SN) + "  My RN " + str(self.RN) , 0)
        while True:
            try:
                queueMessage = self.messageQueue.get(True, 2)
            except Empty:
                if(not firstPacket):
                    writeOnLog("Log", "", "", "", "Receiving! : Time Out", 0)
                    ACKMessage = Message._make([self.selfAddr[1], self.connectionAddr[1], self.SN, self.RN, 8, False, True, False, False, False, "".encode('utf-8')])
                    encodedACKMessage = self.encodeMessage(ACKMessage)
                    writeOnLog("Log", self.selfAddr, self.connectionAddr, "RECV: ACK of a recived message ", ACKMessage)
                    self.socketUDP.sendto(encodedACKMessage, self.connectionAddr)
                    if(numTimeOuts == 5):
                        break
                    else:
                        numTimeOuts += 1
                        continue
                else:
                    continue
            # If I recived something, I need to check it is a data message
            dataMessage = queueMessage[0]
            if(not dataMessage.SYN and not dataMessage.ACK and not dataMessage.FIN):
                lossProb = randint(1,10)
                # I need to check if the package was "lost"
                if(lossProb == 1):
                    writeOnLog("Log", "", "", "", "Receiving! : Package lost", 0)
                    writeOnLog("Log", self.selfAddr, self.connectionAddr, "RECV: Package lost ", dataMessage)
                else:
                    # I need to check if the package is correct
                    if(dataMessage.SN == self.RN):
                        writeOnLog("Log", "", "", "","Receiving! : Correct package", 0)
                        writeOnLog("Log", self.connectionAddr, self.selfAddr, "RECV: valid Data package received ", dataMessage)
                        self.SN = dataMessage.RN
                        self.RN = (self.RN + 1)%2
                        ACKMessage = Message._make([self.selfAddr[1], self.connectionAddr[1], self.SN, self.RN, 8, False, True, False, False, False, "".encode('utf-8')])
                        encodedACKMessage = self.encodeMessage(ACKMessage)
                        writeOnLog("Log", self.connectionAddr, self.selfAddr, "RECV: ACK of a recived message ", ACKMessage)
                        self.socketUDP.sendto(encodedACKMessage, self.connectionAddr)
                        messageRecived.extend(dataMessage.data)
                        numTimeOuts = 0
                        firstPacket = False
                    else:
                        writeOnLog("Log", "", "", "", "Receiving! : Wrong package", 0)
                        writeOnLog("Log", self.connectionAddr, self.selfAddr, "RECV: Wrong package received ", dataMessage)
            else:
                #self.messageQueue.put(queueMessage)
                self.printQueue(self.messageQueue)
        writeOnLog("Log", "", "", "", "Receiving! : EL MESAJE FINAL ES: "+ str(messageRecived))
        return messageRecived


    # close, closes the connection, ie delete the connection sockect from the connectionSockets dictionary.
    def close(self):
        print("SocketPseudoTCP : Closing!")
        # I need to send a FIN message
        FINMMessage = Message._make([self.selfAddr[1], self.connectionAddr[1], self.SN, self.RN, 8, False, False, True, False, False, "".encode('utf-8')])
        encodedFINMessage = self.encodeMessage(FINMMessage)
        self.socketUDP.sendto(encodedFINMessage, self.connectionAddr)
        # I need to wait for a ACK message of my FIN message or another FIN message and answer it
        # First I wait for my connection FIN messages and answer it
        # Then I wait for the ack message of my FIN message
        # Finally I need to close the connection after some time
        self.connectionAddr = ("", -1)


    # "Server" side
    # bind, calls the bind method of the UDP port and starts the despacher. It also initialize the self.messageQueue with the maximun size pass as arg.
    def bind(self, selfAddr):
        writeOnLog("Log", "", "", "","SocketPseudoTCP : Binding!",0)
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
        writeOnLog("Log", "", "", "", "SocketPseudoTCP : Listening!", 0)
        # I only start the listen thread
        listenerThread = Thread(target=self.listenThread)
        listenerThread.daemon = True
        listenerThread.start()

    def listenThread(self):
        writeOnLog("Log", "", "", "", "SocketPseudoTCP : Listening Thread!", 0)
        while True:
            # I need to check if there is a SYN message on my messageQueue and answer it with a SYNACK message
            queueMessage = self.messageQueue.get()
            SYNMessage = queueMessage[0]
            if(SYNMessage.SYN and (not SYNMessage.ACK)):
                # I need to check if I alrrady have a connection with the sender
                if(not (queueMessage[1], SYNMessage.originPort) in self.connectionSockets):
                    # If the SYN message is valid
                    writeOnLog("Log", "", "", "", "Listening Thread! : Valid SYN message!", 0)
                    writeOnLog("Log", (queueMessage[1], SYNMessage.originPort), self.selfAddr, "Listen: New valid SYN Message ", SYNMessage)
                    # I need to store the new posible conection data
                    connectionSocket = SocketPseudoTCP()
                    connectionSocket.SN = randint(0, 1)
                    connectionSocket.RN = (SYNMessage.SN + 1) % 2
                    connectionSocket.selfAddr = self.selfAddr
                    self.connectionSockets[(queueMessage[1], SYNMessage.originPort)] = connectionSocket
                    # I need to send a SYNACK message in respond
                    SYNACKMessage = Message._make([connectionSocket.selfAddr[1],  SYNMessage.originPort, connectionSocket.SN, connectionSocket.RN, 8, True, True, False, False, False, "".encode('utf-8')])
                    encodedSYNACKMessage = self.encodeMessage(SYNACKMessage)
                    writeOnLog("Log", self.selfAddr, (queueMessage[1], SYNMessage.originPort), "Listen: SYN message response (SYNACK)", SYNACKMessage)
                    self.socketUDP.sendto(encodedSYNACKMessage, (queueMessage[1], SYNMessage.originPort))
                    self.messageQueue.task_done()
                    self.printQueue(self.messageQueue)
                else:
                    # If the conection already existed, I need to drop the invalid SYN message
                    print("Listening Thread Error! : The connection already existed!")
                    writeOnLog("Log", (queueMessage[1], self.selfAddr, SYNMessage.originPort), "Listen: The connection already existed", SYNMessage)
                    self.messageQueue.task_done()
                    self.printQueue(self.messageQueue)
                    continue
            else:
                # If it is not a SYN message, I need to put the message again on my messageQueue and try again
                writeOnLog("Log", "", "", "", "Listening Thread Error! : Not a SYN message!", 0)
                writeOnLog("Log", (queueMessage[1], self.selfAddr, SYNMessage.originPort), "Listen: Error! : Not a SYN message!", SYNMessage)
                self.messageQueue.put_nowait(queueMessage)
                self.messageQueue.task_done()
                self.printQueue(self.messageQueue)

    # accept, returns a instance of this class as the connection with the client socket that initiated the communication. Add the new connectionSocket (instance) to the connectionSockets dictionary
    def accept(self):
        writeOnLog("Log", "", "", "", "SocketPseudoTCP : Accepting!", 0)
        while True:
            # I need to check if there is a specal ACK message on my messageQueue and answer it with a regular ACK message
            queueMessage = self.messageQueue.get()
            specialACKMessage = queueMessage[0]
            if(specialACKMessage.ACK and not specialACKMessage.SYN):
                # If it is a special ACK message, I need to check if it is a valid one
                connectionSocket = self.connectionSockets.get((queueMessage[1], specialACKMessage.originPort))
                if(connectionSocket.RN == specialACKMessage.SN):
                    # It is a valid one, now I need to update the connectionSocket data
                    writeOnLog("Log", "", "", "", "Accepting! : valid special specialACK message!", 0)
                    connectionSocket.SN = specialACKMessage.RN
                    connectionSocket.RN = (specialACKMessage.SN + 1)%2
                    connectionSocket.connectionAddr = (queueMessage[1], specialACKMessage.originPort)
                    # I need to sent a regular ACK messages
                    writeOnLog("Log", connectionSocket.connectionAddr, self.selfAddr, "Accept: valid special specialACK message", specialACKMessage)
                    ACKMessage = Message._make([connectionSocket.selfAddr[1],  connectionSocket.connectionAddr[1], connectionSocket.SN, connectionSocket.RN, 8, False, True, False, False, False, "".encode('utf-8')])
                    encodedACKMessage = self.encodeMessage(ACKMessage)
                    writeOnLog("Log", self.selfAddr, connectionSocket.connectionAddr, "Accept: response of specialACK message", ACKMessage)
                    self.socketUDP.sendto(encodedACKMessage, connectionSocket.connectionAddr)
                    self.messageQueue.task_done()
                    self.printQueue(self.messageQueue)
                    writeOnLog("Log", "", "", "", "SERVER SN: " + str(connectionSocket.SN) + "  SERVER RN: " + str(connectionSocket.RN), 0)
                    return(connectionSocket, connectionSocket.selfAddr)
                else:
                    # It is a invalid one, I need to drop this message and try again
                    writeOnLog("Log", "", "", "", "Accepting Error! : Invalid special ACK message!", 0)
                    writeOnLog("Log", (queueMessage[1], specialACKMessage.originPort), self.selfAddr, "Accept: valid special specialACK message", specialACKMessage)
                    self.messageQueue.task_done()
                    self.printQueue(self.messageQueue)
                    continue
            else:
                #If it is not a special ACK message, I need to put the message again on my messageQueue and try again
                writeOnLog("Log", "", "", "", "Accepting Error! : Not a special ACK message!", 0)
                writeOnLog("Log", (queueMessage[1], specialACKMessage.originPort), self.selfAddr, "Accept: Not a special ACK message", specialACKMessage)
                self.messageQueue.put_nowait(queueMessage)
                self.messageQueue.task_done()
                self.printQueue(self.messageQueue)
    # Private methods
    # despatch, thread!, demultiplex all the messages send to the serverPort.
    def despatch(self):
        writeOnLog("Log", "", "", "", "SocketPseudoTCP : Despatching!", 0)
        while True:
            try:
                encodedMessage, senderAddr = self.socketUDP.recvfrom(2048)
            except Exception as e:
                writeOnLog("Log", "", "", "", "Despatching Error! : " + str(e), 0)
                continue
            # If everything was just fine
            # I need to demultiplex the recieved message
            writeOnLog("Log", "", "", "", "Despatching! : " + str(encodedMessage), 0)
            message = self.decodeMessage(encodedMessage)
            writeOnLog("Log", "", "", "", "Despatching! : " + str(message), 0)
            # First I need to check if the message if actually for me
            if(message.destinyPort == self.selfAddr[1]):
                writeOnLog("Log", "", "", "", "Despatching! : The mesage is for me!", 0)
                # Now I need to demultiplex the message
                # If the recieved message is a SYN or FIN it is for my messageQueue
                if(message.SYN):
                    self.messageQueue.put((message, senderAddr[0]))
                    self.printQueue(self.messageQueue);
                else:
                    writeOnLog("Log", "", "", "", "Despatching! : Fisrt you get the data, then you get the power, then you get the women", 0)
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
        writeOnLog("Log", "", "", "", "Encoder : Encoding message!", 0)
        # I need to encode the message parameter into a bytearray
        encodedMessage = ( message.originPort.to_bytes(2, byteorder='big') + message.destinyPort.to_bytes(2, byteorder='big')
        + message.SN.to_bytes(1, byteorder='big') + message.RN.to_bytes(1, byteorder='big') + message.headerSize.to_bytes(1, byteorder='big'))
        # If message is a SYNACK message
        if(message.SYN and message.ACK and not message.FIN):
            encodedMessage += SYNACK.to_bytes(1, byteorder='big')
        # If message is a SYN message
        elif(message.SYN):
            encodedMessage += SYN.to_bytes(1, byteorder='big')
        # If message is a "ACKSTART" message
        elif(message.ACK and message.START):
            encodedMessage += ACKSTART.to_bytes(1, byteorder='big')
        # If message is a "ACKEND" message
        elif(message.ACK and message.END):
            encodedMessage += ACKEND.to_bytes(1, byteorder='big')
        # If message is a ACK message
        elif(message.ACK):
            encodedMessage += ACK.to_bytes(1, byteorder='big')
        # If message is a FIN message
        elif(message.FIN):
            encodedMessage += FIN.to_bytes(1, byteorder='big')
        # If message is a START message
        elif(message.START):
            encodedMessage += START.to_bytes(1, byteorder='big')
        # If message is a END message
        elif(message.END):
            encodedMessage += END.to_bytes(1, byteorder='big')
        encodedMessage += message.data
        return encodedMessage

    # decodeMessage
    def decodeMessage(self, message):
        writeOnLog("Log", "", "", "", "Decoder : Decoding message!", 0)
        decodedMessageSYN = decodedMessageACK = decodedMessageFIN = decodeMessageSTART = decodeMessageEND = False
        if(int(message[7]) == SYNACK):
            decodedMessageSYN = decodedMessageACK = True
        elif(int(message[7]) == SYN):
            decodedMessageSYN = True
        elif(int(message[7]) == ACKSTART):
            decodedMessageACK = decodeMessageSTART = True
        elif(int(message[7]) == ACKEND):
            decodedMessageACK = decodeMessageEND = True
        elif(int(message[7]) == ACK):
            decodedMessageACK = True
        elif(int(message[7]) == FIN):
            decodedMessageFIN = True
        elif(int(message[7]) == START):
            decodedMessageSTART = True
        elif(int(message[7]) == END):
            decodedMessageEND = True
        decodedMessage = Message._make([ int.from_bytes(message[0:2], byteorder='big'), int.from_bytes(message[2:4], byteorder='big'),
        int(message[4]), int(message[5]), int(message[6]), decodedMessageSYN, decodedMessageACK, decodedMessageFIN, decodeMessageSTART, decodeMessageEND, message[7:] ])
        return decodedMessage

    #printQueue
    def printQueue(self, queue):
        print(list(queue.queue))
