import requests
import pandas as pd
from tabulate import tabulate

URL = f"https://fantasy.premierleague.com/api/bootstrap-static/"
resp = requests.get(URL).json()
events = resp['events']

teams = {
}

for i, team in enumerate(resp['teams']):
    teams[i+1] = team['name']


def get_gw(gw=None):
    if gw:
        return events[gw-1]['id']
    else:
        for e in events:
            if e['is_current'] == True:
                return e['id']


def get_fixture(gw=0):
    FIX_URL = 'https://fantasy.premierleague.com/api/fixtures/'
    fixture_raw = requests.get(FIX_URL).json()
    fixture = {"Home Team": [], "Away Team": [], "Score": []}
    if gw < 0 or gw > 38:
        return
    if gw == 0:
        gw = gw = get_gw()

    for game in fixture_raw:
        if game['event'] == gw:
            fixture["Home Team"].append(teams[game['team_h']])
            fixture["Away Team"].append(teams[game['team_a']])
            if game['finished'] == True:
                fixture['Score'].append(
                    f"{game['team_h_score']} - {game['team_a_score']}")
            else:
                fixture['Score'].append("TBP")
    table = []
    for i in range(len(fixture['Home Team'])):
        vals = []
        vals.append(fixture['Home Team'][i])
        vals.append(fixture['Away Team'][i])
        vals.append(fixture['Score'][i])
        table.append(vals)
    return tabulate(table, headers=["Home Team", "Away Team", "Score"], tablefmt="pretty")
