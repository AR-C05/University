# player class. game client

import argparse
import selectors
import signal
from socket import *
import sys
from urllib.parse import urlparse

# to control if debugging statements print
DEBUGGING = False

# port for discovery service
DISCOVERY_PORT = 9999
# timeout for server response (in seconds)
TIMEOUT = 5

# Socket for exchanging messages with server
client_socket = socket(AF_INET, SOCK_DGRAM)
# server address
server = ('', '')
# user name
username = ''
# player inventory
inventory = []

# setting up selector
sel = selectors.DefaultSelector()

# Toggles to determine if server message is in response to a user command (and needs some action other than simple outputting it)
# or an independent message from server (or other command response that simply needs to be printed)
TAKE = False
ROOM_CHANGE = False

# handle Ctrl+c for graceful client exit.  Let the server know when we're gone.
def sigint_handler(sig, frame):
    print("Interrupt Received; Shutting Down.\n")
    msg = 'exit'
    client_socket.sendto(msg.encode(), server)
    for item in inventory:
        drop(item)
    sys.exit(0)

# function for selector to read from socket connection to room server
def read_socket(sock, mask):
    global TAKE
    global ROOM_CHANGE
    msg, addr = sock.recvfrom(1024)
    msg = msg.decode()
    if (TAKE):
        TAKE = not TAKE
        handle_take_response(msg)
    elif (ROOM_CHANGE):
        ROOM_CHANGE = not ROOM_CHANGE
        handle_room_change_response(msg)
    else:
        print()
        if msg == 'disconnect':
            print("Disconnected from server ... exiting!")
            sys.exit(0)
        print(msg)
    # display prompt to user after server message has been handled
    prompt()

# function for selector to read user input from stdin
def read_stdin(file, mask):
    userinput = input().strip()
    process_command(userinput)

# join a room
def join():
    msg = f'join {username}'
    client_socket.sendto(msg.encode(), server)
    response, addr = client_socket.recvfrom(1024)
    print(response.decode())

# lookup server address based on name from the discovery
def lookup_room(name):
    if (DEBUGGING):
        print(f'Attempting to lookup: {name}')
    global server
    lookup_message = f'LOOKUP {name}'
    # set timeout on client_socket
    client_socket.settimeout(TIMEOUT)
    try:
        client_socket.sendto(lookup_message.encode(), ('', DISCOVERY_PORT))
        if (DEBUGGING):
            print(f'Sent Request: {lookup_message}')
        message, address = client_socket.recvfrom(1024)
        if (DEBUGGING):
            print(f'Received Response: {message.decode()}')
        message = message.decode()
        # if (DEBUGGING):
        #     print(f'Received Response: {message}')

        # check if discovery sent url of next room
        if (message.split()[0] == 'OK'):
            return message[3:]
        # discovery sent NOTOK response
        else:
            print(message[6:])
            sys.exit(-1)
    except timeout:
        print("Could not connect to discovery service. Terminating.")
        sys.exit(0)

# handle server response to room change command (nsewup)
def handle_room_change_response(msg):
    global server
    response_from_room = msg.split()

    # room server sent a room name
    if (len(response_from_room) == 1):
        url = lookup_room(msg)        
        try:
            server_address = urlparse(url)
            if ((server_address.scheme != 'room') or (server_address.port == None) or (server_address.hostname == None)):
                raise ValueError
            host = server_address.hostname
            port = server_address.port
            server = (host, port)

            # set timeout on client_socket
            client_socket.settimeout(TIMEOUT)
            try:
                join()
            except timeout:
                print("You attempted to cross over to the next room.")
                print("Unfortunately for you, it was a trap.")
                print("You are DEAD! x_x")
                print("=======")
                print("=======")
                print("Reality: Timed Out. Could not connect to server for next room.")
                sys.exit(-1)
        except ValueError:
            # room change did not occur. display server response
            print("Terminating. Exited previous room; could not get url of next room from discovery")
            # print(url)
            sys.exit(-1)
    # room server sent an error message (i.e. did not send name of a room to move to)
    else:
        print(msg)

# handle server response to take command
def handle_take_response(msg):
    print(msg)
    words = msg.split()
    if ((len(words) == 2) and (words[1] == 'taken')):
        inventory.append(words[0])


# simple user prompt setup
def prompt(skipline=False):
    if (skipline):
        print("")
    print("> ", end='', flush=True)

# drop specified item if it is in inventory, send message to server
def drop(item):
    if (item in inventory):
        msg = f'drop {item}'
        client_socket.sendto(msg.encode(), server)
        # response, addr = client_socket.recvfrom(1024)
        # print(response.decode())
        inventory.remove(item)
    else:
        print(f'You are not holding {item}')

# process command from user; check and send to server as necessary
def process_command(userinput):
    global server
    
    # parse command
    words = userinput.split()
    command = words[0].lower().strip()

    # exit command
    if (command == 'exit'):
        client_socket.sendto(userinput.encode(), server)
        for item in inventory:
            drop(item)
        sys.exit(0)

    # look command
    elif (command == 'look'):
        client_socket.sendto(userinput.encode(), server)

    # inventory command
    elif (command == 'inventory'):
        print("You are holding:")
        if (len(inventory) == 0):
            print('  No items')
        else:
            for item in inventory:
                print(f'  {item}')
        # display prompt to user
        prompt()

    # take command
    elif (command == 'take'):
        global TAKE
        TAKE = not TAKE
        client_socket.sendto(userinput.encode(), server)

    # check drop command
    elif (command == 'drop'):
        if len(words) != 2:
            print("Invalid Command")
            return
        else:
            drop(words[1].strip())

    # room change command
    elif command in ['north', 'south', 'east', 'west', 'up', 'down']:
        global ROOM_CHANGE
        ROOM_CHANGE = not ROOM_CHANGE
        # handle changing room
        client_socket.sendto(command.encode(), server)

    # other command; simply convey the message to server
    else:
        client_socket.sendto(userinput.encode(), server)

# main function
def main():
    global username
    global client_socket
    global server

    # register the signal handler for SIGINT (ctrl+c) (i.e. for shutting down)
    signal.signal(signal.SIGINT, sigint_handler)

    # set up argparse to check command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="name for the player in the game")
    parser.add_argument("server", help="name for the server to connect to at startup")
    args = parser.parse_args()

    # ensure valid URL. if so, save host and port info
    try:
        room_name = "_".join((args.server).split()).lower()
        if (DEBUGGING):
            print(f'Room name: {room_name}')
        url = lookup_room(room_name)
        if (DEBUGGING):
            print(f'URL: {url}')
        server_address = urlparse(url)
        if ((server_address.scheme != 'room') or (server_address.port == None) or (server_address.hostname == None)):
            raise ValueError
        host = server_address.hostname
        port = server_address.port
        server = (host, port)
    except ValueError:
        print('Error:  Discovery did not return a URL of the form:  room://host:port')
        sys.exit(1)

    # set timeout on client_socket
    client_socket.settimeout(TIMEOUT)

    # get username from args
    username = args.name

    # message to enter room
    try:
        join()
    except timeout:
        print("Timed Out. Could not connect to server.")
        sys.exit(-1)

    # register the socket and stdin to selectors
    client_socket.setblocking(False)
    sel.register(client_socket, selectors.EVENT_READ, read_socket)
    sel.register(sys.stdin, selectors.EVENT_READ, read_stdin)

    # prompt the user
    prompt()

    # loop forever; exchange messages with server, report results
    while True:
        # utilising selectors as per documentation
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)



if __name__ == '__main__':
    main()
