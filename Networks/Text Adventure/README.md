# README

`room.py` - server for the game  
`player.py` - client for the game  
`discovery.py` - discovery service for the game  
<br/>
***Commands***:
<hr/>

*look* - look around the room  
*take ITEM* - pick up item from room  
*inventory* - view player inventory  
*say MSG* - send a public message to all in the room  
*drop ITEM* - drop an item from inventory  
*north* - move to north room (same with other directions: south, east, west, up, down)  
*exit* - leave the game

***NOTE:*** for the `take` and `drop` commands, must match case of the item. "Book" is NOT the same as "book"
<br/><br/>

### TLDR
----
`discovery.py` - start first: `python3 discovery.py`  

`room.py` - start any rooms (servers) that should be online next: 
- `python3 room.py [-m CONNECTED_ROOM] NAME DESCRIPTION [ITEMS]`
- -m is represents a direction; followed by name of the connected room
- possible directions: n,s,e,w,u,d (u = up; d = down)
- `ITEMS` (if any) MUST be immediately after `DESCRIPTION`  

`player.py` - start instance of a player:   `python3 player.py USERNAME SERVER_NAME`


## Details
----

FIRST: start discovery service so servers and clients can connect  
```cmd
python3 discovery.py
```

NEXT: start server(s): `python3 room.py NAME DESC ITEMS`  
`NAME` is the server (room) name  
`DESC` is the room description  
`ITEMS` is the list of items in the room (optional)

specify any connected rooms using options [n,s,e,w,u,d] representing a room connection going north, south, east, west, up, down respectively  
Ex.
- -n NorthernRoom
- -d "Shadow Basement"

\*\*\****NOTE***: items must be single word ("green_apple" NOT "green apple")\*\*\*

***Examples***:  
In the following order:
- multiple items, no connected rooms
- one item in room, no connected rooms
- room without any items, no connected rooms
```cmd
python3 room.py "The dark kitchen" "The dark kitchen is a normal kitchen without any light available" fork spoon green_apple

python3 room.py "The dark kitchen" "The dark kitchen is a normal kitchen without any light available" fork

python3 room.py "The dark kitchen" "The dark kitchen is a normal kitchen without any light available"
```
Examples of connected rooms:  
- 2 rooms, connected north-south (north from room1 = room2, south from room2 = room1)
```cmd
python3 room.py "The Southern Room" "The Southern Room is a room at the southern end of the map. There is a path to the north." Book Paper Pen -n "The Northern Room"

python3 room.py "The Northern Room" "The Northern Room is a room at the southern end of the map. There is a path to the south." Computer -s "The Southern Room"
```
- 3 rooms, central room connected to both other rooms
    - West Wing - east to Central Room - north to Northern Room
```cmd
python3 room.py "West Room" -e "Central Room" "The West Room, has a path to the east" Western_Movies_Collection

python3 room.py -w "West Room" -n "The Northern Room" "Central Room" "The Central Room. Has paths to the west and to the north" Map Compass

python3 room.py "Northern Room" "The Northern Room. Has a path to the south" jacket gloves hat -s "Central Room"
```
optional argument(s) (n/s/e/w/u/d) can be anywhere, but must have the corresponding RoomName immediately after  
\*\*\****EXCEPT between `DESC` and `ITEMS`***  
i.e. `ITEMS` (if any) MUST be immediately after `DESC`

use `python3 room.py -h` for detailed usage help  
<br><br>

Start ***client(s)*** after server(s) started:  
pass in `UserName` and `ServerName` as command line arguments  
`UserName` - name of user; one word only  
`ServerName` - name of server  

Examples:
```cmd
python3 player.py ILoveBatman RoomName

python3 player.py I_Love_Superman MyRoom
```

To Exit:
- Client:  
    - `exit` command or `ctrl+c` keyboard interrupt signal
- Server, Discovery Service:
    - `ctrl+c` from keyboard
