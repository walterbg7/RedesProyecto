import csv
import os
import sys
from utilities import *
from socket import *
from threading import Thread

dicNeighbors = {}

def sendNeighborsList (clientAddress):
    listOfNeighbors = dicNeighbors[clientAddress] #We need the list of neighbors
    message = Message._make([REQUEST_ACK, None, listOfNeighbors.encode('utf8')])
    encodedMessage = encodeMessage(message) #We need to decode the message
    serverDispatcherSocket.sendto(encodedMessage, clientAddress) #We send the decode message
    print("Message sended")

with open('neighbors.csv', 'rt',  encoding="utf8") as csvfile2:
    neighborsReader = csv.DictReader(csvfile2)
    for row in neighborsReader:
        try:
            ipS = row['IPS']
            maskS = row['MaskS']
            portS = row['PortS']
            ipD = row['IPD']
            maskD = row['MaskD']
            portD = row['PortD']
            costD = row['Cost']
        except Exception as e:
            print("Error: Invalid csv file format!")
            sys.exit(-1)
        # I need to check if the parameter in the csv file are valid
        if((not is_valid_ipv4_address(ipS)) or (not is_valid_ipv4_address(ipD))):
            print("Error: Invalid ip address")
            sys.exit(-1)
        try:
            maskSInt = int(maskS)
            maskDInt = int(maskD)
        except ValueError:
            print_error_invalid_mask()
            sys.exit(-1)
        if((maskSInt < 8 or maskSInt > 30) or (maskDInt < 8 or maskDInt > 30)):
            print_error_invalid_mask()
            sys.exit(-1)
        try:
            portSInt = int(portS)
            portDInt = int(portD)
        except ValueError:
            print_error_invalid_port()
            sys.exit(-1)
        if((portSInt < 0 or portSInt > 65535) or (portDInt < 0 or portDInt > 65535)):
            print_error_invalid_port()
            sys.exit(-1)
        try:
            costDInt = int(costD)
        except ValueError:
            print_error_invalid_cost()
            sys.exit(-1)
        #Add to the dicNeighbors
        key1 = (ipS, portSInt)
        key2 = (ipD, portDInt)
        strValue1 = ""+ipD+MESSAGE_PARTS_DIVIDER+maskD+MESSAGE_PARTS_DIVIDER+portD+MESSAGE_PARTS_DIVIDER+costD+MESSAGE_LINES_DIVIDER
        strValue2 = ""+ipS+MESSAGE_PARTS_DIVIDER+maskS+MESSAGE_PARTS_DIVIDER+portS+MESSAGE_PARTS_DIVIDER+costD+MESSAGE_LINES_DIVIDER
        existK1 = dicNeighbors.get(key1)
        existK2 = dicNeighbors.get(key2)
        if((existK1 is None) and (existK2 is None)):
            dicNeighbors[key1] = strValue1
            dicNeighbors[key2] = strValue2
        elif((not existK1 is None) and (not existK2 is None)):
            dicNeighbors[key1] = existK1 + strValue1
            dicNeighbors[key2] = existK2 + strValue2
        elif((not existK1 is None) and (existK2 is None)):
            dicNeighbors[key1] = existK1 + strValue1
            dicNeighbors[key2] = strValue2
        else:
            dicNeighbors[key2] = existK2 + strValue2
            dicNeighbors[key1] = strValue1
print(dicNeighbors)

serverDispatcherSocket = socket(AF_INET, SOCK_DGRAM) #We create a UDP socket
serverDispatcherSocket.bind((SERVER_DISPATCHER_IP, SERVER_DISPATCHER_PORT))

while (1):
    enodedMessage, client = serverDispatcherSocket.recvfrom(2048) #Receive message
    message = decodeMessage(enodedMessage) #We need to decode the message
    print(client)
    if client not in dicNeighbors: #IP is no in the Neighbors Dictionary
        print("Recived message from a invalid IP")
        continue

    print(message.flag)
    if message.flag == REQUEST: #Only request messages are answered
        newRequest = Thread(target=sendNeighborsList, args = (client, ))
        newRequest.start()
        continue
    print("Message is not a REQUEST message")
