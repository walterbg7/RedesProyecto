import csv
import os
import sys
from utilities import *
from threading import *

serverDispatcherSocket = socket(AF_INET, SOCK_DGRAM)
serverDispatcherSocket.bind((SERVER_DISPATCHER_IP, SERVER_DISPATCHER_PORT))
dicNeighbors = {}

def sendNeighborsList (clientAddress):
    print("ServerDispatcher : sendNeighborsList")
    listOfNeighbors = dicNeighbors[clientAddress] #We need the list of neighbors
    print("ServerDispatcher : <"+str(clientAddress)+"> neighbors :")
    for ind in listOfNeighbors:
        print(str(ind))
    requetedMessage = ActualizationMessage._make([REQUEST_ACK, len(listOfNeighbors), listOfNeighbors])
    encodedRequestedMessage = encode_message(requetedMessage) #We need to decode the message
    serverDispatcherSocket.sendto(encodedRequestedMessage, clientAddress) #We send the decode message

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
            cost = row['Cost']
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
            costInt = int(cost)
        except ValueError:
            print_error_invalid_cost()
            sys.exit(-1)
        #if(costInt < 20 or costInt > 100):
        #    print_error_invalid_cost()
        #    sys.exit(-1)
        #Add to the dicNeighbors
        key1 = (ipS, portSInt)
        key2 = (ipD, portDInt)
        value1 = (ipD, maskDInt, portDInt, costInt)
        value2 = (ipS, maskSInt, portSInt, costInt)
        existKey1 = dicNeighbors.get(key1)
        existKey2 = dicNeighbors.get(key2)
        if((existKey1 is None) and (existKey2 is None)):
            dicNeighbors[key1] = []
            dicNeighbors[key1].append(value1)
            dicNeighbors[key2] = []
            dicNeighbors[key2].append(value2)
        elif((not existKey1 is None) and (not existKey2 is None)):
            dicNeighbors[key1].append(value1)
            dicNeighbors[key2].append(value2)
        elif((not existKey1 is None) and (existKey2 is None)):
            dicNeighbors[key1].append(value1)
            dicNeighbors[key2] = []
            dicNeighbors[key2].append(value2)
        else:
            dicNeighbors[key2].append(value2)
            dicNeighbors[key1] = []
            dicNeighbors[key1].append(value1)
for k in dicNeighbors:
    print(str(k)+" : "+str(dicNeighbors[k]))

while (1):
    enodedMessage, client = serverDispatcherSocket.recvfrom(2048) #Receive message
    if client not in dicNeighbors: #IP is no in the Neighbors Dictionary
        print("ServerDispatcher Error : Recived message is from a invalid Node")
        continue
    message = decode_message(enodedMessage) #We need to decode the message
    if(message != None):
        if message.type == REQUEST: #Only request messages are answered
            newRequest = Thread(target=sendNeighborsList, args = (client, ))
            newRequest.daemon = True
            newRequest.start()
            continue
        else:
            print("ServerDispatcher Error : Recieved message is not a REQUEST message")
