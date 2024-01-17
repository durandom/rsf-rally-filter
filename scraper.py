import requests
from bs4 import BeautifulSoup
import os
import re
from rsf import Rally

class Scraper:
    def __init__(self, url, cache_file='rally_data_cache.html'):
        self.url = url
        self.cache_file = cache_file
        self.html_content = ''
        self.rallies = []

    def fetch_html(self):
        response = requests.get(self.url)
        return response.text

    def parse_html(self):
        # The columns in the table
        # <tr class="fejlec2"><td class="rally_list_name" align="center"><b>Rally name</b></td><td class="rally_list_description" align="center"><b>Description</b></td><td class="rally_list_stages" align="center"><b>Stages /<BR>Legs</b></td><td class="rally_list_creator" align="center"><b>Creator</b></td><td class="rally_list_damage" align="center"><b>Damage</b></td><td class="rally_list_open" align="center"><b>Open /<BR>Close</b></td><td width=25 align="center">edit</td></tr>
        # a row in the table
        # <tr class="lista_free_ngp6"><td class="rally_list_status"></td><td class="rally_list_name" align="left" onmouseover="Tip('<div align=left><b>R5/Rally 2 vs Group B</b></div><br> <b>Car Groups</b> : Group B, Group R5, Rally 2')" onmouseout="UnTip()"><a href="/rbr/rally_online.php?centerbox=rally_list_details.php&rally_id=64909">PSR Rally - Are you brave enough?</a></td><td class="rally_list_description" align="left"><div class="rally_list_description">R5/Rally 2 vs Group B</div></td><td class="rally_list_sf" align="center">43/12</td><td class="rally_list_stages" align="center">7/6</td><td class="rally_list_creator" align="center"><a href="usersstats.php?user_stats=24098" title="Stats">MCKRS</a><td class="rally_list_damage" align="center">Reduced</td><td class="rally_list_open" align="center">01-15 13:35<br>01-22 13:00</td><td class="rally_list_res" align="center"><div class="tooltip-link" onclick=window.location="?centerbox=rally_results.php&rally_id=64909"><span class="tooltiptext">See results</span><img src='images/watch_small.png'></div></td></tr>
        soup = BeautifulSoup(self.html_content, 'html.parser')

        # find all tables with "widht=100%" attribute as the only attribute
        tables = soup.find_all('table', attrs={'width': '100%'})

        for table in tables:
            # if the table contains another table, skip it
            if table.find('table'):
                continue
            # check if the table has a td with the class "rally_list_name"
            if table.find('td', attrs={'class': 'rally_list_name'}):
                # check if a td has onmouseover attribute
                if table.find('td', attrs={'onmouseover': True}):
                    self.parse_rallies(table)


    def parse_td(self, row, class_name):
        td = row.find('td', attrs={'class': class_name})
        if td:
            return td.text.strip()
        else:
            return ""


    def parse_rallies(self, table):

        for row in table.find_all('tr')[1:]:
            columns = row.find_all('td')
            # status is the content of the column with the class "rally_list_status"
            # find the td with the class "rally_list_status" and get the text
            stages = self.parse_td(row, 'rally_list_stages')
            # stages has the format "7/6"
            # perform a regexp match to see if its the format

            if not re.match(r'\d+\/\d+', stages):
                continue

            status = self.parse_td(row, 'rally_list_status')
            name = self.parse_td(row, 'rally_list_name')
            description = self.parse_td(row, 'rally_list_description')
            sf = self.parse_td(row, 'rally_list_sf')
            creator = self.parse_td(row, 'rally_list_creator')
            damage = self.parse_td(row, 'rally_list_damage')
            open = self.parse_td(row, 'rally_list_open')
            results = self.parse_td(row, 'rally_list_res')

            # get the allowed car groups
            # find the td with the onmouseover attribute
            # onmouseover="Tip('<div align=left><b>R5/Rally 2 vs Group B</b></div><br> <b>Car Groups</b> : Group B, Group R5, Rally 2')"
            td = row.find('td', attrs={'onmouseover': True})
            if td:
                # get the text of the onmouseover attribute
                # split the text by the "Car Groups" string
                # get the second part of the split
                txt = td['onmouseover'].split('Car Groups')[1].split(':')[1].strip()
                # remove "')" from the end of the string if it exists
                if txt.endswith("')"):
                    txt = txt[:-2]
                car_groups = txt.split(', ')
            else:
                car_groups = ""

            legs = int(stages.split('/')[1])
            stages = int(stages.split('/')[0])

            if sf == "":
                starts = 0
                finishs = 0
            else:
                starts = int(sf.split('/')[0])
                finishs = int(sf.split('/')[1])

            rally = Rally(status, name, description, starts, finishs, legs, stages, creator, damage, open, results, car_groups)
            self.rallies.append(rally)

    def refresh_data(self, refresh):
        if refresh or not os.path.exists(self.cache_file):
            print("Fetching new data...")
            self.html_content = self.fetch_html()
            with open(self.cache_file, 'w', encoding='utf-8') as file:
                file.write(self.html_content)
        else:
            print("Using cached data...")
            with open(self.cache_file, 'r', encoding='utf-8') as file:
                self.html_content = file.read()

    def scrape(self, refresh=False):
        self.refresh_data(refresh)
        self.parse_html()
