from socket import *
from clientNode import *

class ClientNodeTCP(ClientNode):

    #Constructor
    def __init__(self, ip, port):
        ClientNode.__init__(self, ip, port)
        #We need to keep a list of conections
        self.conections = {}
        print("ClientNodeTCP : Constructor :)")

    # Overwrite father class send method
    def sendMessage(self, serverName, serverPort, message):
       # We need to send the message
        idConection = str(serverName) + "-" + str(serverPort)
        if(idConection in self.conections):
            print("Existing connection")
            try:
                self.conections[idConection].send(message)
                modifiedSentence = self.conections[idConection].recv(1024)
                print ("From Server: " + modifiedSentence.decode('utf-8'))
                # If the server died
                if((modifiedSentence.decode('utf-8')) != "✓✓"):
                    print("RIP server")
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
            except Exception as e:
                print("No connection can't be established: ",e)
    def stop(self):
        print("Client TCP: Stoping!")
        stopMessage = self.packMessage("0")
        for key in self.conections:
            self.conections[key].send(stopMessage)
            self.conections[key].close()
