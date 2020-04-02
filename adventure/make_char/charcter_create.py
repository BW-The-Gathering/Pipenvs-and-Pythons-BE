from adventure.make_world.MakeRoom import make_player, make_player_old, make_map, make_rooms

from adventure.models import Room

def game_start(user):
    """Generates a new player, map, and populates map with rooms. 
    Sets player's positions  
    
    Arguments:
        request  -- request packet
    
    Returns:
        Dict -- Returns Player, new_map, and rooms in map
    """

    username = user.username
    player = make_player(user_id=user)
    new_map = make_map(player)
    rooms = make_rooms(new_map, genre="fantasy")
    player.position = rooms[(0,0)]
    player.save()

    # new content
    room_count = len(Room.objects.filter(map_id=new_map.id))
    last_room = Room.objects.filter(map_id=new_map.id).order_by('id')[room_count-1]
    # FOR PRODUCTION: ^ this line puts the end at the last room created
    # last_room = Room.objects.filter(map_id=new_map.id).order_by('id')[1]
    # FOR TESTING: ^ this line puts the end at the second room of the map (north of entrance)
    last_room.end = True
    last_room.save()

    return_packet = {
        "player": player,
        "map_id": new_map, 
        "rooms": rooms
    }
    return player