import threading
from socket import *
from collections import namedtuple

# Constants
SERVER_DISPATCHER_IP = "127.0.0.1"
SERVER_DISPATCHER_PORT = 60000
MESSAGE_PARTS_DIVIDER = "/"
MESSAGE_LINES_DIVIDER = "&"

# Flags
CATASTROPHE = 0 #The number of hops are counted
KEEP_ALIVE = 1
KEEP_ALIVE_ACK = 2
DATA = 4
REQUEST = 8
REQUEST_ACK = 16
CHANGE_COST = 32
CHANGE_KILL = 64

# Global variables
clientMenu = '''
Select an option:
    0 : Delete node
    1 : Change cost
    2 : Print alcanzabiliy table

'''

Message = namedtuple("Message", ["flag", "n", "data"])

# Locks
aTLock = threading.Lock()
logFileLock = threading.Lock()

# Functions
def print_error_invalid_ip():
    print("Error: invalid ip address")

def print_error_invalid_mask():
    print("Error: invalid subnet mask")

def print_error_invalid_port():
    print("Error: invalid port")

def print_error_option():
    print("Error: Select a valid option!")

def print_error_invalid_n():
    print("Error: Please select a valid number of message lines (n > 0)")

def print_error_invalid_message():
    print("Error: invalid message")

def print_error_invalid_cost():
    print("Error: invalid cost")

def is_valid_ipv4_address(address):
    try:
        inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            inet_aton(address)
        except error:
            return False
        return address.count('.') == 3
    except error:  # not a valid address
        return False
    return True

def is_valid_network_ipv4_address(address, mask):
    if(is_valid_ipv4_address(address)):
        return True
    else:
        return False

def writeOnLog(strToWrite, strHeader = None):
    logFileLock.acquire()
    try:
        logFile = open("log.txt", 'r+')
        logFile.read()
    except:
        logFile = open("log.txt", 'w')
    if(strHeader is not None):
        logFile.write(strHeader+"\n")
    logFile.write(strToWrite+"\n")
    logFile.write("\n-----------------------------------------------------------------------\n\n")
    logFile.close()
    logFileLock.release()

def encodeMessage(message):
    encodedMessage = None
    if(message.flag == REQUEST):
        encodedMessage = REQUEST.to_bytes(1, byteorder='big')
    elif(message.flag == REQUEST_ACK):
        encodedMessage = REQUEST_ACK.to_bytes(1, byteorder='big') + message.data
    elif(message.flag == KEEP_ALIVE):
        encodedMessage = KEEP_ALIVE.to_bytes(1, byteorder='big')
    elif(message.flag == KEEP_ALIVE_ACK):
        encodedMessage = KEEP_ALIVE_ACK.to_bytes(1, byteorder='big')
    else:
        print("encodeMessage : Invalid flag")
    return encodedMessage

def decodeMessage(encodedMessage):
    message = None
    if(encodedMessage[0] == REQUEST):
        message = Message._make([REQUEST, None, None])
    elif(encodedMessage[0] == REQUEST_ACK):
        message = Message._make([REQUEST_ACK, None, encodedMessage[1:]])
    elif(encodedMessage[0] == KEEP_ALIVE):
        message = Message._make([KEEP_ALIVE, None, None])
    elif(encodedMessage[0] == KEEP_ALIVE_ACK):
        message = Message._make([KEEP_ALIVE_ACK, None, None])
    else:
        print("encodeMessage : Invalid flag")
    return message
