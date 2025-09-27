from socket import socket, AF_INET, SOCK_DGRAM
from argparse import ArgumentParser

# create UDP message payload
payload = 'sup'

# define command line interface
parser = ArgumentParser()
parser.add_argument('-ip', help='IP')
parser.add_argument('-server_port', type=int, help='Server port')
# parse command line options
args = parser.parse_args()
# create a UDP socket
with socket(AF_INET, SOCK_DGRAM) as client_socket:
    # send message to server
    print(f'Sending message to {args.ip}:{args.server_port}')
    client_socket.sendto(payload.encode(), (args.ip, args.server_port))
    # receive response from server
    data, server_address = client_socket.recvfrom(1024)
    print(f'Received response from {server_address[0]}:{server_address[1] }: {data.decode()}')
