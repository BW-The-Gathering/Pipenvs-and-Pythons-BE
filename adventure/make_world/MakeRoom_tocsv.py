from tempmod import Room, Map
import random
from makenames import makename

def make_rooms(new_map, genre):
    # make first room (0,0)
    entrance = Room(map_id=new_map, id=0, name='Entrance', xcoord=0, ycoord=0) ###TODO: change Room to have coordinates (maybe, also sorta done?)
    # entrance.save()
    rooms = {(0,0): entrance}
    # new_map.save()
    # create branches (recursion)
    entrance.north = make_room('south', new_map, coords=(0,1), rooms=rooms, recursion=0, prev_room=entrance, genre=genre)
    # entrance.save()
    return rooms


def make_room(path_to_prev, map_id, coords, rooms, recursion, prev_room, genre='fantasy'):
    if rooms.get(coords, None):
        # print(f"Dupe Detected: {coords}") <- Used for testing
        setattr(rooms[coords], "test", "Collision")
        setattr(rooms[coords], path_to_prev, prev_room.id) #<- fixes one-way doors
        # rooms[coords].save()
        return rooms[coords].id
    # make current room
    curr_room = Room(map_id=map_id, id=random.random(), name=makename(genre),xcoord=coords[0], ycoord=coords[1]) # description=None) # TODO: Did makename BREAK?
    # curr_room.save()
    # attach_room(path_to_prev, prev_room, curr_room)
    rooms.update({coords: curr_room})
    if recursion >= 25: # temporary base-case
        setattr(curr_room, "test", "Max Depth")
        # attach_room(path_to_prev, prev_room, curr_room)
        setattr(curr_room, path_to_prev, prev_room.id) #<- fixes one-way doors
        # curr_room.save()
        return curr_room.id
    
    # Use RNG to decide if a room will be made for each

    north_connect = random.choice([make_room, None])
    if north_connect:
        curr_room.north = north_connect('south', map_id, (coords[0], coords[1] + 1), rooms, recursion + 1, curr_room)
        # curr_room.save()

    east_connect =  random.choice([make_room, None])
    if east_connect:
        curr_room.east = east_connect('west', map_id, (coords[0] + 1, coords[1]), rooms, recursion + 1, curr_room)
        # curr_room.save()

    west_connect =  random.choice([make_room, None])
    if west_connect:
        curr_room.west =west_connect('east', map_id, (coords[0] - 1, coords[1]), rooms, recursion + 1, curr_room)
        # curr_room.save()

    south_connect = random.choice([make_room, None])
    if south_connect:
        curr_room.south = south_connect('north', map_id,(coords[0], coords[1] - 1), rooms, recursion + 1, curr_room)
        # curr_room.save()

    setattr(rooms[coords], "test", "Finally")
    # attach_room(path_to_prev, prev_room, curr_room)
    setattr(curr_room, path_to_prev, prev_room.id)
    # curr_room.save()
    return curr_room.id
    
    

"""Debug Code"""

maps = make_rooms(1, genre="fantasy")
# # for key in maps.keys():
# #     print(maps[key].name)
# # print(maps[(0,1)].south.name)
# print(len(maps))

# # toex = [key for key in maps.keys()]

f = open('map.txt', 'w')
# for key in maps.keys():
#     f.write(str(key)+',')
# f.close()     
import csv
with open('test.csv', 'w') as f:
    for key in maps.keys():
        f.write("%s,%s,%s,%s,%s,%s,%s,%s\n"%(maps[key].id,maps[key].name,maps[key].xcoord,maps[key].ycoord,maps[key].north,maps[key].east,maps[key].west,maps[key].south))
# ### TODO: link new room to old room. 
# ### TODO: mess with shape/recursion RNG
# # python MakeRoom.py
columns=['id', 'name', 'x', 'y', 'north', 'east', 'west', 'south']
