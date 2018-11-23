from socket import *
from collections import namedtuple

# Constants
SERVER_DISPATCHER_IP = "127.0.0.1"
SERVER_DISPATCHER_PORT = 60000
TIMEOUT = 5

# Flags
ACTUALIZATION = 1
IS_ALIVE = 2
IS_ALIVE_ACK = 3
BROADCAST = 4
DATA = 5
COST_CHANGE = 6
DEAD = 7
REQUEST = 8
REQUEST_ACK = 9

# Global variables
clientMenu = '''
Select an option:
    0 : Delete node
    1 : Change cost
    2 : Print alcanzabiliy table

'''

TypeMessage = namedtuple("TypeMessage", ["type"])
ActualizationMessage = namedtuple("ActualizationMessage", ["type", "n", "data"])
BroadcastMessage = namedtuple("BroadcastMessage", ["type", "n"])
CostChangeMessage = namedtuple("BroadcastMessage", ["type", "cost"])
DataMessage = namedtuple("DataMessage", ["type", "IPS", "PortS", "IPD", "PortD", "n", "Data"])

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

def encodeMessage(message):
    encodedMessage = None
    if(isinstance(message, TypeMessage)):
        print("encodeMessage : TypeMessage")
        encodedMessage = message.type.to_bytes(1, byteorder='big')
    elif(isinstance(message, ActualizationMessage)):
        print("encodeMessage : ActualizationMessage")
    elif(isinstance(message, BroadcastMessage)):
        print("encodeMessage : BroadcastMessage")
    elif(isinstance(message, CostChangeMessage)):
        print("encodeMessage : CostChangeMessage")
    elif(isinstance(message, DataMessage)):
        print("encodeMessage : DataMessage")
    else:
        print("encodeMessage Error: Invalid message")
    return encodedMessage

def decodeMessage(encodedMessage):
    message = None
    messageType = encodedMessage[0]
    if(messageType == IS_ALIVE or messageType == IS_ALIVE_ACK or messageType == DEAD or messageType == REQUEST):
        print("decodeMessage : TypeMessage")
        message = TypeMessage._make([messageType])
    elif(messageType == ACTUALIZATION or messageType == REQUEST_ACK):
        print("decodeMessage : ActualizationMessage")
    elif(messageType == BROADCAST):
        print("decodeMessage : BroadcastMessage")
    elif(messageType == COST_CHANGE):
        print("decodeMessage : CostChangeMessage")
    elif(messageType == DATA):
        print("decodeMessage : DataMessage")
    else:
        print("decodeMessage Error: Invalid type of message")
    return message
