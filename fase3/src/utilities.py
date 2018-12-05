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
ACTUALIZATION_RATE = 10
BROADCAST_JUMPS = 5
IGNORING_TIME = 20#3 * ACTUALIZATION_RATE

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
    3 : Send message

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

def print_error_invalid_cost():
    print("Error: invalid cost")

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

def decode_ip_addr(ip):
    ipF = ''
    for itr in range (3):
        ipF += str(int.from_bytes(ip[itr])) + '.'
    ipF += str(int.from_bytes(ip[3]))
    print(ipF)

def encode_message(message):
    #print("encode_message : "+str(message))
    encodedMessage = None
    if(isinstance(message, TypeMessage)):
        #print("encode_message : TypeMessage")
        encodedMessage = message.type.to_bytes(1, byteorder='big')
    elif(isinstance(message, ActualizationMessage)):
        #print("encode_message : ActualizationMessage")
        if(is_valid_actualization_message(message)):
            encodedMessage = message.type.to_bytes(1, byteorder='big') + message.n.to_bytes(2, byteorder='big')
            for it in message.data:
                encodedMessage += encode_ip_adrr(it[0]) + it[1].to_bytes(1, byteorder='big') + it[2].to_bytes(2, byteorder='big') + it[3].to_bytes(3, byteorder='big')
        else:
            print("encode_message Error: Invalid actualization message")
    elif(isinstance(message, BroadcastMessage)):
        #print("encode_message : BroadcastMessage")
        try:
            messageType = message.type.to_bytes(1, byteorder='big')
        except Exception as e:
            print("encode_message Error: Invalid broadcast message type")
            messageType = None
        try:
            messageN = message.n.to_bytes(2, byteorder='big')
        except Exception as e:
            print("encode_message Error: Invalid broadcast message type")
            messageN = None
        if(messageType != None and messageN != None):
            encodedMessage = messageType + messageN
    elif(isinstance(message, CostChangeMessage)):
        try:
            encodedMessage = message.type.to_bytes(1, byteorder='big') + message.cost.to_bytes(3, byteorder='big')
            print("encode_message : CostChangeMessage")
        except:
            print("encode_message Error: Invalid CostChange message type")
            messageN = None
    elif(isinstance(message, DataMessage)):
        try:
            encodedMessage = message.type.to_bytes(1, byteorder='big')
            encodedMessage += encode_ip_adrr(message.IPS)
            encodedMessage += message.PortS.to_bytes(2, byteorder='big')
            encodedMessage += encode_ip_adrr(message.IPD)
            encodedMessage += message.PortD.to_bytes(2, byteorder='big')
            encodedMessage += message.n.to_bytes(2, byteorder='big')
            encodedMessage += message.Data.encode('utf-8')
         #   print("encode_message : DataMessage")
        except:
            print("encode_message Error: Data message type")
            messageN = None
    else:
        print("encode_message Error: Invalid message")
    return encodedMessage

def decode_ip_addr(ip):
    decodedIP = ""+str(ip[0])+"."+str(ip[1])+"."+str(ip[2])+"."+str(ip[3])
    return decodedIP

def decode_message(encodedMessage):
    #print("decode_message :"+str(encodedMessage))
    try:
        messageType = encodedMessage[TYPE]
    except Exception as e:
        print("decode_message Error: invalid encodedMessage")
        return None
    message = None
    if(messageType == KEEP_ALIVE or messageType == KEEP_ALIVE_ACK or messageType == DEAD or messageType == REQUEST):
        #print("decode_message : TypeMessage")
        message = TypeMessage._make([messageType])
    elif(messageType == ACTUALIZATION or messageType == REQUEST_ACK):
        #print("decode_message : ActualizationMessage")
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
        else:
            print("decode_message Error: Invalid actualization message")
    elif(messageType == BROADCAST):
        #print("decode_message : BroadcastMessage")
        if(len(encodedMessage)==3):
            n = int.from_bytes(encodedMessage[N:], byteorder='big')
            message = BroadcastMessage._make([messageType, n])
        else:
            print("decode_message Error: Invalid broadcast message")
    elif(messageType == COST_CHANGE):
        if(len(encodedMessage)==4):
            cost = int.from_bytes(encodedMessage[1:], byteorder = 'big')
            message = CostChangeMessage._make([messageType, cost])
            #print("decode_message : CostChangeMessage")
        else:
            print("Decode message error (Cost Change)")
    elif(messageType == PURE_DATA):
        if(len(encodedMessage) > 14):
            #("DataMessage", ["type", "IPS", "PortS", "IPD", "PortD", "n", "Data"])
            IPs = decode_ip_addr(encodedMessage[1:5])
            PortS = int.from_bytes(encodedMessage[5:7], byteorder='big')
            IPd = decode_ip_addr(encodedMessage[7:11])
            Portd = int.from_bytes(encodedMessage[11:13], byteorder='big')
            n = int.from_bytes(encodedMessage[13:15], byteorder='big')
            data = encodedMessage[15:].decode('utf-8')
            message = DataMessage._make([messageType, IPs, PortS, IPd, Portd, n, data])
        else:
            print('Decode message error (Data)')
        #print("decode_message : DataMessage")
    else:
        print("decode_message Error: Invalid type of message")
    return message
