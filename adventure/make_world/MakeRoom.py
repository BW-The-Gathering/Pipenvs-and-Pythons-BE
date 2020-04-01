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
    new_map.save()
    # make first room (0,0)
    entrance = Room(map_id=new_map, name='Entrance') ###TODO: change Room to have coordinates (maybe, also sorta done?)
    entrance.save()
    rooms = {(0,0): entrance}
    new_map.save()
    # create branches (recursion)
    entrance.north = make_room('south', new_map, coords=(0,1), rooms=rooms, recursion=0, prev_room=entrance, genre=genre)
    entrance.save()
    # entrance.north = make_room(new_map, (0,0), (0,1), rooms, 0,)
    # for key in rooms.keys():
    #     rooms[key].save()
    return rooms
    

# def attach_room(previous, current, prev_coords, current_coords):
#     #prev -> current is north
#     if prev_coords[1] == current_coords[1] - 1:
#         setattr(previous, 'north', current.id)
#         setattr(current, 'south', previous.id)
#     #prev -> current is south
#     if prev_coords[1] == current_coords[1] + 1:
#         setattr(previous, 'south', current.id)
#         setattr(current, 'north', previous.id)
#     #prev -> current is east
#     if prev_coords[0] == current_coords[0] - 1:
#         setattr(previous, 'east', current.id)
#         setattr(current, 'west', previous.id)
#     #prev -> current is west
#     if prev_coords[0] == current_coords[0] + 1:
#         setattr(previous, 'west', current.id)
#         setattr(current, 'east', previous.id)
#     current.save()
#     previous.save()


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

    north_connect = random.choice([make_room, None])
    if north_connect:
        curr_room.north = north_connect('south', map_id,(coords[0], coords[1] + 1), rooms, recursion + 1, curr_room)
        curr_room.save()

    east_connect =  random.choice([make_room, None])
    if east_connect:
        curr_room.east = east_connect('west', map_id,(coords[0] + 1, coords[1]), rooms, recursion + 1, curr_room)
        curr_room.save()

    west_connect =  random.choice([make_room, None])
    if west_connect:
        curr_room.west =west_connect('east', map_id,(coords[0] - 1, coords[1]), rooms, recursion + 1, curr_room)
        curr_room.save()

    south_connect = random.choice([make_room, None])
    if south_connect:
        curr_room.south = south_connect('north', map_id,(coords[0], coords[1] - 1), rooms, recursion + 1, curr_room)
        curr_room.save()

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