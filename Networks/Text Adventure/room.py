# room class. game server

from socket import *
import signal
import sys
import argparse
from urllib.parse import urlparse

# port for discovery service
DISCOVERY_PORT = 9999

# saved room information
# display_name: server name for displaying. matches user input
display_name = ""
# name: server name for communication. spaces removed, lowercased for ease of use
name = ''
description = ''
items = []
connections = []  # current clients in room in tuple format (username, address)

# valid arguments
valid_args = ["join", "look", "take", "drop", "exit", "say"]

# rooms potentially accessible from current room:
north_room = ''
south_room = ''
east_room = ''
west_room = ''
up_room = ''
down_room = ''

# create the room's socket
room_socket = socket(AF_INET, SOCK_DGRAM)

# handle Ctrl+c and exit server gracefully
def sigint_handler(sig, frame):
    print("Interrupt Received; Shutting Down.\n")
    # inform discovery server and all connected clients of termination
    inform_all("disconnect", '')
    deregister_message = f'DEREGISTER {name}'
    room_socket.sendto(deregister_message.encode(), ('', DISCOVERY_PORT))
    sys.exit(0)

# describe room, return description as a string
def room_description():
    global display_name
    global description
    global items
    global connections
    
    # name and description of room
    info = f'{display_name}\n\n{description}\n\n'

    # any items in room (not including players)
    if len(items) == 0 and len(connections) <= 1:
        info += "The room is empty.\n"
    else:
        info += "The room contains:"
        for item in items:
            info += f'\n\t{item}'

    return info

# get list of names of players currently in room (excluding the player at specified connection)
# one name per line
# return a string
def other_players_in_room(current_connection):
    others = ''
    for connection in connections:
        if connection[0] != current_connection[0]:
            others += f"\n\t{connection[0]}"
    return others

# add player to client list "connections" (list of tuples: (username, address))
def add_client(client):
    connections.append(client)

# remove player from client list "connections" (list of tuples: (username, address))
def remove_client(client):
    if client in connections:
        connections.remove(client)
        # print(f'{client[0]} from address {client[1]} removed')  # for testing purpose

# given player's name, return corresponding tuple from client list "connections" of form (username, address)
# return None if player not found
def get_client_by_name(username=''):
    for connection in connections:
        if connection[0] == username:
            return connection
    return None

# given player's address, return corresponding tuple from client list "connections" of form (username, address)
# return None if player not found
def get_client_by_address(address):
    for connection in connections:
        if connection[1] == address:
            return connection
    return None

# look command
# return string of room summary (including other players in room)
def look(client):
    info = room_description() + other_players_in_room(client) + "\n"
    return info

# inform all users except the user at specified connection of given message
def inform_all(msg, addr):
    # print(msg) # for testing purposes
    for client in connections:
        if client[1] != addr:
            room_socket.sendto(msg.encode(), client[1])

# process incoming message
def process_message(message, addr):
    global valid_args

    # parse message
    words = message.split()
    # get the command
    command = words[0].strip().lower()

    # If player is joining the server, add them to the list of players.
    # inform all other players that this player joined
    if (command == 'join'):
        if len(words) == 2:
            add_client((words[1], addr))
            print(f"User {words[1]} joined from address {addr}")
            inform_all(f'{words[1]} entered the room.', addr)
            return look((words[1], addr))
        else:
            return "Invalid Command"

    # If player is leaving the server. remove them from the list of players.
    elif(command == 'exit'):
        inform_all(f'{get_client_by_address(addr)[0]} left the game.', addr)
        remove_client(get_client_by_address(addr))
        return "Goodbye"

    # If player looks around, give them the room summary.
    elif(command == 'look'):
        return look(get_client_by_address(addr))

    # If player takes an item, make sure it is here and give it to the player.
    elif(command == 'take'):
        if len(words) == 2:
            if words[1] in items:
                items.remove(words[1])
                return f'{words[1]} taken'
            else:
                return f'{words[1]} cannot be taken in this room'
        else:
            return "Invalid Command"

    # If player drops an item, put in in the list of things here.
    elif(command == 'drop'):
        if len(words) == 2:
            items.append(words[1])
            return f'{words[1]} dropped'
        else:
            return 'Invalid Command'

    # If a player says something, 
    elif(command == 'say'):
        if len(words) >= 2:
            # convey message part of 'say' command to all other users
            msg = message[4:].strip()
            # print(msg) # for testing purpose
            inform_all(f'{get_client_by_address(addr)[0]} said "{msg}"', addr)
            return f'You said "{msg}"'
        else:
            return 'What did you want to say?'

    # room movement commands (north/south/east/west/up/down)
    # if a room exists (movement direction is in list of valid commands "valid_args") process the move; inform other players of move
    # else inform player that it is not possible to move in that direction (no room in that direction)
    elif(command == 'north'):
        if  command in valid_args:
            # print(f'{get_client_by_address(addr)[0]} left the room, heading {command}.')
            inform_all(f'{get_client_by_address(addr)[0]} left the room, heading {command}.', addr)
            remove_client(get_client_by_address(addr))
            return north_room
        else:
            return f'Moving {command} is not possible'
    elif(command == 'south'):
        if  command in valid_args:
            # print(f'{get_client_by_address(addr)[0]} left the room, heading {command}.')
            inform_all(f'{get_client_by_address(addr)[0]} left the room, heading {command}.', addr)
            remove_client(get_client_by_address(addr))
            return south_room
        else:
            return f'Moving {command} is not possible'
    elif(command == 'east'):
        if  command in valid_args:
            # print(f'{get_client_by_address(addr)[0]} left the room, heading {command}.')
            inform_all(f'{get_client_by_address(addr)[0]} left the room, heading {command}.', addr)
            remove_client(get_client_by_address(addr))
            return east_room
        else:
            return f'Moving {command} is not possible'
    elif(command == 'west'):
        if  command in valid_args:
            # print(f'{get_client_by_address(addr)[0]} left the room, heading {command}.')
            inform_all(f'{get_client_by_address(addr)[0]} left the room, heading {command}.', addr)
            remove_client(get_client_by_address(addr))
            return west_room
        else:
            return f'Moving {command} is not possible'
    elif(command == 'up'):
        if  command in valid_args:
            # print(f'{get_client_by_address(addr)[0]} left the room, heading {command}.')
            inform_all(f'{get_client_by_address(addr)[0]} left the room, heading {command}.', addr)
            remove_client(get_client_by_address(addr))
            return up_room
        else:
            return f'Moving {command} is not possible'
    elif(command == 'down'):
        if  command in valid_args:
            # print(f'{get_client_by_address(addr)[0]} left the room, heading {command}.')
            inform_all(f'{get_client_by_address(addr)[0]} left the room, heading {command}.', addr)
            remove_client(get_client_by_address(addr))
            return down_room
        else:
            return f'Moving {command} is not possible'

    # Otherwise, the command is bad.
    else:
        return "Invalid Command"


