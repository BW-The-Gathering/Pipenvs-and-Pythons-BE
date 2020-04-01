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
    # entrance.north = make_room(new_map, (0,0), (0,1), rooms, 0,)
    return rooms
    

def attach_room(previous, current, prev_coords, current_coords):
    #prev -> current is north
    if prev_coords[1] == current_coords[1] - 1:
        setattr(previous, 'north', current.id)
        setattr(current, 'south', previous.id)
    #prev -> current is south
    if prev_coords[1] == current_coords[1] + 1:
        setattr(previous, 'south', current.id)
        setattr(current, 'north', previous.id)
    #prev -> current is east
    if prev_coords[0] == current_coords[0] - 1:
        setattr(previous, 'east', current.id)
        setattr(current, 'west', previous.id)
    #prev -> current is west
    if prev_coords[0] == current_coords[0] + 1:
        setattr(previous, 'west', current.id)
        setattr(current, 'east', previous.id)
    current.save()
    previous.save()


# def make_room(map_id, prev_coords, current_coords, rooms, recurse_depth, genre='fantasy'):
#     """
#         basecase 1: colission
#         basecase 2: recursion

#         shoot north -> max depth
#         returncurrent room.id
#     """
#     current_room = Room(map_id=map_id, name=makename(genre),)
#     rooms.update({current_coords: current_room})
#     attach_room(rooms[prev_coords], rooms[current_room], prev_coords, current_coords)
#     if recurse_depth == 5:
#         return current_room
#     recurse_depth += 1
#     current_room.north = make_room()



def make_room(path_to_prev, map_id, coords, rooms, recursion, prev_room, genre='fantasy'):
    if rooms.get(coords, None):
        # print(f"Dupe Detected: {coords}") <- Used for testing
        setattr(rooms[coords], "test", "Collision")
        setattr(rooms[coords], path_to_prev, prev_room.id) #<- fixes one-way doors
        # attach_room(path_to_prev, prev_room, rooms[coords])
        rooms[coords].save()
        return rooms[coords].id
    # make current room
    curr_room = Room(map_id=map_id, name=makename(genre),) # description=None) # TODO: Did makename BREAK?
    # attach_room(path_to_prev, prev_room, curr_room)
    rooms.update({coords: curr_room})
    if recursion >= 25: # temporary base-case
        setattr(rooms[coords], "test", "Max Depth")
        # attach_room(path_to_prev, prev_room, curr_room)
        setattr(rooms[coords], path_to_prev, prev_room.id) #<- fixes one-way doors
        curr_room.save()
        return curr_room.id
    # Use RNG to decide if a room will be made for each
    # curr_room.north = make_room('south', map_id,(coords[0], coords[1] + 1), rooms, recursion + 1, curr_room)  
    curr_room.north = random.choice([make_room('south', map_id,(coords[0], coords[1] + 1), rooms, recursion + 1, curr_room), None])
    # curr_room.east = make_room('west', map_id,(coords[0] + 1, coords[1]), rooms, recursion + 1, curr_room)
    curr_room.east =  random.choice([make_room('west', map_id,(coords[0] + 1, coords[1]), rooms, recursion + 1, curr_room), None])
    # curr_room.west = make_room('east', map_id,(coords[0] - 1, coords[1]), rooms, recursion + 1, curr_room) 
    curr_room.west =  random.choice([make_room('east', map_id,(coords[0] - 1, coords[1]), rooms, recursion + 1, curr_room), None])
    # curr_room.south = make_room('north', map_id,(coords[0], coords[1] - 1), rooms, recursion + 1, curr_room)
    curr_room.south = random.choice([make_room('north', map_id,(coords[0], coords[1] - 1), rooms, recursion + 1, curr_room), None])
    setattr(rooms[coords], "test", "Finally")
    # attach_room(path_to_prev, prev_room, curr_room)
    setattr(curr_room, path_to_prev, prev_room.id)
    curr_room.save()
    return curr_room.id
    
    

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