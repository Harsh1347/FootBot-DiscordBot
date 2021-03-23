import requests
import json
import time
from bs4 import BeautifulSoup


def get_cricket_score(team_name):
    header = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
    }
    team = team_name.lower().split()
    team.append("cricket+score")
    team = "+".join(team)
    URL = f"https://www.google.com/search?q={team}"
    page = requests.get(URL, headers=header)
    soup = BeautifulSoup(page.content, 'lxml')
    scores = soup.find(
        'div', class_="imso_mh__scr-sep")

    team1_score = scores.find(
        'div', class_="imspo_mh_cricket__first-score imspo_mh_cricket__one-innings-column-with-overs").text
    team2_score = scores.find(
        'div', class_="imspo_mh_cricket__second-score imspo_mh_cricket__one-innings-column-with-overs").text

    team_playing = soup.find_all(
        'div', class_="ellipsisize liveresults-sports-immersive__team-name-width kno-fb-ctx")

    cricket = []
    for t in team_playing:
        cricket.append(t.text)

    toss = soup.find(
        'div', class_="imso_mh__score-txt imso-ani imspo_mh_cricket__summary-sentence").text

    score_card = f"{cricket[0]} : {team1_score} \t {cricket[1]} : {team2_score}"
    return(score_card+"\n"+toss)
