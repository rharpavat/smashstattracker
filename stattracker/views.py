from django.contrib import messages
from django.db.models import Sum
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

from .models import MatchDataTest
from .models import PlayerStatsTest

# Create your views here.
def index(request):
    return render(request, "index.html")

def run_analytics(request):
    context = {
        "playerinfo": []
    }

    pnames = get_unique_player_names()

    for name in pnames:
        pinfo = {}
        pinfo['name'] = name
        pinfo['totalkills'] = get_total_kills(name)
        pinfo['avgkills'] = get_avg_kills(name)
        context['playerinfo'].append(pinfo)

    return render(request, "testdatadisplayer.html", context)

def importdata(request):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    apikey = json.loads(os.environ.get('GOOGLE_API_KEY_FILE'))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(apikey,scope)
    client = gspread.authorize(creds)

    sheet = client.open("SmashStats").worksheet("StatTest")
    data = sheet.get_values()

    trimmedData = data[1:]
    consolidatedData = [item[:7] + item[13:] for item in trimmedData]
    convertedData = [
        MatchDataTest(
            matchid = item[0],
            playerid = item[1],
            fighter = item[2],
            playerrank = item[3],
            kills = item[4],
            deaths = item[5],
            selfdestructs = item[6],
            damagegiven = item[7],
            damagetaken = item[8],
            stagename = item[9],
            matchdate = item[10],
        )
        for item in consolidatedData
    ]

    MatchDataTest.objects.bulk_create(convertedData, ignore_conflicts=True, batch_size=100)

    return redirect('index')

# playerid = models.CharField(max_length=20)
# collectiondate = models.DateField()
# totalkills = models.IntegerField()
# avgkills = models.DecimalField(max_digits=3, decimal_places=2)
# totaldeaths = models.IntegerField()
# avgdeaths = models.DecimalField(max_digits=3, decimal_places=2)
# totalsds = models.IntegerField()
# avgsds = models.DecimalField(max_digits=3, decimal_places=2)
# totalwins = models.IntegerField()
# kdratio = models.DecimalField(max_digits=3, decimal_places=2)
# avgrank = models.DecimalField(max_digits=3, decimal_places=2)

def get_unique_player_names():
    records = MatchDataTest.objects.values('playerid').distinct()
    namelist = [item['playerid'] for item in records]
    return namelist

def get_total_kills(playerid):
    records = MatchDataTest.objects.filter(playerid=playerid).values('kills')
    sum_info = records.aggregate(Sum('kills'))
    return sum_info['kills__sum']

def get_avg_kills(playerid):
    records = MatchDataTest.objects.filter(playerid=playerid).values('kills')
    sum_info = records.aggregate(Avg('kills'))
    return sum_info['kills__avg']