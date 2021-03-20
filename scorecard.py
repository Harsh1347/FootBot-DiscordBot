import requests
from bs4 import BeautifulSoup
import time


def get_score(team_name):
    team = team_name.lower().split()
    team = "+".join(team)

    URL = f"https://www.google.com/search?q={team}"
    header = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}
    page = requests.get(URL, headers=header)

    soup = BeautifulSoup(page.content, 'lxml')
    try:
        match_time = soup.find(
            'span', class_="imso_mh__ft-mtch imso-medium-font imso_mh__ft-mtchc").text
    except:
        match_time = ""

    try:
        half_time = soup.find('div', class_="imso_mh__lv-m-stts-cont").text
    except:
        half_time = ""

    try:
        live_time = soup.find(
            'span', class_="liveresults-sports-immersive__game-minute").text
    except:
        live_time = ""
    score = soup.find('div', class_="imso_mh__ma-sc-cont").text
    team_name = []
    names = soup.find_all(
        'div', class_="ellipsisize liveresults-sports-immersive__team-name-width kno-fb-ctx")
    for n in names:
        team_name.append(n.text)
    if live_time == '':
        if half_time != '':
            live_time = half_time
        else:
            live_time = match_time
    team1 = score[0]
    team2 = score[-1]

    return f"{team_name[0]} {team1} - {team2} {team_name[1]} \nTime : {live_time}"
