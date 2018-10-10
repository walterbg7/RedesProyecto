from socket import *
from queue import *
from random import randint

class SocketPseudoTCP:

    # Constructor
    def __init__(self):
        # Fields
        # selfAddr, self ip addr and port
        # connectioAddr, connection ip addr and port
        # messageQueue, Queue to store the recived message to this sockect
        messageQueue = Queue();
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
            print("clientSocketSide : this is my selfAddr " + str(self.selfAddr))
            try:
                self.socketUDP.bind(self.selfAddr)
            except:
                print("clientSocketSide : unsuccessful bind, repeating!")
                continue
            successfulBind = True

        # I need to send the SYN message to start the handshake process with the wanted serverSocket 

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
        pass

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
        pass



s = SocketPseudoTCP()
