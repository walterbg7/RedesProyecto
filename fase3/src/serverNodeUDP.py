from socket import *
from serverNode import *

class ServerNodeUDP(ServerNode):

    # Constructor
    def __init__(self, ip, mask, port, table, listN):
        ServerNode.__init__(self, ip, mask, port, table, listN)
        self.serverSocket = socket(AF_INET, SOCK_DGRAM) #We create a UDP socket
        self.serverSocket.bind((self.ip, self.port))
        print("ServerNodeUDP : Constructor")

    def getNeighborsFromServer(self):
        # We create a neighbor request message
        message = Message._make([self.port, 60000, REQUEST, "".encode('utf-8')])
        encodedMessage = encodeMessage(message)
        noNeighbors = True
        while(noNeighbors):
            # Send the message to the dealer
            try:
                self.serverSocket.sendto(encodedMessage, (SERVERD_IP, SERVERD_PORT))
            except Exception as e:
                print("ServerNodeUDP : Error asking for my neighbors", str(e))
                continue
        # Wait for the answer
            try:
                modifiedMessage, serverAddress = self.serverSocket.recvfrom(2048)
            except:
                print("ServerNodeUDP : Error receiving message from serverDispatcher", str(e))
            recvMessage = decodeMessage(modifiedMessage)
            print ("ServerNodeUDP : From Dealer: ", recvMessage)
            if(recvMessage.flag == REQUEST_ACK):
                noNeighbors = False
                myNeighbors = recvMessage.data.decode('utf-8')
                myNeighborsTokens = myNeighbors.split(MESSAGES_DIVIDER)
                for ind in myNeighborsTokens:
                    print(ind)
            else:
                print("ServerNodeUDP : Error no REQUEST_ACK message")
                continue

    def run(self):
        getNeighborsFromServerThread = Thread(target=self.getNeighborsFromServer, args=())
        getNeighborsFromServerThread.start()
        print("ServerNodeUDP : Receiving stuff")
        while(1):
            continue
