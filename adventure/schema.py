import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import Player, Map, Room

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
    
    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

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

class Mutation(graphene.ObjectType):
    player_mutation = PlayerMutation.Field()
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)