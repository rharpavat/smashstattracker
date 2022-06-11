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

class PlayerStatsTest(models.Model):
    playerid = models.CharField(max_length=20)
    collectiondate = models.DateField()
    totalkills = models.IntegerField()
    avgkills = models.DecimalField(max_digits=3, decimal_places=2)
    totaldeaths = models.IntegerField()
    avgdeaths = models.DecimalField(max_digits=3, decimal_places=2)
    totalsds = models.IntegerField()
    avgsds = models.DecimalField(max_digits=3, decimal_places=2)
    totalwins = models.IntegerField()
    kdratio = models.DecimalField(max_digits=3, decimal_places=2)
    avgrank = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        unique_together = (('playerid', 'collectiondate'),)

