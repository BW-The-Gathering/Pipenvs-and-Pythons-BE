# from tempmod import Room, Map
import math
import random
from adventure.make_world.makenames import makename
from adventure.models import Room,Map,Player
from django.contrib.auth.models import User # TODO: GET RID OF THIS!!!

def make_player_old():
    usr = User() # TODO: GET RID OF THIS!!!
    usr.save() # TODO: GET RID OF THIS!!!
    temp = Player(user_id=usr) # TODO: make this legit and not janky
    temp.save() 
    return temp

def make_player(user_id):
    player = Player(user_id=user_id)
    player.save()
    return player

def make_map(player_id): # TODO: How to get player id? 
    # make a map
    new_map = Map(player_id=player_id)
    new_map.save()
    return new_map

def make_rooms(new_map, genre):
    # make first room (0,0)
    entrance = Room(map_id=new_map, name='Entrance') ###TODO: change Room to have coordinates (maybe, also sorta done?)
    entrance.save()
    rooms = {(0,0): entrance}
    new_map.save()
    # create branches (recursion)
    entrance.north = make_room('south', new_map, coords=(0,1), rooms=rooms, recursion=0, prev_room=entrance, genre=genre)
    entrance.save()
    return rooms


def make_room(path_to_prev, map_id, coords, rooms, recursion, prev_room, genre='fantasy'):
    max_depth = 30
    if rooms.get(coords, None):
        # print(f"Dupe Detected: {coords}") <- Used for testing
        setattr(rooms[coords], "test", "Collision")
        setattr(rooms[coords], path_to_prev, prev_room.id) #<- fixes one-way doors
        rooms[coords].save()
        return rooms[coords].id
    # make current room
    curr_room = Room(map_id=map_id, name=makename(genre),) # description=None) # TODO: Did makename BREAK?
    curr_room.save()
    # attach_room(path_to_prev, prev_room, curr_room)
    rooms.update({coords: curr_room})
    if recursion >= 25: # temporary base-case
        setattr(curr_room, "test", "Max Depth")
        # attach_room(path_to_prev, prev_room, curr_room)
        setattr(curr_room, path_to_prev, prev_room.id) #<- fixes one-way doors
        curr_room.save()
        return curr_room.id
    
    # Use RNG to decide if a room will be made for each
    chance = 1 - (math.log(recursion) / math.log(max_depth))

    def rng(chance):
        random_num = random.random()

        if random_num <= chance:
            return make_room
        else:
            return None

    north_connect = rng(chance)
    if north_connect:
        curr_room.north = north_connect('south', map_id,(coords[0], coords[1] + 1), rooms, recursion + 1, curr_room)

    east_connect =  rng(chance)
    if east_connect:
        curr_room.east = east_connect('west', map_id,(coords[0] + 1, coords[1]), rooms, recursion + 1, curr_room)

    west_connect =  rng(chance)
    if west_connect:
        curr_room.west =west_connect('east', map_id,(coords[0] - 1, coords[1]), rooms, recursion + 1, curr_room)

    south_connect = rng(chance)
    if south_connect:
        curr_room.south = south_connect('north', map_id,(coords[0], coords[1] - 1), rooms, recursion + 1, curr_room)



    # north_connect = random.choice([make_room, None])
    # if north_connect:
    #     curr_room.north = north_connect('south', map_id,(coords[0], coords[1] + 1), rooms, recursion + 1, curr_room)
    #     curr_room.save()

    # east_connect =  random.choice([make_room, None])
    # if east_connect:
    #     curr_room.east = east_connect('west', map_id,(coords[0] + 1, coords[1]), rooms, recursion + 1, curr_room)
    #     curr_room.save()

    # west_connect =  random.choice([make_room, None])
    # if west_connect:
    #     curr_room.west =west_connect('east', map_id,(coords[0] - 1, coords[1]), rooms, recursion + 1, curr_room)
    #     curr_room.save()

    # south_connect = random.choice([make_room, None])
    # if south_connect:
    #     curr_room.south = south_connect('north', map_id,(coords[0], coords[1] - 1), rooms, recursion + 1, curr_room)
    #     curr_room.save()

    setattr(rooms[coords], "test", "Finally")
    # attach_room(path_to_prev, prev_room, curr_room)
    setattr(curr_room, path_to_prev, prev_room.id)
    curr_room.save()
    return curr_room.id
    
    

"""Debug Code"""

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

