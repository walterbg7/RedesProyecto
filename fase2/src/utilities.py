import threading
from socket import *

# Constants
separator = "-"

clientMenu = '''
Select an option:
    0 : Delete node
    1 : Send message
    2 : Print alcanzabiliy table

'''

askClientMessage = '''
Please enter the message:
Hint: Remember the message struture is:
    ni
    ip/mask/cost
    ip/mask/cost
    .
    .
    .

'''

fileLock = threading.Lock()
aTLock = threading.Lock()

askIPAddressMessage = "Please, put the destination ip address: "
askPortMessage = "Please, put the destination port number: "
askNMessage = "Write the number of lines of the message (n): "

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
'''
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
'''

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
'''
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
''
def writeOnLog(fileName, originAddr, destAddr, action, message, type = 1):
    fileLock.acquire()
    log = open(fileName, "a")
    if type:
        log.write("Transmitter: " + str(originAddr) + "\nReceiver: " + str(destAddr)+ "\nAction: " + str(action) +  "\nMessage: " + str(message))
    else:
        log.write("Control Message: "+ message)
    log.write("\n" + separator * 130 + "\n")
    log.close()
    fileLock.release()

    strH = "Transmitter: " + str((queueMessage[1], SYNMessage.originPort)) + "\nReceiver: " + str(self.selfAddr)+ "\nListen: New valid SYN Message "
    strB = "Message: " + str(SYNMessage)
    writeOnLog(strB, strH)
'''
