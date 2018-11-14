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
