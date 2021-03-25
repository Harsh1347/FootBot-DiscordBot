import requests
import json
import time
from bs4 import BeautifulSoup
from plyer import notification
# session = requests.session()
# url = 'https://users.premierleague.com/accounts/login/'
# payload = {
#     'password': 'Saanvi@28',
#     'login': 'harshvai07@gmail.com',
#     'redirect_uri': 'https://fantasy.premierleague.com/a/login',
#     'app': 'plfpl-web'
# }

# session.post(url, data=payload)

# response = session.get('https://fantasy.premierleague.com/api/my-team/2445319')
# print(response.json())


# if __name__ == "__main__":
#     for i in range(5):
#         notification.notify(
#             title="Score Update",
#             message=get_cricket_score("india vs england"),
#             timeout=10)
#         time.sleep(10)
