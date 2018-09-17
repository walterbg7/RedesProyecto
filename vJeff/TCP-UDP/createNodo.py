import sys
import argparse
import threading
import fileinput
import numpy

# Funtions

#To validate
def print_error_invalid_ip():
    print("Error: invalid ip address")

def print_error_invalid_mask():
    print("Error: invalid subnet mask")

def print_error_invalid_port():
    print("Error: invalid port")

def validate_ip_address(ip):
    # Fisrt we split the string with the ip address, using the dot as separator, to obtain the decimal parts of the ip address
    ip_tokens = ip.split(".")
    # We need to make sure the number of decimal parts is exacly four
    #print(ipTokens)
    if(not(len(ip_tokens) == 4)):
        return False
    # We need to check the ip decimal parts are valid, ie are in the range [0, 255]
    for i in range(0,4):
        try:
            decimal_part = int(ip_tokens[i])
        except ValueError:
            return False
        if(decimal_part < 0 or decimal_part > 255):
            return False
    return True

#Server
class Server:
    def server_thread(self):
        # We need to create a new terminal
        print("Server running!") # We need to print this message on the newly created terminal
        global alcanzability_table
        alcanzability_table = alcanzability_table.upper()
        global being_deleted
        while (being_deleted): 
            True 

#Client
class Client:
    def print_error_invalid_n(self):
        print("Error invalid value to n")

    def print_error_option(self):
        print("Select a valid option idiot!")

    def delete_node(self):
        global being_deleted
        being_deleted = True

    def send_message(self):
        # we need to read the user message it form the terminal
        ask_client_message = '''
    Remember the message struture is:
        ni
        ip/mask/cost
        ip/mask/cost
        .
        .
        .
    
    
    '''
        print(ask_client_message)
        n = input("Write the number of lines of the message (n): ")
        try:
            n = int(n)
        except ValueError:
            self.print_error_invalid_n()
            return
        client_message = ""
        client_message += str(n) + "\n"
        for i in range (n):
            client_message += input() + "\n"
        print(client_message)
   
 
    def print_alcanzability_table(self):
        global alcanzability_table
        print (alcanzability_table)

    def client_thread(self):
        client_menu = '''
    Select an option:
        0 : Delete node
        1 : Send message
        2 : Print alcanzabiliy table

    '''
        global being_deleted
        while(not being_deleted):
            option = input(client_menu)
            try:
                option = int(option)
            except ValueError:
                self.print_error_option()
            if(option == 0):
                self.delete_node()
            elif(option == 1):
                self.send_message()
            elif(option == 2):
                self.print_alcanzability_table()

#Program
# We need to parse the arguments pass by the user
parser = argparse.ArgumentParser()
parser.add_argument("ip", help="recive the node ip address")
parser.add_argument("mask", help="recive the subnet mask, it must be a integer between 8 and 30", type=int)
parser.add_argument("port", help="recive the server port number", type=int)
args = parser.parse_args()
print ("ip address: " + args.ip + "\nsubnet mask: " + str(args.mask) + "\nport number: " + str(args.port))

# We need to make sure the arg pass by the user are valid

# We need to check if the ip address pass by the user is a valid ip address
if(not validate_ip_address(args.ip)):
    print_error_invalid_ip()
    sys.exit(-1)
print ("The provided ip address is valid! Hooray!")

# We need to check if the subnet mask pass by the user is valid, ie is in the range [8, 30]
if(args.mask < 8 or args.mask > 30):
    print_error_invalid_mask()
    sys.exit(-1)
print ("The provided subnet mask is valid! Hooray!")

# We need to check if the port pass by the user is valid, ie is in the range [1, 65535]
if(args.port < 0 or args.port > 65535):
    print_error_invalid_port()
    sys.exit(-1)
print ("The provided port is valid! Hooray!")

#We need to create the objects Client and Server
client = Client()
server = Server()

# We need to create the shared data structure to store the "tabla de alcanzabilidad"
alcanzability_table = "alcanzability table"
being_deleted = False

# We need to create a thread for the server functionality of the node
serverT = threading.Thread(target=server.server_thread(), args=())
serverT.start()
clientT = threading.Thread(target=client.client_thread(), args=())
clientT.start()

sys.exit(0)
