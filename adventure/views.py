from django.shortcuts import render
from adventure.make_world.MakeRoom import make_player, make_map, makename

# Create your views here.
def test(request):
    player = make_player()
    rooms = make_map(player)
    # rooms = makename()
    context = {
        'testrun': rooms
    }
    return render(request, 'map-test.html', context)