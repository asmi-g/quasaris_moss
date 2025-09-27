from socket import socket, AF_INET, SOCK_DGRAM
from argparse import ArgumentParser
# define command line interface
parser = ArgumentParser()
parser.add_argument('-ip', help='IP')
parser.add_argument('-server_port', type=int, help='Server port')
# parse command line options
args = parser.parse_args()
# create a UDP socket
with socket(AF_INET, SOCK_DGRAM) as server_socket:
    # bind server with a specific network address
    # which consists of IP and port number
    server_socket.bind((args.ip, args.server_port))

    print(f'UDP server up and listening on {args.ip}:{args.server_port}')
    # wait for the incoming data
    data, client_address = server_socket.recvfrom(1024)
    print(f'Received message from {client_address[0]}:{client_address[1]} : {data.decode()}')
    # send response to client
    server_socket.sendto('Message received'.encode(), client_address)
