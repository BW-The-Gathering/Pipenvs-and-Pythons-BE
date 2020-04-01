import graphene
from graphene_django.types import DjangoObjectType
from .models import Player, Map, Room


class PlayerType(DjangoObjectType):
    class Meta:
        model = Player

class PlayerMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        position = graphene.Int()
        health = graphene.Int()
        mana = graphene.Int()
        stamina = graphene.Int()

    player = graphene.Field(PlayerType)

    def mutate(self, info, id, position=None, health=None, mana=None, stamina=None):
        player = Player.objects.get(pk=id)
        if position is not None:
            room = Room.objects.get(pk=position)
            player.position = room
        if health is not None:
            player.health = health
        if mana is not None:
            player.mana = mana
        if stamina is not None:
            player.stamina = stamina
        player.save()

        return PlayerMutation(player=player)


class MapType(DjangoObjectType):
    class Meta:
        model = Map

class RoomType(DjangoObjectType):
    class Meta:
        model = Room

class Query(graphene.ObjectType):
    # Get ALL
    all_players = graphene.List(PlayerType)
    all_maps = graphene.List(MapType)
    all_rooms = graphene.List(RoomType)


    def resolve_all_players(self, info, **kwargs):
        print(type(Player.objects.all()))
        return Player.objects.all()

    def resolve_all_maps(self, info, **kwargs):
        return Map.objects.all()
        
    def resolve_all_rooms(self, info, **kwargs):
        return Room.objects.all()

    # Get Single
    player = graphene.Field(PlayerType, id=graphene.Int())
    map = graphene.Field(MapType, id=graphene.Int())
    room = graphene.Field(RoomType, id=graphene.Int())

    def resolve_player(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Player.objects.get(pk=id)
        
        return None

    def resolve_map(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Map.objects.get(pk=id)
        
        return None

    def resolve_room(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Room.objects.get(pk=id)
        
        return None

    adjacent_rooms = graphene.List(RoomType, id=graphene.Int())

    def resolve_adjacent_rooms(self, info, **kwargs):
        id = kwargs.get('id')

        current_room = Room.objects.get(pk=id)
        
        directions = []

        if current_room.north is not None:
            directions.append(current_room.north)
        if current_room.south is not None:
            directions.append(current_room.south)
        if current_room.east is not None:
            directions.append(current_room.east)
        if current_room.west is not None:
            directions.append(current_room.west)

        return Room.objects.filter(pk__in=directions)

class Mutation(graphene.ObjectType):
    player_mutation = PlayerMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)