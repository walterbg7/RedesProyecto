import csv
import os
import sys
from utilities import *

with open('nodes.csv', 'rt',  encoding="utf8") as csvfile:
    nodesReader = csv.DictReader(csvfile)
    for row in nodesReader:
        try:
            ip = row['IP']
            mask = row['Mask']
            port = row['Port']
        except Exception as e:
            print("Error: Invalid csv file format!")
        print(ip, mask, port)
        # I need to check if the parameter in the csv file are valid
        if(not is_valid_ipv4_address(ip)):
            print("Error: Invalid ip address")
            sys.exit(-1);
        try:
            maskInt = int(mask)
        except ValueError:
            print_error_invalid_mask()
            sys.exit(-1)
        if(maskInt < 8 or maskInt > 30):
            print_error_invalid_mask()
            sys.exit(-1)
        try:
            portInt = int(port)
        except ValueError:
            print_error_invalid_port()
            sys.exit(-1)
        if(portInt < 0 or portInt > 65535):
            print_error_invalid_port()
            sys.exit(-1)
        # I need to create a new terminal and run the 'node.py' program with the row parameters on that terminal
        os.system("gnome-terminal -x python3 node.py"+' '+ip+' '+mask+' '+port)

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
        tupleK = (ipS, portS)
        strValue = ""+str(ipD)+"/"+str(portD)+"/"+str(costD)+" "
        exist = dicNeighbors.get(tupleK)
        if(not exist):
            dicNeighbors[tupleK] = strValue
        else:
            exist += strValue
            dicNeighbors[tupleK] = exist

print(dicNeighbors)
