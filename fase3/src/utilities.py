from socket import *
from collections import namedtuple

# Constants
SERVER_DISPATCHER_IP = "127.0.0.1"
SERVER_DISPATCHER_PORT = 60000
TIMEOUT = 5
MAX_NUMBER_OF_TRIES = 5

TYPE = 0
N = 1
DATA = 3
LINE_SIZE = 10
IP = 0
MASK = 4
PORT = 5
COST = 7
KEEP_ALIVE_RATE = 60
ACTUALIZATION_RATE = 30

# Flags
ACTUALIZATION = 1
KEEP_ALIVE = 2
KEEP_ALIVE_ACK = 3
BROADCAST = 4
PURE_DATA = 5
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

ignoring = False

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

def is_valid_actualization_message(actualizationMessage):
    return True

def encode_ip_adrr(ip):
    ipTokens = ip.split('.')
    encodedIP = int(ipTokens[0]).to_bytes(1, byteorder='big')+int(ipTokens[1]).to_bytes(1, byteorder='big')+int(ipTokens[2]).to_bytes(1, byteorder='big')+int(ipTokens[3]).to_bytes(1, byteorder='big')
    return encodedIP

def encode_message(message):
    print("encodeMessage : "+str(message))
    encodedMessage = None
    if(isinstance(message, TypeMessage)):
        print("encodeMessage : TypeMessage")
        encodedMessage = message.type.to_bytes(1, byteorder='big')
    elif(isinstance(message, ActualizationMessage)):
        print("encodeMessage : ActualizationMessage")
        if(is_valid_actualization_message(message)):
            encodedMessage = message.type.to_bytes(1, byteorder='big') + message.n.to_bytes(2, byteorder='big')
            for it in message.data:
                encodedMessage += encode_ip_adrr(it[0]) + it[1].to_bytes(1, byteorder='big') + it[2].to_bytes(2, byteorder='big') + it[3].to_bytes(3, byteorder='big')
        else:
            print("encodeMessage Error: Invalid actualization message")
    elif(isinstance(message, BroadcastMessage)):
        print("encodeMessage : BroadcastMessage")
    elif(isinstance(message, CostChangeMessage)):
        print("encodeMessage : CostChangeMessage")
    elif(isinstance(message, DataMessage)):
        print("encodeMessage : DataMessage")
    else:
        print("encodeMessage Error: Invalid message")
    return encodedMessage

def decode_ip_addr(ip):
    decodedIP = ""+str(ip[0])+"."+str(ip[1])+"."+str(ip[2])+"."+str(ip[3])
    return decodedIP

def decode_message(encodedMessage):
    print("decodeMessage :"+str(encodedMessage))
    try:
        messageType = encodedMessage[TYPE]
    except Exception as e:
        print("decodeMessage Error: invalid encodedMessage")
        return None
    message = None
    if(messageType == KEEP_ALIVE or messageType == KEEP_ALIVE_ACK or messageType == DEAD or messageType == REQUEST):
        print("decodeMessage : TypeMessage")
        message = TypeMessage._make([messageType])
    elif(messageType == ACTUALIZATION or messageType == REQUEST_ACK):
        print("decodeMessage : ActualizationMessage")
        if(is_valid_actualization_message(encodedMessage)):
            n = int.from_bytes(encodedMessage[N:DATA], byteorder='big')
            data = []
            lineStart = DATA
            lineEnd = DATA + LINE_SIZE
            for ind in range(n):
                line = encodedMessage[lineStart:lineEnd]
                ip = decode_ip_addr(line[IP:MASK])
                mask = line[MASK]
                port = int.from_bytes(line[PORT:COST], byteorder='big')
                cost = int.from_bytes(line[COST:], byteorder='big')
                data.append((ip, mask, port, cost))
                lineStart = lineEnd
                lineEnd = lineStart + LINE_SIZE
            message = ActualizationMessage._make([messageType, n, data])
    elif(messageType == BROADCAST):
        print("decodeMessage : BroadcastMessage")
    elif(messageType == COST_CHANGE):
        print("decodeMessage : CostChangeMessage")
    elif(messageType == PURE_DATA):
        print("decodeMessage : DataMessage")
    else:
        print("decodeMessage Error: Invalid type of message")
    return message
