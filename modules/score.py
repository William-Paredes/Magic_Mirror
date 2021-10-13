import requests
from bs4 import BeautifulSoup

def data():
    League = ['nba', 'nfl', 'mlb']
    url = f"http://www.espn.com/{League[0]}/schedule"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    date = soup.find('h2',{'class':'table-caption'})
    teamName = soup.find('a',{'class':'team-name'})
    
    for row in soup.select("table.schedule tbody tr"):
        #print(row)
        td = row.select("td.home")
        print(td)
        #home_team, away_team = row.select("team-name")

#        print(home_team.get_text(), away_team.get_text())

    return date.string

data()