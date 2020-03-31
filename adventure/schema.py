import graphene
from graphene_django.types import DjangoObjectType
from .models import Player, Map, Room

from graphene_django.filter import DjangoFilterConnectionField

class PlayerType(DjangoObjectType):
    class Meta:
        model = Player
        interfaces = (graphene.relay.Node,)
        filter_fields = ['id']

class MapType(DjangoObjectType):
    class Meta:
        model = Map
        interfaces = (graphene.relay.Node,)
        filter_fields = ['id', 'player_id']

class RoomType(DjangoObjectType):
    class Meta:
        model = Room
        interfaces = (graphene.relay.Node,)
        filter_fields = ['id', 'map_id']

class Query(graphene.ObjectType):
    players = DjangoFilterConnectionField(PlayerType)
    rooms = DjangoFilterConnectionField(RoomType)
    maps = DjangoFilterConnectionField(MapType)

schema = graphene.Schema(query=Query)