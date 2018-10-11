from socket import *
from queue import *
from random import randint
from threading import Thread
from collections import namedtuple

Message = namedtuple("Message", ["originPort", "destinyPort", "SYN", "ACK", "FIN", "headerSize", "data"])

class SocketPseudoTCP:

    # Constructor
    def __init__(self):
        # Fields
        # selfAddr, self ip addr and port
        # connectioAddr, connection ip addr and port
        # messageQueue, Queue to store the recived message to this sockect
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

        # I need to check if the parameters are valid

        # I need to create a new random port number (it is also a socket id) and make bind on it
        successfulBind = False
        while( not successfulBind ):
            self.selfAddr = ("", randint(1024, 65535))
            #self.selfAddr = ("", 80)
            print("clientSocketSide : this is my selfAddr " + str(self.selfAddr))
            try:
                self.bind(self.selfAddr)
            except:
                print("clientSocketSide : unsuccessful bind, repeating!")
                continue
            successfulBind = True

        # I need to send the SYN message to start the handshake process with the wanted serverSocket
        SYNMessage = Message._make([self.selfAddr[1], serverAddr[1], True, False, False, 8, "".encode('utf-8')])
        print(str(SYNMessage))
        encodedSYNMessage = self.encodeMessage(SYNMessage)
        print(str(encodedSYNMessage))

        self.socketUDP.sendto(encodedSYNMessage, serverAddr)

    # send, sends a byte array or encoded message.
    def send(self, message):
        print("SocketPseudoTCP : Sending!")
        pass

    # recv, recive the number of bytes passed as arg. Returns a the received message as encoded message o a byte array
    def recv(self, numberOfBytes):
        print("SocketPseudoTCP : Receiving!")
        pass

    # close, closes the connection, ie delete the connection sockect from the connectionSockets dictionary.
    def close(self):
        print("SocketPseudoTCP : Closing!")
        pass

    # "Server" side
    # bind, calls the bind method of the UDP port and starts the despacher. It also initialize the self.messageQueue with the maximun size pass as arg.
    def bind(self, selfaddr):
        print("SocketPseudoTCP : Binding!")
        self.socketUDP.bind(selfaddr)
        # I need to start the despacher thread
        despacherThread = Thread(target=self.despatch)
        despacherThread.daemon = True
        despacherThread.start()

    # listen, thread!, search the server socket messageQueue for a SYN message and proccess it.
    def listen(self, serverQueueSize):
        print("SocketPseudoTCP : Listening!")
        pass

    # accept, returns a instance of this class as the connection with the client socket that initiated the communication. Add the new connectionSocket (instance) to the connectionSockets dictionary
    def accept(self):
        print("SocketPseudoTCP : Accepting!")
        pass

    # Private methods
    # despatch, thread!, demultiplex all the messages send to the serverPort.
    def despatch(self):
        print("SocketPseudoTCP : Despatching!")
        while(1):
            message, senderAddr = self.socketUDP.recvfrom(2048)
            print("Despacher: message = " + message.decode('utf-8') + ", sender addr = " + str(senderAddr))
            # I need to check if the recived message is really for me
            # If the message was really for me then I need to demultiplex it

    def encodeMessage(self, message):
        print("Encoder : Encoding message!")
        if(isinstance(message, Message)):
            # I need to encode the message parameter into a bytearray
            encodedMessage = ( message.originPort.to_bytes(2, byteorder='big') + message.destinyPort.to_bytes(2, byteorder='big')
            + int(message.SYN).to_bytes(1, byteorder='big') + int(message.ACK).to_bytes(1, byteorder='big') + int(message.FIN).to_bytes(1, byteorder='big')
            + message.headerSize.to_bytes(1, byteorder='big') + message.data )
            return encodedMessage
        else:
            print ("Error: encodeMessage, invalid message :(")
            return ":("

    def decodeMessage(self, message):
        print("Decoder : Decoding message!")
        decodedMessage = Message._make([ int.from_bytes(message[0:2], byteorder='big'), int.from_bytes(message[2:4], byteorder='big'),
        bool(message[4]), bool(message[5]), bool(message[6]), int(message[7]), message[8:] ])
        return decodedMessage
