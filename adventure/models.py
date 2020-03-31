from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Player(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.ForeignKey('Room', on_delete=models.CASCADE, null=True, blank=True)
    health = models.IntegerField(default=100)
    mana = models.IntegerField(default=100)
    stamina = models.IntegerField(default=100)


class Map(models.Model):
    id = models.AutoField(primary_key=True)
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    map_id = models.ForeignKey(Map, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    north = models.IntegerField(blank=True,null=True)
    south = models.IntegerField(blank=True,null=True)
    east = models.IntegerField(blank=True,null=True)
    west = models.IntegerField(blank=True,null=True)