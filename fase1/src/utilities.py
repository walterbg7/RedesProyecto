import threading
from socket import *

# Constants
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

aTLock = threading.Lock()
fileLock = threading.Lock()

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

def validateRow(row):
    rowList = row.split("/")
    if(len(rowList) < 3):
        print("Error: Incorrect message struture")
        return False
    else:
    	ipR = rowList[0]
    	if(not is_valid_ipv4_address(ipR)):
    		print("Error: The IP is invalid")
    		return False
    	try:
    		maskR = int(rowList[1])
    	except ValueError:
    		print("Error: The mask must be int")
    		return False
    	if(maskR<8 or maskR>30):
    		print("Error: The mask is invalid")
    		return False
    	try:
    		costR = int(rowList[2])
    	except ValueError:
    		print("Error: The cost must be int")
    		return False
    	ipRList = ipR.split(".")
    	ipRBin = ""
    	for i in ipRList:
    		bits = str(bin(int(i)))
    		bits = bits[2:]
    		if(len(bits)<8):
    			numBitsMissing = 8-len(bits)
    			bitsMissing = ""
    			for j in range(0, numBitsMissing):
    				bitsMissing += "0"
    			bits = bitsMissing + bits
    		ipRBin += bits
    	#print(ipRBin)
    	for it in range(maskR, 32):
    		if(ipRBin[it]!="0"):
    			print("Error: It is not a valid network address")
    			return False
    	#print("Nice One!")
    	return True

def writeOnBita(strToWrite, strHeader = None):
    fileLock.acquire()
    try:
        fileBi = open("bitacora.txt", 'r+')
        fileBi.read()
    except:
        fileBi = open("bitacora.txt", 'w')
    if(strHeader is not None):
        fileBi.write(strHeader+"\n")
    fileBi.write(strToWrite+"\n")
    fileBi.write("\n-----------------------------------------------------------------------\n\n")
    fileBi.close()
    fileLock.release()
