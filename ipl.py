import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
header = {
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
}


def get_ipl_table():

    page = requests.get(
        f"https://www.sportskeeda.com/go/ipl/points-table", headers=header)
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
    return tabulate(teams, headers=["Team", "P", "W", "L", "D", "NRR", "Pts"], tablefmt="pretty")


def get_yester_match_result():
    page = requests.get(
        "https://www.sportskeeda.com/cricket/yesterday-ipl-match-result", headers=header)
    soup = BeautifulSoup(page.content, 'lxml')
    div_tag = soup.find('div', class_="taxonomy-content")
    para_tags = div_tag.find_all("p")
    info = []
    for para in para_tags[:-10]:
        if para.text != "":
            info.append(para.text)
    info.pop(5)
    info.pop(4)
    summary = info[0]
    scoreBoard = f"{info[1]}\n{info[2]}\n{info[3]}\nMan of the Match: {info[-2]}\n"

    maxStatsBatsmen = f"Most Runs : {info[4]}\nMost Sixes : {info[-1]}\n"
    maxStatsBowler = f"Most Wickets : {info[5]}"
    return (summary, scoreBoard, maxStatsBatsmen, maxStatsBowler)


if __name__ == "__main__":
    print(get_yester_match_result())
