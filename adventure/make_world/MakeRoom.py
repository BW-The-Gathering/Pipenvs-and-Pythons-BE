# from tempmod import Room, Map
import random
from adventure.make_world.makenames import makename
from adventure.models import Room,Map,Player
from django.contrib.auth.models import User # TODO: GET RID OF THIS!!!

def make_player():
    usr = User() # TODO: GET RID OF THIS!!!
    usr.save() # TODO: GET RID OF THIS!!!
    temp = Player(user_id=usr) # TODO: make this legit and not janky
    temp.save() 
    return temp

def make_map(player_id, genre='fantasy'): # TODO: How to get player id? 
    # make a map
    new_map = Map(player_id=player_id)
    # make first room (0,0)
    entrance = Room(map_id=new_map, name='Entrance') ###TODO: change Room to have coordinates (maybe, also sorta done?)
    rooms = {(0,0): entrance}
    new_map.save()
    entrance.save()
    # create branches (recursion)
    entrance.north = make_room('south', new_map, coords=(0,1), rooms=rooms, recursion=0, prev_room=entrance, genre=genre)
    return rooms
    

# def attach_room(direction, previous, current):
#     if direction == 'north':
#         current.north = previous
#     if direction == 'south':
#         current.south = previous
#     if direction == 'east':
#         current.east = previous
#     if direction == 'west':
#         current.west = previous

    
"""Changes made below: Pass Map(new_map) Object as map_id"""
def make_room(direction, map_id, coords, rooms, recursion, prev_room, genre='scifi'):
    recursion = recursion
    if rooms.get(coords, None):
        # print(f"Dupe Detected: {coords}") <- Used for testing
        # setattr(curr_room, direction, prev_room) <- fixes one-way doors

        return #rooms[coords]
    # make current room
    curr_room = Room(map_id=map_id, name=makename(genre),) # description=None)
    # attach_room(direction, prev_room, curr_room)
    rooms.update({coords: curr_room})
    if recursion == 25: # temporary base-case
        return #curr_room
    # Use RNG to decide if a room will be made for each
    curr_room.north = random.choice([make_room('south', map_id,(coords[0], coords[1] + 1), rooms, recursion + 1, curr_room), None])
    curr_room.east = random.choice([make_room('west', map_id,(coords[0] + 1, coords[1]), rooms, recursion + 1, curr_room), None])
    curr_room.west = random.choice([make_room('east', map_id,(coords[0] - 1, coords[1]), rooms, recursion + 1, curr_room), None])
    curr_room.south = random.choice([make_room('north', map_id,(coords[0], coords[1] - 1), rooms, recursion + 1, curr_room), None])
    curr_room.save()
    setattr(curr_room, direction, prev_room)
    return #curr_room
    
    

# maps = make_map(1)
# # for key in maps.keys():
# #     print(maps[key].name)
# # print(maps[(0,1)].south.name)
# print(len(maps))

# # toex = [key for key in maps.keys()]

# f = open('map.txt', 'w')
# for key in maps.keys():
#     f.write(str(key)+',')
# f.close()     
# ### TODO: link new room to old room. 
# ### TODO: mess with shape/recursion RNG
# # python MakeRoom.py