from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from collections import deque

class Queue():
    def __init__(self):
        self.queue = deque()
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.popleft()
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = deque()
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

total_rooms = len(room_graph)
visited = set()

# run a dft to complete test
def get_directions():
    # breadcrumbs stack to keep track of path travelled, to use to return to last unexplored path
    breadcrumbs = Stack()
    follow_breadcrumb = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
    # until all rooms have been explored...
    while len(visited) < len(world.rooms):
        # add the current room to visited set
        visited.add(player.current_room)
        # get neighbors
        exits = player.current_room.get_exits()
        # (re)initialize list of connected, unexplored rooms
        unexplored_rooms = []
        # check to see if neighbors in visited
        for direction in exits:
            if player.current_room.get_room_in_direction(direction) not in visited:
                # add any unexplored rooms to unexplored list
                unexplored_rooms.append(direction)

        # if there are any unexplored neighbors, choose a neighbor and travel to it
        if len(unexplored_rooms) > 0:
            # pick a random direction
            travel_direction = random.choice(unexplored_rooms)
            # add travel direction to traversal path, move the player and place breadcrumb
            traversal_path.append(travel_direction)
            player.travel(travel_direction)
            breadcrumbs.push(travel_direction)
        else:
            # if there are no unexplored paths, follow breadcrumb back and record on traversal path
            breadcrumb = breadcrumbs.pop()
            traversal_path.append(follow_breadcrumb[breadcrumb])
            player.travel(follow_breadcrumb[breadcrumb])

get_directions()
print(traversal_path)
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
