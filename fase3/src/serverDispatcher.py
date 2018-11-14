import csv
import os
import sys
from utilities import *
from socket import *
from threading import Thread

dicNeighbors = {}

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
        tupleK = (ipS, portSInt)
        strValue = ""+str(ipD)+"/"+str(portD)+"/"+str(costD)+" "
        exist = dicNeighbors.get(tupleK)
        if(exist is None):
            dicNeighbors[tupleK] = strValue
        else:
            dicNeighbors[tupleK] = exist + strValue

print(dicNeighbors)

#--------------------------------------------------------------------------------------------------------

def sendNeighborsList (clientAddress):
    listOfNeighbors = dicNeighbors[clientAddress] #We need the list of neighbors
    message = Message._make([selfPort, int(clientAddress[1]), 2, listOfNeighbors.encode('utf-8')])
    finalMessage = encodeMessage(message) #We need to decode the message
    serverSocket.sendto(finalMessage, (clientAddress[0], int(clientAddress[1]))) #We send the decode message
    print("Message sended")

#------------------------------------------------SERVER UP -----------------------------------------------


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
