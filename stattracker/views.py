from django.contrib import messages
from django.db.models import Sum, Avg, Count, Max
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials
from collections import defaultdict

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from chart.PieChart import PieChart
from chart.LineChart import LineChart

from .models import MatchData, PlayerStats

# ================================
# VIEW FUNCTIONS
# ================================
def index(request):
    return render(request, "index.html")

def get_total_kills_chart(request):
    return get_stat_chart_over_time('totalkills')

def get_avg_kills_chart(request):
    return get_stat_chart_over_time('avgkills')

def get_total_deaths_chart(request):
    return get_stat_chart_over_time('totaldeaths')

def get_avg_deaths_chart(request):
    return get_stat_chart_over_time('avgdeaths')

def get_total_sds_chart(request):
    return get_stat_chart_over_time('totalsds')

def get_avg_sds_chart(request):
    return get_stat_chart_over_time('avgsds')

def get_total_wins_chart(request):
    return get_stat_chart_over_time('totalwins')

def get_latest_total_wins_chart(request):
    return get_total_stat_chart('totalwins')

def get_avg_rank_chart(request):
    return get_stat_chart_over_time('avgrank')

def view_graphs(request):
    context = {}
    # win_info = get_aggregated_total_wins()

    # unique_players = get_unique_player_names()

    # NewChart = PieChart(list(win_info.values()), list(win_info.keys()))
    # NewChart.data.label = "My Favourite Numbers"      # can change data after creation

    # kill_info = get_aggregated_avg_kills()
    
    # # playerlist = kill_info.keys()
    # datelist = [item[1] for item in kill_info.keys()]
    # uniquedates = []
    # for date in datelist:
    #     if date not in uniquedates:
    #         uniquedates.append(date)
    
    # sorteddates = sorted(uniquedates)

    # ChartJSON = NewChart.get()

    # context["chartJSON"] = ChartJSON
    # context["killChartJSON"] = lchart.get()
    # # context["otherdata"] = list(datasets.values())
    # context["otherdata2"] = kill_info
    # context["data"] = list(datasets.values())
    # context["labels"] = sorteddates


    return render(request=request,
                  template_name='graphs.html',
                  context=context)
    # return render(request, "graphs.html")

