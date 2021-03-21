import requests
from bs4 import BeautifulSoup
from tabulate import tabulate


def get_table(league):
    header = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
    }

    league = league.lower()
    if league in ['laliga', 'la liga']:
        league = 'la-liga'
    if league in ['serie-a', 'serie a']:
        league = 'serie-a-calcio'
    if league == 'efl':
        league = 'efl-championship'

    page = requests.get(
        f"https://www.sportskeeda.com/go/{league}/standings", headers=header)
    soup = BeautifulSoup(page.content, 'lxml')
    table = soup.find('table')
    rows = table.find_all('tr')
    teams = []
    for row in rows:
        info = row.find_all('td')
        team = []
        for i in info:
            team.append(i.text.strip())
        if len(team) == 0:
            continue

        teams.append(team)
    return tabulate(teams, headers=["Position", "Team", "Played", "Win", "Draw", "Loss", "GD", "Points"], tablefmt="pretty")
