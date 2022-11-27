
from bs4 import BeautifulSoup
import urllib.request
import http.client

LEADERBOARD_1 = 'https://www.codewars.com/users/leaderboard'
LEADERBOARD_2 = "https://www.codewars.com/users/leaderboard/kata"
LEADERBOARD_3 = "https://www.codewars.com/users/leaderboard/authored"

# Подключение к странице с таблицей лидеров и парсинг списка пользователей
def getUsernames(source):
    page = urllib.request.urlopen(source)
    data = http.client.HTTPResponse.read(page)
    soup = BeautifulSoup(data, 'html.parser')
    body = soup.find('body')

    div = body.find('div', attrs={'class':'leaderboard p-0'})
    table = div.find('table')
    table_rows = table.find_all("tr")

    users = set()
    for i in range(1, len(table_rows)):
        curr_row = table_rows[i]
        users.add(curr_row['data-username'])
    
    return users

# Метод получения полного списка лидерам
def getLeadernames():
    return getUsernames(LEADERBOARD_1) | getUsernames(LEADERBOARD_2) | getUsernames(LEADERBOARD_3)


def getUsernamesFromKataList():
    usernames = set()

    page = urllib.request.urlopen("https://www.codewars.com/kata/search/?q=&beta=false&sample=true")
    
    data = http.client.HTTPResponse.read(page)
    soup = BeautifulSoup(data, 'html.parser')

    main = soup.find('main', { "id": "shell_content" })
    rows = main.find_all('div', { "class" : "list-item-kata bg-ui-section p-4 rounded-lg shadow-md" })

    for row in rows:
        element = row.find('a', { "data-tippy-content" : "This kata's Sensei" })
        if element is not None and len(element) >= 2:
            usernames.add(element.contents[1])

    return usernames


























