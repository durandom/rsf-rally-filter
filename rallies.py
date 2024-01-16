import requests
from bs4 import BeautifulSoup
import argparse
import os

# The columns in the table
# <tr class="fejlec2"><td class="rally_list_name" align="center"><b>Rally name</b></td><td class="rally_list_description" align="center"><b>Description</b></td><td class="rally_list_stages" align="center"><b>Stages /<BR>Legs</b></td><td class="rally_list_creator" align="center"><b>Creator</b></td><td class="rally_list_damage" align="center"><b>Damage</b></td><td class="rally_list_open" align="center"><b>Open /<BR>Close</b></td><td width=25 align="center">edit</td></tr>
# a row in the table
# <tr class="lista_free_ngp6"><td class="rally_list_status"></td><td class="rally_list_name" align="left" onmouseover="Tip('<div align=left><b>R5/Rally 2 vs Group B</b></div><br> <b>Car Groups</b> : Group B, Group R5, Rally 2')" onmouseout="UnTip()"><a href="/rbr/rally_online.php?centerbox=rally_list_details.php&rally_id=64909">PSR Rally - Are you brave enough?</a></td><td class="rally_list_description" align="left"><div class="rally_list_description">R5/Rally 2 vs Group B</div></td><td class="rally_list_sf" align="center">43/12</td><td class="rally_list_stages" align="center">7/6</td><td class="rally_list_creator" align="center"><a href="usersstats.php?user_stats=24098" title="Stats">MCKRS</a><td class="rally_list_damage" align="center">Reduced</td><td class="rally_list_open" align="center">01-15 13:35<br>01-22 13:00</td><td class="rally_list_res" align="center"><div class="tooltip-link" onclick=window.location="?centerbox=rally_results.php&rally_id=64909"><span class="tooltiptext">See results</span><img src='images/watch_small.png'></div></td></tr>


class RallyScraper:
    def __init__(self, url, cache_file='rally_data_cache.html'):
        self.url = url
        self.cache_file = cache_file
        self.html_content = ''

    def fetch_html(self):
        response = requests.get(self.url)
        return response.text

    def parse_html(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')

        for row in soup.find_all('tr')[1:]:
            columns = row.find_all('td')
            rally_name = columns[0].text.strip()
            description = columns[1].text.strip()
            print(f"Rally Name: {rally_name}, Description: {description}")

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


def main(refresh):
    url = 'https://www.rallysimfans.hu/rbr/rally_online.php'
    scraper = RallyScraper(url)
    scraper.scrape(refresh)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rally Data Scraper with Cache Option')
    parser.add_argument('--refresh', action='store_true', help='Refresh data by fetching new content')
    args = parser.parse_args()
    main(args.refresh)
