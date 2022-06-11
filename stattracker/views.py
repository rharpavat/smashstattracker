from django.contrib import messages
from django.db.models import Sum, Avg, Count, Max
from django.http import HttpResponse
from django.shortcuts import redirect, render

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

    stat_objects = []

    for name in pnames:

        totalkills = get_total_kills(name)
        totaldeaths = get_total_deaths(name)

        stat_obj = PlayerStatsTest(
            playerid = name,
            collectiondate = get_latest_played_date(name),
            totalkills = totalkills,
            avgkills = get_avg_kills(name),
            totaldeaths = totaldeaths,
            avgdeaths = get_avg_deaths(name),
            totalsds = get_total_sds(name),
            avgsds = get_avg_sds(name),
            totaldmggiven = get_total_dmggiven(name),
            avgdmggiven = get_avg_dmggiven(name),
            totaldmgtaken = get_total_dmgtaken(name),
            avgdmgtaken = get_avg_dmgtaken(name),
            totalwins = get_total_wins(name),
            kdratio = round((totalkills / totaldeaths), 2),
            avgrank = get_avg_rank(name)
        )

        stat_objects.append(stat_obj)

        # pinfo = {}
        # pinfo['name'] = name
        # totalkills = get_total_kills(name)
        # pinfo['totalkills'] = totalkills
        # pinfo['avgkills'] = get_avg_kills(name)
        # totaldeaths = get_total_deaths(name)
        # pinfo['totaldeaths'] = totaldeaths
        # pinfo['avgdeaths'] = get_avg_deaths(name)
        # pinfo['totalsds'] = get_total_sds(name)
        # pinfo['avgsds'] = get_avg_sds(name)
        # pinfo['totaldmggiven'] = get_total_dmggiven(name)
        # pinfo['avgdmggiven'] = get_avg_dmggiven(name)
        # pinfo['totaldmgtaken'] = get_total_dmgtaken(name)
        # pinfo['avgdmgtaken'] = get_avg_dmgtaken(name)
        # pinfo['totalwins'] = get_total_wins(name)
        # pinfo['kdratio'] = round((totalkills / totaldeaths), 2)
        # pinfo['avgrank'] = get_avg_rank(name)
        # pinfo['lastplayeddate'] = get_latest_played_date(name)
        # context['playerinfo'].append(pinfo)

    PlayerStatsTest.objects.bulk_create(stat_objects, ignore_conflicts=True)

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
            damagegiven = None if (item[7] == 'NULL') else item[7],
            damagetaken = None if (item[8] == 'NULL') else item[8],
            stagename = item[9],
            matchdate = item[10],
        )
        for item in consolidatedData
    ]

    MatchDataTest.objects.bulk_create(convertedData, ignore_conflicts=True, batch_size=100)

    return redirect('index')

def get_unique_player_names():
    records = MatchDataTest.objects.values('playerid').distinct()
    namelist = [item['playerid'] for item in records]
    return namelist

def get_total_kills(playerid):
    records = MatchDataTest.objects.filter(playerid=playerid).values('kills')
    info = records.aggregate(Sum('kills'))
    return info['kills__sum']

def get_avg_kills(playerid):
    records = MatchDataTest.objects.filter(playerid=playerid).values('kills')
    info = records.aggregate(Avg('kills'))
    return info['kills__avg']

def get_total_deaths(playerid):
    records = MatchDataTest.objects.filter(playerid=playerid).values('deaths')
    info = records.aggregate(Sum('deaths'))
    return info['deaths__sum']

def get_avg_deaths(playerid):
    records = MatchDataTest.objects.filter(playerid=playerid).values('deaths')
    info = records.aggregate(Avg('deaths'))
    return info['deaths__avg']

def get_total_sds(playerid):
    records = MatchDataTest.objects.filter(playerid=playerid).values('selfdestructs')
    info = records.aggregate(Sum('selfdestructs'))
    return info['selfdestructs__sum']

def get_avg_sds(playerid):
    records = MatchDataTest.objects.filter(playerid=playerid).values('selfdestructs')
    info = records.aggregate(Avg('selfdestructs'))
    return info['selfdestructs__avg']

def get_total_wins(playerid):
    records = MatchDataTest.objects.filter(playerid=playerid, playerrank=1).values('playerrank')
    info = records.aggregate(Count('playerrank'))
    return info['playerrank__count']

def get_avg_rank(playerid):
    records = MatchDataTest.objects.filter(playerid=playerid).values('playerrank')
    info = records.aggregate(Avg('playerrank'))
    return info['playerrank__avg']

def get_total_dmggiven(playerid):
    records = MatchDataTest.objects.filter(playerid=playerid).values('damagegiven').exclude(damagegiven__isnull=True)
    info = records.aggregate(Sum('damagegiven'))
    return info['damagegiven__sum']

def get_avg_dmggiven(playerid):
    records = MatchDataTest.objects.filter(playerid=playerid).values('damagegiven').exclude(damagegiven__isnull=True)
    info = records.aggregate(Avg('damagegiven'))
    return info['damagegiven__avg']

def get_total_dmgtaken(playerid):
    records = MatchDataTest.objects.filter(playerid=playerid).values('damagetaken').exclude(damagetaken__isnull=True)
    info = records.aggregate(Sum('damagetaken'))
    return info['damagetaken__sum']

def get_avg_dmgtaken(playerid):
    records = MatchDataTest.objects.filter(playerid=playerid).values('damagetaken').exclude(damagetaken__isnull=True)
    info = records.aggregate(Avg('damagetaken'))
    return info['damagetaken__avg']

def get_latest_played_date(playerid):
    records = MatchDataTest.objects.filter(playerid=playerid).values('matchdate').distinct()
    info = records.aggregate(Max('matchdate'))
    return info['matchdate__max']
