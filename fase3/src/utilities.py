import threading
from socket import *
from collections import namedtuple

# Constants
SERVERD_IP = "127.0.0.1"
SERVERD_PORT = 60000
# Flags
REQUEST = 2 #Flag to request message
REQUEST_ACK = 3
DATA = 0
NORMAL_ACK = 4
MESSAGE_PARTS_DIVIDER = "/"
MESSAGES_DIVIDER = "&"

# Global variables
clientMenu = '''
Select an option:
    0 : Delete node
    1 : Change cost (disabled)
    2 : Print alcanzabiliy table

'''
Message = namedtuple("Message", ["originPort", "destPort", "flag", "data"]) #Structure of the message

# Locks
aTLock = threading.Lock()
fileLock = threading.Lock()

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
    print("Error: invalid message, please check the message format on the 'Hint' text")

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
    fileLock.acquire()
    try:
        fileBi = open("log.txt", 'r+')
        fileBi.read()
    except:
        fileBi = open("log.txt", 'w')
    if(strHeader is not None):
        fileBi.write(strHeader+"\n")
    fileBi.write(strToWrite+"\n")
    fileBi.write("\n-----------------------------------------------------------------------\n\n")
    fileBi.close()
    fileLock.release()

def encodeMessage(message):
    # I need to encode the message parameter into a bytearray
    print(message)
    encodedMessage = (message.originPort.to_bytes(2, byteorder='big') +
        message.destPort.to_bytes(2, byteorder='big') +
        message.flag.to_bytes(1, byteorder = 'big'))
    encodedMessage += message.data
    print(encodedMessage)
    return encodedMessage

def decodeMessage(packedMessage):
    print(packedMessage)
    #self.writeOnLog("Decoder : Decoding message!", "Control Message:")
    decodedMessage = Message._make([ int.from_bytes(packedMessage[0:2], byteorder='big'),
    int.from_bytes(packedMessage[2:4], byteorder='big'),
    int.from_bytes(packedMessage[4:5], byteorder='big'),
    packedMessage[5:]])
    return decodedMessage
