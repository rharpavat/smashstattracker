import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint as pp

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("smashstattracker-f6677d9a54c2.json",scope)
client = gspread.authorize(creds)

sheet = client.open("SmashStats").worksheet("StatTest")
data = sheet.get_values()

trimmedData = data[1:]
consolidatedData = [item[:7] + item[13:] for item in trimmedData]
for row in consolidatedData:
    print(row)