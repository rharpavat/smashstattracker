from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

from .models import MatchDataTest

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")

 #    return render(request, "db.html", {"greetings": greetings})

def importdata(request):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json(os.environ.get('GOOGLE_API_KEY_FILE'),scope)
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

    MatchDataTest.objects.bulk_create(convertedData, ignore_conflicts=True)

    return redirect('index')



