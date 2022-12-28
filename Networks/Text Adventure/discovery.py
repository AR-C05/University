# discovery class. discovery service
import signal
from socket import *
import sys
from urllib.parse import urlparse

# to control if debugging statements print
DEBUGGING = False

DISCOVERY_PORT = 9999

# socket for the discovery service
discovery_socket = socket(AF_INET, SOCK_DGRAM)

# dictionary of all registered rooms
# key: room name
# value: room url
ROOMS = {}

# handle Ctrl+c and exit server gracefully
def sigint_handler(sig, frame):
    print("Interrupt Received; Shutting Down.\n")
    sys.exit(0)

# register a room name with it's url in the ROOMS dictionary
def register(url, name):
    try:
        if (DEBUGGING):
            print(f"Registery:  {ROOMS}")
            print(f"New name: {name};   New URL: {url}")
            print()

        # is the url a valid url?
        server_address = urlparse(url)
        if ((server_address.scheme != 'room') or (server_address.port == None) or (server_address.hostname == None)):
            raise ValueError

        # does a room with the given name already registered?
        if name in ROOMS:
            return f"NOTOK A room with the name {name} already exists."
        
        # is a room already registered at the given URL?
        if url in ROOMS.values():
            return f"NOTOK A room already exists at that url"

        # valid new registration. register and return "OK" response
        ROOMS[name] = url
        return "OK"

    except ValueError:
        # room change did not occur. display server response
        return "NOTOK Invalid URL for registration"

# deregister room with given name (i.e. remove entry from dictionary with key=name)
# send appropriate response
def deregister(name):
    try:
        if (DEBUGGING):
            print(f"Registery:  {ROOMS}")
            print(f"Deregistration name: {name}")
            print()
        ROOMS.pop(name)
        return "OK"
    except KeyError:
        return "NOTOK Attempt to deregister an unregistered room"

# if registered, return address of room with specified name
def lookup(name):
    if (DEBUGGING):
        print(f"Registery:  {ROOMS}")
        print(f"LOOKUP name: {name}")
        print()
    if name in ROOMS:
        return f"OK {ROOMS[name]}"
    return "NOTOK Attempting to access an unregistered room"

# process incoming message
def process_message(msg, address):
    response = ''
    words = msg.split()
    command = words[0].lower()
    # parse incoming message; determine which command, process if valid
    # registration request from a game room (coming online)
    if (command == 'register'):
        if (len(words) == 3):
            response = register(words[1], words[2])
        else:
            response = "NOTOK Invalid format for REGISTER"
    # deregistration request from a game room (going offline)
    elif (command == 'deregister'):
        if (len(words) == 2):
            response = deregister(words[1])
        else:
            response = "NOTOK Invalid format for DEREGISTER"
    # lookup request from a client (want url of room with specified name)
    elif (command == 'lookup'):
        if (len(words) == 2):
            response = lookup(words[1])
        else:
            response = "NOTOK Invalid format for LOOKUP"
    # invalid command
    else:
        response = "NOTOK Invalid Command"
    return response

# main function
def main():
    # register the signal handler for SIGINT (ctrl+c) (i.e. for shutting down)
    signal.signal(signal.SIGINT, sigint_handler)

    discovery_socket.bind(('', DISCOVERY_PORT))
    while True:
        # receive and process packet
        msg, addr = discovery_socket.recvfrom(2048)

        decoded_message = msg.decode()

        # process message and retrieve response
        response = process_message(decoded_message, addr)

        # respond
        discovery_socket.sendto(response.encode(), addr)


if __name__ == '__main__':
    main()
