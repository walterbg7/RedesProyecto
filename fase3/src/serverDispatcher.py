import csv
import os
import sys
from utilities import *
from socket import *
from threading import Thread

dicNeighbors = {}

#--------------------------------------------------------------------------------------------------------
def sendNeighborsList (clientAddress):
    listOfNeighbors = dicNeighbors[clientAddress] #We need the list of neighbors
    message = Message._make([selfPort, int(clientAddress[1]), REQUEST_ACK, listOfNeighbors.encode('utf-8')])
    finalMessage = encodeMessage(message) #We need to decode the message
    serverSocket.sendto(finalMessage, (clientAddress[0], int(clientAddress[1]))) #We send the decode message
    print("Message sended")
#------------------------------------------------SERVER UP -----------------------------------------------

with open('neighbors.csv', 'rt',  encoding="utf8") as csvfile2:
    neighborsReader = csv.DictReader(csvfile2)
    for row in neighborsReader:
        try:
            ipS = row['IPS']
            portS = row['PortS']
            ipD = row['IPD']
            portD = row['PortD']
            costD = row['Cost']
        except Exception as e:
            print("Error: Invalid csv file format!")
        # I need to check if the parameter in the csv file are valid
        if(not is_valid_ipv4_address(ipS)):
            print("Error: Invalid ip address = "+str(ipS))
            sys.exit(-1);
        try:
            portSInt = int(portS)
        except ValueError:
            print_error_invalid_port()
            sys.exit(-1)
        if(portSInt < 0 or portSInt > 65535):
            print_error_invalid_port()
            sys.exit(-1)
        if(not is_valid_ipv4_address(ipD)):
            print("Error: Invalid ip address = "+str(ipD))
            sys.exit(-1);
        try:
            portDInt = int(portD)
        except ValueError:
            print_error_invalid_port()
            sys.exit(-1)
        if(portDInt < 0 or portDInt > 65535):
            print_error_invalid_port()
            sys.exit(-1)
        try:
            costDInt = int(costD)
        except ValueError:
            print_error_invalid_cost()
            sys.exit(-1)
        #Add to the dicNeighbors
        tupleK1 = (ipS, portSInt)
        tupleK2 = (ipD, portDInt)
        strValue1 = ""+str(ipD)+MESSAGE_PARTS_DIVIDER+str(portD)+MESSAGE_PARTS_DIVIDER+str(costD)+MESSAGES_DIVIDER
        strValue2 = ""+str(ipS)+MESSAGE_PARTS_DIVIDER+str(portS)+MESSAGE_PARTS_DIVIDER+str(costD)+MESSAGES_DIVIDER
        existK1 = dicNeighbors.get(tupleK1)
        existK2 = dicNeighbors.get(tupleK2)
        if((existK1 is None) and (existK2 is None)):
            dicNeighbors[tupleK1] = strValue1
            dicNeighbors[tupleK2] = strValue2
        elif((not existK1 is None) and (not existK2 is None)):
            dicNeighbors[tupleK1] = existK1 + strValue1
            dicNeighbors[tupleK2] = existK2 + strValue2
        elif((not existK1 is None) and (existK2 is None)):
            dicNeighbors[tupleK1] = existK1 + strValue1
            dicNeighbors[tupleK2] = strValue2
        else:
            dicNeighbors[tupleK2] = existK2 + strValue2
            dicNeighbors[tupleK1] = strValue1
print(dicNeighbors)

selfPort = 60000

serverSocket = socket(AF_INET, SOCK_DGRAM) #We create a UDP socket
serverSocket.bind(("", selfPort))

while (1):
    packedMessage, client = serverSocket.recvfrom(2048) #Receive message
    message = decodeMessage(packedMessage) #We need to decode the message
    clientAddress = client[0], message.originPort #We need to know the client addrs
    print(clientAddress)
    if clientAddress not in dicNeighbors: #IP is no in the Neighbors Dictionary
        print("Recived message from a invalid IP")
        continue

    print(message.flag)
    if message.flag == REQUEST: #Only request messages are answered
        newRequest = Thread(target=sendNeighborsList, args = (clientAddress,))
        newRequest.start()
        continue
    print("Message is not for request")
