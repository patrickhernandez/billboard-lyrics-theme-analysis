import pandas as pd
import requests
from bs4 import BeautifulSoup

class BillboardClient:

    def __init__(self):
        self.base_url = 'https://www.billboard.com'

    def get_hot100(self, dates):
        all_charts = []
        
        for date in dates:
            date_string = date.strftime('%Y-%m-%d')
            chart_url = f'{self.base_url}/charts/hot-100/{date_string}'
            response = requests.get(chart_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.select('ul.o-chart-results-list-row')

            for rank, row in enumerate(table, start=1):
                title = row.select_one('h3.c-title').get_text(strip=True)
                artists = row.select_one('span.c-label.a-no-trucate, span.c-label a').get_text(strip=True)

                all_charts.append({'trackTitle': title, 'artists': artists, 'date': date, 'rank': rank})

        return pd.DataFrame(all_charts)
