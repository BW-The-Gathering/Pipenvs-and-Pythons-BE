import graphene
import graphql_jwt
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
        user = info.context.user
        if user.is_anonymous:
            return Exception('Not Logged In!')

        player = Player.objects.get(pk=id)

        if user.id is not player.user_id.id:
            return Exception('This is not your player!')

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
        user = info.context.user
        if user.is_anonymous:
            return Exception('Not Logged In!')

        return Player.objects.filter(user_id=user)


    def resolve_all_maps(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            return Exception('Not Logged In!')

        return Map.objects.all()
        
    def resolve_all_rooms(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            return Exception('Not Logged In!')

        return Room.objects.all()

    # Get Single
    player = graphene.Field(PlayerType, id=graphene.Int())
    map = graphene.Field(MapType, id=graphene.Int())
    room = graphene.Field(RoomType, id=graphene.Int())

    def resolve_player(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            return Exception('Not Logged In!')

        id = kwargs.get('id')

        if id is not None:
            player =  Player.objects.get(pk=id)
            if user.id is not player.user_id.id:
                return Exception('This is not your player!')

            return player
        
        return None

    def resolve_map(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            return Exception('Not Logged In!')
        id = kwargs.get('id')

        if id is not None:
            map = Map.objects.get(pk=id)
            if user.id is not map.player_id.user_id.id:
                return Exception('This is not your map!')
            return map

        return None

    def resolve_room(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            return Exception('Not Logged In!')
        id = kwargs.get('id')

        if id is not None:
            room = Room.objects.get(pk=id)
            if user.id is not room.map_id.player_id.user_id.id:
                return Exception('This is not your room!')
            
            return room
        
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
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    player_mutation = PlayerMutation.Field()
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)