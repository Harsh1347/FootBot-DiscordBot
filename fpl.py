import requests
import pandas as pd
from tabulate import tabulate

URL = f"https://fantasy.premierleague.com/api/bootstrap-static/"
resp = requests.get(URL).json()
events = resp['events']
elements = resp['elements']
element_type = {
    1: "GKP",
    2: "DEF",
    3: "MID",
    4: "FWD",
}

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


def get_live_stats():
    FIX_URL = 'https://fantasy.premierleague.com/api/fixtures/'
    fixture_raw = requests.get(FIX_URL).json()
    result = {}
    for game in fixture_raw:
        if game['started'] == True and game['finished'] == False:
            result['Home Team'] = TEAMS[game['team_h']]
            result['Away Team'] = TEAMS[game['team_a']]
            result['Home Score'] = game['team_h_score']
            result['Away Score'] = game['team_a_score']
            goal_home_scorer = game['stats'][0]['h']
            goal_away_scorer = game['stats'][0]['a']
            assist_home_scorer = game['stats'][1]['h']
            assist_away_scorer = game['stats'][1]['a']
            for val in goal_away_scorer:
                for player in elements:
                    if player['id'] == val['element']:
                        val['element'] = player['web_name']
            for val in goal_home_scorer:
                for player in elements:
                    if player['id'] == val['element']:
                        val['element'] = player['web_name']
            for val in assist_away_scorer:
                for player in elements:
                    if player['id'] == val['element']:
                        val['element'] = player['web_name']
            for val in assist_home_scorer:
                for player in elements:
                    if player['id'] == val['element']:
                        val['element'] = player['web_name']
            result['Goal Score Home'] = goal_home_scorer
            result['Goal Score Away'] = goal_away_scorer
            result['Assist Score Home'] = assist_home_scorer
            result['Assist Score Away'] = assist_away_scorer
    table = [["\n".join([f"{p['element']}(G)- {p['value']}" for p in result['Goal Score Home']]), "\n".join([f"{p['element']}(G)- {p['value']}" for p in result['Goal Score Away']])],
             ["\n".join([f"{p['element']}(A)- {p['value']}" for p in result['Assist Score Home']]), "\n".join([f"{p['element']}(A)- {p['value']}" for p in result['Assist Score Away']])]]

    return tabulate(table, headers=[f"{result['Home Team']}-{result['Home Score']}", f"{result['Away Team']}-{result['Away Score']}"], tablefmt="pretty")


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
        if game['event'] > looper:
            break
        if game['event'] < gw:
            continue
        else:
            if game['team_h'] == team_id:
                fixture.append(f"{SHORT_TEAMS[game['team_a']]} - Home")
            elif game['team_a'] == team_id:
                fixture.append(f"{SHORT_TEAMS[game['team_h']]} - Away")
    return fixture


def get_team_details(id):
    TEAM_URL = f'https://fantasy.premierleague.com/api/entry/{id}/event/29/picks/'
    MANG_URL = f'https://fantasy.premierleague.com/api/entry/{id}/'
    mang_raw = requests.get(MANG_URL).json()
    team_raw = requests.get(TEAM_URL).json()
    mang_name = f"{mang_raw['player_first_name']} {mang_raw['player_last_name']}"
    team_name = mang_raw['name']
    mang_info = f"Manager : {mang_name}\nTeam Name : {team_name}\n"
    players = team_raw['picks']
    eleven = []
    pos = []
    for player in players:
        for i in elements:
            if i['id'] == player['element']:
                if player['is_captain'] == True:
                    eleven.append(f"{i['web_name']}(C)")
                if player['is_vice_captain'] == True:
                    eleven.append(f"{i['web_name']}(VC)")
                if player['is_captain'] == False and player['is_vice_captain'] == False:
                    eleven.append(i['web_name'])
                pos.append(element_type[i['element_type']])
    lineup = f"Starting 11:\n\t\t\t  {eleven[0]}"
    for i in range(1, len(pos)):
        if i < 11:
            if pos[i] != pos[i-1]:
                lineup += f"\n{eleven[i]}"
            else:
                lineup += f"  {eleven[i]}"
        else:
            if i == 11:
                lineup += f"\nBench:\n{eleven[i]}"
            else:
                lineup += f", {eleven[i]}"

    return mang_info+lineup


def fpl_team_info(id):
    TEAM_URL = f'https://fantasy.premierleague.com/api/entry/{id}/history/'
    MANG_URL = f'https://fantasy.premierleague.com/api/entry/{id}/'
    team_raw = requests.get(TEAM_URL).json()
    mang_raw = requests.get(MANG_URL).json()
    mang_name = f"{mang_raw['player_first_name']} {mang_raw['player_last_name']}"
    team_name = mang_raw['name']
    leagues = mang_raw['leagues']
    current = team_raw['current']
    chips = team_raw['chips']
    data = [[ele['event'], ele['points'], ele['points_on_bench'], ele['event_transfers'], '']
            for ele in current]
    for chip in chips:
        data[chip['event']-1][-1] = chip['name']

    mang_info = f"Manager : {mang_name}\tTeam Name : {team_name}\t Region/Country : {mang_raw['player_region_name']}\nOverall Points : {mang_raw['summary_overall_points']}\tGameweek {mang_raw['current_event']} Points : {mang_raw['summary_event_points']} \n"
    mang_rank = f"Overall Rank : {mang_raw['summary_overall_rank']}\t Gameweek {mang_raw['current_event']} Rank : {mang_raw['summary_event_rank']}\n"
    mang_value = f"Team Value : {mang_raw['last_deadline_value']/10}\t Bank : {mang_raw['last_deadline_bank']/10}\n"
    cl = [[l['id'], l['name'], l['entry_rank'], l['entry_last_rank']]
          for l in leagues['classic']]
    h2h = [[l['id'], l['name'], l['entry_rank'], l['entry_last_rank']]
           for l in leagues['h2h']]
    gameweek_history = tabulate(data, headers=[
                                "Game Week", "Points", "Points on Bench", "Transfers Made", "Chip Played"], tablefmt="pretty")
    classic_leagues = tabulate(cl, headers=[
                               "League ID", "League Name", "Rank", "Previou Rank"], tablefmt="pretty")
    h2h_leagues = tabulate(h2h, headers=[
                           "League ID", "League Name", "Rank", "Previou Rank"], tablefmt="pretty")

    return (mang_info+mang_rank+mang_value, "\nGameweek History\n"+gameweek_history, "\n\nClassic Leagues\n"+classic_leagues, "\n\nHead-to-Head Leagues\n"+h2h_leagues)


if __name__ == '__main__':
    print(fpl_team_info(2445319))