def run_analytics(request):
    context = {
        "playerinfo": []
    }

    pnames = get_unique_player_names()

    stat_objects = []

    for name in pnames:

        totalkills = get_total_kills(name)
        totaldeaths = get_total_deaths(name)

        stat_obj = PlayerStats(
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

    try:
        PlayerStats.objects.bulk_create(stat_objects, ignore_conflicts=True)
    except IntegrityError:
        for obj in stat_objects:
            try:
                obj.save()
            except IntegrityError:
                continue

    return render(request, "testdatadisplayer.html", context)

def importdata(request):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    apikey = json.loads(os.environ.get('GOOGLE_API_KEY_FILE'))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(apikey,scope)
    client = gspread.authorize(creds)

    sheet = client.open("SmashStats").worksheet("StatSheet")
    data = sheet.get_values()

    trimmedData = data[1:]
    consolidatedData = [item[:7] + item[13:] for item in trimmedData]
    convertedData = [
        MatchData(
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

    MatchData.objects.bulk_create(convertedData, ignore_conflicts=True, batch_size=100)

    return redirect('index')

def get_unique_player_names():
    records = MatchData.objects.values('playerid').distinct()
    namelist = [item['playerid'] for item in records]
    return namelist

def get_total_kills(playerid):
    records = MatchData.objects.filter(playerid=playerid).values('kills')
    info = records.aggregate(Sum('kills'))
    return info['kills__sum']

def get_avg_kills(playerid):
    records = MatchData.objects.filter(playerid=playerid).values('kills')
    info = records.aggregate(Avg('kills'))
    return info['kills__avg']

def get_total_deaths(playerid):
    records = MatchData.objects.filter(playerid=playerid).values('deaths')
    info = records.aggregate(Sum('deaths'))
    return info['deaths__sum']

def get_avg_deaths(playerid):
    records = MatchData.objects.filter(playerid=playerid).values('deaths')
    info = records.aggregate(Avg('deaths'))
    return info['deaths__avg']

def get_total_sds(playerid):
    records = MatchData.objects.filter(playerid=playerid).values('selfdestructs')
    info = records.aggregate(Sum('selfdestructs'))
    return info['selfdestructs__sum']

def get_avg_sds(playerid):
    records = MatchData.objects.filter(playerid=playerid).values('selfdestructs')
    info = records.aggregate(Avg('selfdestructs'))
    return info['selfdestructs__avg']

def get_total_wins(playerid):
    records = MatchData.objects.filter(playerid=playerid, playerrank=1).values('playerrank')
    info = records.aggregate(Count('playerrank'))
    return info['playerrank__count']

def get_avg_rank(playerid):
    records = MatchData.objects.filter(playerid=playerid).values('playerrank')
    info = records.aggregate(Avg('playerrank'))
    return info['playerrank__avg']

def get_total_dmggiven(playerid):
    records = MatchData.objects.filter(playerid=playerid).values('damagegiven').exclude(damagegiven__isnull=True)
    info = records.aggregate(Sum('damagegiven'))
    return info['damagegiven__sum']

def get_avg_dmggiven(playerid):
    records = MatchData.objects.filter(playerid=playerid).values('damagegiven').exclude(damagegiven__isnull=True)
    info = records.aggregate(Avg('damagegiven'))
    return info['damagegiven__avg']

def get_total_dmgtaken(playerid):
    records = MatchData.objects.filter(playerid=playerid).values('damagetaken').exclude(damagetaken__isnull=True)
    info = records.aggregate(Sum('damagetaken'))
    return info['damagetaken__sum']

def get_avg_dmgtaken(playerid):
    records = MatchData.objects.filter(playerid=playerid).values('damagetaken').exclude(damagetaken__isnull=True)
    info = records.aggregate(Avg('damagetaken'))
    return info['damagetaken__avg']

def get_latest_played_date(playerid):
    records = MatchData.objects.filter(playerid=playerid).values('matchdate').distinct()
    info = records.aggregate(Max('matchdate'))
    return info['matchdate__max']

# ================================
# PLAYERSTATS QUERY UTIL FUNCTIONS
# ================================

int_stats = ['totalkills', 'totaldeaths', 'totalsds', 'totaldmggiven', 'totaldmgtaken', 'totalwins']
float_stats = ['avgkills', 'avgdeaths', 'avgsds', 'avgdmggiven', 'avgdmgtaken', 'kdratio', 'avgrank']
colors = ["#ea5545", "#ffa600", "#87bc45", "#27aeef", "#b33dc6"]
bgcolors = ["rgba(234,85,69,0.5)", "rgba(255,166,0,0.5)", "rgba(135,188,69,0.5)", "rgba(39,174,239,0.5)", "rgba(179,61,198,0.5)"]

# -------- GENERIC STAT UTIL FUNCTIONS --------

def get_stat_chart_over_time(stat):
    unique_players = get_unique_player_names()
    info = get_aggregated_stat(stat)

    datelist = [item[1] for item in info.keys()]
    uniquedates = []
    for date in datelist:
        if date not in uniquedates:
            uniquedates.append(date)

    sorteddates = sorted(uniquedates)

    datasets = {
        name : {
            'label': name,
            'data': [],
            'fill': False,
        }
        for name in unique_players
    }

    ctr = 0
    for key, value in datasets.items():
        datasets[key]['borderColor'] = colors[ctr]
        datasets[key]['backgroundColor'] = bgcolors[ctr]
        ctr += 1

    for key, value in sorted(info.items()):
        datasets[key[0]]['data'].append(value)

    findata = list(datasets.values())

    return JsonResponse(data={
        'labels': uniquedates,
        'data': findata
    })

def get_aggregated_stat(statname):
    records = PlayerStats.objects.values('playerid', 'collectiondate', statname)

    transformed = defaultdict(dict)
    for record in records:
        name = record['playerid']
        date = str(record['collectiondate'])
        value = record[statname]
        transformed[(name, date)] = parse_stat_value(statname, value)

    return transformed

def get_total_stat_chart(stat):
    infodict = {}

    players = get_unique_player_names()
    for player in players:
        count = get_latest_total_stat_for_player(stat, player)
        infodict[player] = count

    dataset = [
        {
            'data': list(infodict.values()),
            'backgroundColor': colors,
            'hoverOffset': 4
        }
    ]

    return JsonResponse(data={
        'labels': list(infodict.keys()),
        'data': dataset
    })

def get_latest_total_stat_for_player(statname, playerid):
    latest_date_played = get_latest_played_date(playerid)
    records = PlayerStats.objects.filter(playerid=playerid, collectiondate=latest_date_played).values(statname)
    return records[0][statname]

def parse_stat_value(statname, value): #TODO: Add exception case if the value doesn't fall under either category
    if statname in int_stats:
        return int(value)

    if statname in float_stats:
        return float(value)

# -------- INDIVIDUAL STAT UTIL FUNCTIONS --------
def get_aggregated_avg_kills():
    return get_aggregated_stat('avgkills')