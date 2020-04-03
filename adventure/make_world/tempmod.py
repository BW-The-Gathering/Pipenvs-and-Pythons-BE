import random
# Create your models here.
# 


class Map():
    def __init__(self, id=1, player_id=1):
        self.id = id 
        self.player_id = player_id


class Room:
    def __init__(self, map_id, id, name,xcoord=None, ycoord=None, description=None):
        self.description = description
        self.map_id = map_id
        self.name = name
        self.id = id
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.north = None
        self.east = None
        self.west = None
        self.south = None