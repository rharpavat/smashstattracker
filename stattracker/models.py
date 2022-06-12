from django.db import models

# Create your models here.

class MatchData(models.Model):
    matchid = models.IntegerField()
    playerid = models.CharField(max_length=20)
    fighter = models.CharField(max_length=20)
    playerrank = models.IntegerField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    selfdestructs = models.IntegerField()
    damagegiven = models.IntegerField(null=True)
    damagetaken = models.IntegerField(null=True)
    stagename = models.CharField(max_length=50, blank=True)
    matchdate = models.DateField()

    class Meta:
        unique_together = (('matchid', 'playerid'),)

class PlayerStats(models.Model):
    playerid = models.CharField(max_length=20)
    collectiondate = models.DateField()
    totalkills = models.IntegerField()
    avgkills = models.DecimalField(max_digits=3, decimal_places=2)
    totaldeaths = models.IntegerField()
    avgdeaths = models.DecimalField(max_digits=3, decimal_places=2)
    totalsds = models.IntegerField()
    avgsds = models.DecimalField(max_digits=3, decimal_places=2)
    totaldmggiven = models.IntegerField(null=True)
    avgdmggiven = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    totaldmgtaken = models.IntegerField(null=True)
    avgdmgtaken = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    totalwins = models.IntegerField()
    kdratio = models.DecimalField(max_digits=3, decimal_places=2)
    avgrank = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        unique_together = (('playerid', 'collectiondate'),)

class Leaderboard(models.Model):
    statistic = models.CharField(max_length=20, unique=True)
    playerid = models.CharField(max_length=20)
    value = models.DecimalField(max_digits=10, decimal_places=2)

