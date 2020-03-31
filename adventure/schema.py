import graphene
from graphene_django.types import DjangoObjectType
from .models import Player, Map, Room

class PlayerType(DjangoObjectType):
    class Meta:
        model = Player

class MapType(DjangoObjectType):
    class Meta:
        model = Map

class RoomType(DjangoObjectType):
    class Meta:
        model = Room

class Query(graphene.ObjectType):
    all_players = graphene.List(PlayerType)
    all_maps = graphene.List(MapType)
    all_rooms = graphene.List(RoomType)

    def resolve_all_players(self, info, **kwargs):
        return Player.objects.all()

    def resolve_all_maps(self, info, **kwargs):
        return Map.objects.all()

    def resolve_all_rooms(self, info, **kwargs):
        return Room.objects.all()    

schema = graphene.Schema(query=Query)