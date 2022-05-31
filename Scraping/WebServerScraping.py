# --------------------------------------------------
# REQUIREMENTS:
# --------------------------------------------------
# pip install beautifulsoup4
# pip install requests
# pip install lxml
# --------------------------------------------------

# --------------------------------------------------
# CODE: SCRAPING
# --------------------------------------------------

from bs4 import BeautifulSoup 
import requests
import pandas as pd

df = pd.DataFrame(columns=['team', 'result', 'margin', 'ballRemaning', 'toss', 'bat', 'opposition', 'ground', 'date'])

for x in [1, 3]:
    source = requests.get('https://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;filter=advanced;home_or_away=' + str(x) + ';orderby=start;page=1;result=1;result=3;result=4;size=200;template=results;type=team;view=results').text

    soup = BeautifulSoup(source, 'lxml')

    pages = soup.find('html').body.find('div', id='ciHomeContent').div.find('div', class_='pnl650M').find_all('table')[1::2][0].tr.find_all('td')[0::1][0].find_all('b')[1::2][0].text

    for page in range(1, int(pages) + 1):
        s = 'https://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;filter=advanced;home_or_away=' + str(x) + ';orderby=start;page='+ str(page) + ';result=1;result=3;result=4;size=200;template=results;type=team;view=results'
        source = requests.get(s).text
        soup = BeautifulSoup(source, 'lxml')

        data = ''

        data = soup.find('html').body.find('div', id='ciHomeContent').div.find('div', class_='pnl650M').find_all('table')[2::3][0].tbody.find_all('tr')
        count = 0
        for i in data:
            team = i.find_all('td')[0::1][0].text.strip()
            result = i.find_all('td')[1::2][0].text.strip()
            margin = i.find_all('td')[2::3][0].text.strip()
            ballRemaining = i.find_all('td')[3::4][0].text.strip()
            toss = i.find_all('td')[4::5][0].text.strip()
            bat = i.find_all('td')[5::6][0].text.strip()
            opposition = i.find_all('td')[7::8][0].text.strip().split(' ')[1::]
            opposition = ' '.join(opposition)
            ground = i.find_all('td')[8::9][0].text.strip()
            date = i.find_all('td')[9::10][0].text.strip()
            df.loc[count] = [team, result, margin, ballRemaining, toss, bat, opposition, ground, date]
            count += 1
        if x == 1:
            df.to_csv('matchHome.csv', mode='a', index=False, header=False)
        else:
            df.to_csv('matchNeutral.csv', mode='a', index=False, header=False)

print("Scraping Complete")



# https://towardsdatascience.com/machine-learning-algorithms-for-football-prediction-using-statistics-from-brazilian-championship-51b7d4ea0bc8

# https://stackoverflow.com/questions/15513640/predicting-football-match-winners-based-only-on-previous-data-of-same-match

# https://towardsdatascience.com/can-we-beat-the-bookmaker-with-machine-learning-45e3b30fc921

# https://www.kaggle.com/code/seraquevence/1st-place-solution-football-prob-pred#Make-a-model

# https://www.kaggle.com/code/paulofelipe/blend-lstm-lgbm#Classification

# https://www.kaggle.com/code/saife245/football-match-prediction/notebook