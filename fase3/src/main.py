import sys
import argparse
from utilities import *
from node import *

# main funtion
if __name__ == '__main__':
    # We need to parse the arguments pass by the user
    parser = argparse.ArgumentParser(description='this program create a node with the recived arguments as input')
    parser.add_argument("ip", help="recive the node ip address")
    parser.add_argument("mask", help="recive the node subnet mask", type=int)
    parser.add_argument("port", help="recive the server port number", type=int)
    args = parser.parse_args()
    print ("main : ip address: " + args.ip + ", port number: " + str(args.port))

    # We need to make sure the arg pass by the user are valid

    # We need to check if the ip address pass by the user is a valid ip address
    if(is_valid_ipv4_address(args.ip)):
        print ("main : The provided ip address is valid! Hooray!")
    else:
        print_error_invalid_ip()
        sys.exit(-1)

    # We need to check if the subnet mask pass by the user is valid, ie is in the range [8, 30]
    if(args.mask < 8 or args.mask > 30):
        print_error_invalid_mask()
        sys.exit(-1)
    print ("main : The provided subnet mask is valid! Hooray!")

    # We need to check if the port pass by the user is valid, ie is in the range [1, 65535]
    if(args.port < 0 or args.port > 65535):
        print_error_invalid_port()
        sys.exit(-1)
    print ("main : The provided port is valid! Hooray!")

    # If all the arguments pass by the user are valid, we continue creating the node and executing it
    node = Node(args.ip, args.mask, args.port)
    node.run()

    print('main : main terminating...')
