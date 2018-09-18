# Constants
clientMenu = '''
Select an option:
    0 : Delete node
    1 : Send message
    2 : Print alcanzabiliy table

'''

# Funtions
def print_error_invalid_ip():
    print("Error: invalid ip address")

def print_error_invalid_mask():
    print("Error: invalid subnet mask")

def print_error_invalid_port():
    print("Error: invalid port")

def print_error_option():
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
