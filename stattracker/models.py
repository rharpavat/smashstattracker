from django.db import models

# Create your models here.

class MatchDataTest(models.Model):
    matchid = models.IntegerField()
    playerid = models.CharField(max_length=20)
    fighter = models.CharField(max_length=20)
    playerrank = models.IntegerField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    selfdestructs = models.IntegerField()
    damagegiven = models.IntegerField()
    damagetaken = models.IntegerField()
    stagename = models.CharField(max_length=50)
    matchdate = models.DateField()

    class Meta:
        unique_together = (('matchid', 'playerid'),)

