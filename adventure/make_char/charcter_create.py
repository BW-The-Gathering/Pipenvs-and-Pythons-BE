from adventure.make_world.MakeRoom import make_player, make_player_old, make_map, make_rooms


def pc(user):
    """Generates a new player, map, and populates map with rooms. 
    Sets player's positions  
    
    Arguments:
        request  -- request packet
    
    Returns:
        Dict -- Returns User, Player, 
    """

    username = user.username
    player = make_player(user_id=request.user)
    new_map = make_map(player)
    rooms = make_rooms(new_map)
    player.position = rooms[(0,0)]

    return_packet = {
        "user": user,
        "player": player,
        "map_id": new_map, 
        "rooms": rooms
    }
    return return_packet