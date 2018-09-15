import sys
import argparse
import threading

# Funtions
def print_error_invalid_ip():
    print("Error: invalid ip address")

def print_error_invalid_mask():
    print("Error: invalid subnet mask")

def print_error_invalid_port():
    print("Error: invalid port")

def printErrorOption():
    print("Select a valid option idiot!")

def validate_ip_address(ip):
    # Fisrt we split the string with the ip address, using the dot as separator, to obtain the decimal parts of the ip address
    ipTokens = ip.split(".")
    # We need to make sure the number of decimal parts is exacly four
    #print(ipTokens)
    if(not(len(ipTokens) == 4)):
        return False
    # We need to check the ip decimal parts are valid, ie are in the range [0, 255]
    for i in range(0,4):
        try:
            decimalPart = int(ipTokens[i])
        except ValueError:
            return False
        if(decimalPart < 0 or decimalPart > 255):
            return False
    return True

#Server
def serverThread():
    print("Server running!")
    global alcanzabilityTable
    alcanzabilityTable = alcanzabilityTable.upper()
    while(not beingDeleted): 
        True    

#Program
# We need to parse the arguments pass by the user
parser = argparse.ArgumentParser()
parser.add_argument("ip", help="recive the node ip address")
parser.add_argument("mask", help="recive the subnet mask, it must be a integer between 8 and 30", type=int)
parser.add_argument("port", help="recive the server port number", type=int)
args = parser.parse_args()
print ("ip address: " + args.ip + "\nsubnet mask: " + str(args.mask) + "\nport number: " + str(args.port))

# We need to make sure the arg pass by the user are valid
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


# We need to check if the ip address pass by the user is a valid ip address
if(not validate_ip_address(args.ip)):
    print_error_invalid_ip()
    sys.exit(-1)
print ("The provided ip address is valid! Hooray!")

# We need to create the shared data structure to store the "tabla de alcanzabilidad"
alcanzabilityTable = "alcanzability table"
beingDeleted = False

# We need to create a thread for the server functionality of the node
serverT = threading.Thread(target=serverThread, args=())
serverT.start()

#Client
clientMenu = '''
Select an option:
    0 : Delete node
    1 : Send message
    2 : Print alcanzabiliy table

'''

while(not beingDeleted):
    option = input(clientMenu)
    try:
        option = int(option)
    except ValueError:
        printErrorOption()
    if(option == 0):
        beingDeleted = True
    elif(option == 2):
        print(alcanzabilityTable)
sys.exit(0)
