from django.shortcuts import render
from adventure.make_world.MakeRoom import make_player, make_player_old, make_map, make_rooms
from adventure.schema import PlayerMutation
import graphene


# Create your views here.
def test(request):
    player = make_player_old()
    new_map = make_map(player)
    rooms = make_rooms(new_map, genre='fantasy')
    context = {
        'testrun': rooms
    }
    return render(request, 'map-test.html', context)

def home(request):
    return render(request, 'homepage.html')


def pct(request):
    """Gets user id from request, take an direction (input)
    move player by updating player.location (graphQL)
    
   """

    username = request.user.username
    player = make_player(user_id=request.user)
    new_map = make_map(player)
    rooms = make_rooms(new_map, genre="fantasy")
    context = {

        'name': username,
        'playername': player.id,
        'testrun': rooms
        }
    return render(request, 'playercreationtest.html', context)

def draw_map(request):
    pass