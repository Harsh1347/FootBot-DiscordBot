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
        'div', class_="imspo_mh_cricket__first-score imspo_mh_cricket__one-innings-column-with-overs")
    team2_score = scores.find(
        'div', class_="imspo_mh_cricket__second-score imspo_mh_cricket__one-innings-column-with-overs")

    if not team1_score:
        score_list = []
        first_team_scores = scores.find(
            'div', class_="imspo_mh_cricket__first-score imspo_mh_cricket__two-innings-column")
        first_team_score = first_team_scores.find_all(
            "div", class_='imspo_mh_cricket__score-major')
        for s in first_team_score:
            score_list.append(s.text)
        team1_score = " & ".join(score_list)
    elif team1_score:
        team1_score = team1_score.text

    if not team2_score:
        score_list = []
        second_team_scores = scores.find(
            'div', class_="imspo_mh_cricket__second-score imspo_mh_cricket__two-innings-column")
        second_team_score = second_team_scores.find_all(
            "div", class_='imspo_mh_cricket__score-major')
        for s in second_team_score:
            score_list.append(s.text)
        team2_score = " & ".join(score_list)
    elif team2_score:
        team2_score = team2_score.text

    team_playing = soup.find_all(
        'div', class_="ellipsisize liveresults-sports-immersive__team-name-width kno-fb-ctx")

    cricket = []
    for t in team_playing:
        cricket.append(t.text)

    toss = soup.find(
        'div', class_="imso_mh__score-txt imso-ani imspo_mh_cricket__summary-sentence").text

    score_card = f"{cricket[0]} : {team1_score} \t {cricket[1]} : {team2_score}"
    return(score_card+"\n"+toss)


if __name__ == '__main__':
    print(get_cricket_score("Srilanka"))