# main function
def main():
    global display_name
    global name
    global description
    global items
    global connections

    # register the signal handler for SIGINT (ctrl+c) (i.e. for shutting down)
    signal.signal(signal.SIGINT, sigint_handler)

    # set up argparse to check command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="name of the room")
    parser.add_argument("description", help="description of the room")
    parser.add_argument("item", nargs='*', help="items found in the room by default")
    parser.add_argument("-n", metavar="North", help="room to NORTH. Name of the room")
    parser.add_argument("-s", metavar='South', help="room to SOUTH. Name of the room")
    parser.add_argument("-e", metavar="East", help="room to EAST. Name of the room")
    parser.add_argument("-w", metavar="West", help="room to WEST. Name of the room")
    parser.add_argument("-u", metavar="Up", help="room going UP. Name of the room")
    parser.add_argument("-d", metavar="Down", help="room going DOWN. Name of the room")
    args = parser.parse_args()


    # get data from the command line args
    display_name = args.name
    name = "_".join(display_name.split()).lower()
    description = args.description
    items = args.item
    # parse optional arguments for possible connected rooms
    # add specified directions to list of valid commands
    # store a no-spaces, lowercased, version of corresponding room name
    if (args.n is not None):
        global north_room
        north_room = "_".join((args.n).split()).lower()
        valid_args.append("north")
    if (args.s is not None):
        global south_room
        south_room = "_".join((args.s).split()).lower()
        valid_args.append("south")
    if (args.e is not None):
        global east_room
        east_room = "_".join((args.e).split()).lower()
        valid_args.append("east")
    if (args.w is not None):
        global west_room
        west_room = "_".join((args.w).split()).lower()
        valid_args.append("west")
    if (args.u is not None):
        global up_room
        up_room = "_".join((args.u).split()).lower()
        valid_args.append("up")
    if (args.d is not None):
        global down_room
        down_room = "_".join((args.d).split()).lower()
        valid_args.append("down")

    # starting description of room
    print("Room Starting Description: ")
    print(room_description())

    # bind socket. any interface, port assigned by system.
    room_socket.bind(('', 0))
    port = room_socket.getsockname()[1]
    register_message = f'REGISTER room://localhost:{port} {name}'
    room_socket.sendto(register_message.encode(), ('', DISCOVERY_PORT))
    message, address = room_socket.recvfrom(2048)
    message = message.decode()
    registration_response = message.split()[0]
    if (registration_response == "NOTOK"):
        print(message[6:])
        sys.exit(0)

    # debugging to check if port was assigned properly
    # print("Room will wait for players at port: " + str(port))
    print()

    # stay on and process messages from clients until receive interrupt
    while True:
        # receive and process packet from client
        message, addr = room_socket.recvfrom(2048)

        # process message and retrieve response
        response = process_message(message.decode(), addr)

        # send response to client
        room_socket.sendto(response.encode(),addr)


if __name__ == '__main__':
    main()
