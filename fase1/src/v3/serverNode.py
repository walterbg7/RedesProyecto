from threading import Thread
from utilities import *

class ServerNode(Thread):

    # Constructor
    def __init__(self, port, table, ip):
        Thread.__init__(self)
        self.port = port
        self.alcanzabilityTable = table
        self.ip = ip
        fileLock.acquire()
        try:
            fileBi = open("bitacora.txt", 'r+')
            fileBi.read()
        except:
            fileBi = open("bitacora.txt", 'w')
        fileBi.write("New server, ip: "+str(self.ip)+", port: "+str(self.port)+"\n")
        fileBi.write("\n\n")
        fileBi.close()
        fileLock.release()
        print("ServerNode : Constructor :)")
    
    def run(self):
        fileLock.acquire()
        fileBi = open("bitacora.txt", 'r+')
        fileBi.read()
        fileBi.write("Server, ip: "+str(self.ip)+", port: "+str(self.port)+"\n")
        fileBi.write("ServerNode : Receiving messages and stuff!\n")
        fileBi.write("ServerNode : I'm dying!\n")
        fileBi.write("\n\n")
        fileBi.close()
        fileLock.release()
        print("ServerNode : Receiving messages and stuff!")
        print("ServerNode : I'm dying!")

    def unpackMessage(self, packedMessage):
        print("ServerNode : Unpacking the message ...")
        if(len(packedMessage) == 1):
            if(packedMessage[0] == 0):
                return "0"
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
            listDel = []
            for itr in self.alcanzabilityTable:
                if(self.alcanzabilityTable[itr][1] == clientAddr):
                    listDel.append(itr)
            for it in listDel:
                del self.alcanzabilityTable[it]
            del listDel
        elif(msj == "18"):
            pass
        else:
            msg = msj.split('/')
            maximo = int(msg[0]) * 3
            i = 1
            while(i < maximo):
                tupleK = (str(msg[i]), str(msg[i+1])) # key
                tupleV = (str(msg[i+2]), clientAddr) # value
                if(tupleK in self.alcanzabilityTable):
                    if(int(self.alcanzabilityTable[tupleK][0]) > int(tupleV[0])):
                        self.alcanzabilityTable[tupleK] = tupleV
                else:
                    self.alcanzabilityTable[tupleK] = tupleV
                i += 3
        aTLock.release()
