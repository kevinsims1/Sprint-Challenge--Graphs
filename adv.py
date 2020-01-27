from player import Player
from world import World
from util import Graph, Stack, Queue
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()
player = Player(world.starting_room)
graph = Graph()

# Populate graph by traversing through all the rooms using a depth first traversal
def dft():
    #Create Stack
    stack = Stack()
    #Put the starting point in the stack
    stack.push(world.starting_room)

    # Create a set to keep track of where we've been
    visited = set()

    #While the stack is not empty
    while stack.size() > 0:
        # grabs room instance off of stack
        room = stack.pop()
        # Grabbing the specific ID 
        room_id = room.id

        # If room not in graph
        if room_id not in graph.vertices:
            # Add it
            graph.add_vertex(room_id)

        # Get an array of available exits(Edges) of that room
        exits = room.get_exits()

        # For each exit
        for direction in exits:
            # Grab the exits room.id
            exit_room = room.get_room_in_direction(direction)
            exit_room_id = exit_room.id

            # If exit room not in graph, add it
            if exit_room_id not in graph.vertices:
                graph.add_vertex(exit_room_id)

            # Make a connection from initial room to exit. Make note of direction as well
            graph.add_edge(room_id, exit_room_id, direction)

            # If we haven't already visited exit room, add it to the stack
            if exit_room_id not in visited:
                stack.push(exit_room)

        visited.add(room_id)

# Searches for the nearest unvisited space using a Breadth First Search
def bfs(room_id, visited, graph_=graph):
    """
    Takes in a room id and a set of visited room ids
    returns a set of moves that the player can take to get to the nearest unvisited space.
    """
    #Create a queue
    queue = Queue()
    
    #Enqueue the starting point
    queue.enqueue([room_id, []])

    # Make a set to keep track of where we've been
    visited_bfs = set()

    # Add our current room
    visited_bfs.add(room_id)
    
    # While our queue is not empty 
    while queue.size() > 0:

        # Grab our recent list of room and moves 
        room, moves = queue.dequeue()

        # Grab neighbors of room
        neighbors = graph_.get_neighbors(room)

        # Grabs keys. These are directions
        neighbors_keys = list(neighbors.keys())

        # WE've hit a new dead end. 
        if len(neighbors_keys) == 1 and neighbors[neighbors_keys[0]] not in visited:
            # Return set of directions for player to traverse
            dead_end = list(moves) + [neighbors_keys[0]]
            return dead_end
        else:
            # Keep going through the graph until we hit a dead end
            for direction in neighbors:
                next_room = neighbors[direction]
                new_moves = moves + [direction]
                # If we haven't visited the next room add it to our BFS and Queue
                if next_room not in visited_bfs:
                    queue.enqueue([next_room, new_moves])
                    visited_bfs.add(next_room)
                if next_room not in visited:
                    return new_moves

dft()


traversal_path = []
visited = set()
visited.add(world.starting_room.id)
current_room_id = world.starting_room.id
num_rooms = len(graph.vertices)

# While visited rooms is less than the actual number of rooms
while len(visited) < num_rooms:
    # Find the nearest dead end
    moves = bfs(current_room_id, visited)

    # Traverse the returned list of moves
    for direction in moves:
        player.travel(direction)
        traversal_path.append(direction)
        visited.add(player.current_room.id)
    current_room_id = player.current_room.id

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

# Pass each move in and traverse the map
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
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")




# Hello,

# I offer excellent communication skills, and have the drive of a race horse. I believe I would be a great candidate for this position, because I simply love to learn, help and grow with others. The projects section of my resume highlights the hours of work I have put in, to build the skills I have. The skills section highlights the exact tools I've used during my learning process, which are aligned with your needs. 

# I'd welcome the opportunity to speak with someone from thus organization if you feel I'd be a strong candidate for this or other positions within your network.

# Thank you,

# Kevin Sims  
