import requests
import pandas as pd
from tabulate import tabulate

HELLO = """
Hi! I'm Footbot!
!eplfixture for epl matches
"""


URL = f"https://fantasy.premierleague.com/api/bootstrap-static/"
resp = requests.get(URL).json()
events = resp['events']

TEAMS = {
}

for i, team in enumerate(resp['teams']):
    TEAMS[i+1] = team['name']

SHORT_TEAMS = {}
for i, team in enumerate(resp['teams']):
    SHORT_TEAMS[i+1] = team['short_name']


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
            fixture["Home Team"].append(TEAMS[game['team_h']])
            fixture["Away Team"].append(TEAMS[game['team_a']])
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


def get_team_fixture(team_name, next_fix=5):
    team_id = None
    for k, v in SHORT_TEAMS.items():
        if v.lower() == team_name.lower():
            team_id = k

    gw = get_gw()
    FIX_URL = 'https://fantasy.premierleague.com/api/fixtures/'
    fixture_raw = requests.get(FIX_URL).json()
    looper = gw + next_fix
    if looper > 38:
        looper = 38
    fixture = []
    for game in fixture_raw:
        if game['event'] == None:
            continue
        if game['event'] >= looper:
            break
        if game['event'] < gw:
            continue
        else:
            if game['team_h'] == team_id:
                fixture.append(f"{SHORT_TEAMS[game['team_a']]} - Home")
            elif game['team_a'] == team_id:
                fixture.append(f"{SHORT_TEAMS[game['team_h']]} - Away")
    return fixture