import threading
from socket import *

# Constants
clientMenu = '''
Select an option:
    0 : Delete node
    1 : Send message
    2 : Print alcanzabiliy table

'''

# Locks
aTLock = threading.Lock()
fileLock = threading.Lock()

# Funtions
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
    pass

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
