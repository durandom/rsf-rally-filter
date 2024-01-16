import requests
from bs4 import BeautifulSoup
import argparse
import os
import json


class Car:
    def __init__(self, **kwargs):
        self.car_id = kwargs.get('car_id')
        self.power = kwargs.get('power')
        self.torque = kwargs.get('torque')
        self.drive_train = kwargs.get('drive_train')
        self.engine = kwargs.get('engine')
        self.transmission = kwargs.get('transmission')
        self.weight = kwargs.get('weight')
        self.wdf = kwargs.get('wdf')
        self.steering_wheel = kwargs.get('steering_wheel')
        self.skin = kwargs.get('skin')
        self.model = kwargs.get('model')
        self.audio = kwargs.get('audio')
        self.year = kwargs.get('year')
        self.shifterType = kwargs.get('shifterType')
        self.id = kwargs.get('id')
        self.group = CarGroup()

    def __str__(self):
        return f"{self.model}"

class CarGroup:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.user_id = kwargs.get('user_id')
        self.main = kwargs.get('main')
        self.test = kwargs.get('test')
        self.ngp = kwargs.get('ngp')
        self.cars = []

    def add_car(self, car):
        self.cars.append(car)

    def __str__(self):
        return f"{self.name}"

class Rsf:
    def __init__(self):
        self.cars = []
        self.car_groups = []

    def parse_json(self):
        # the encoding is windows-1252
        with open('rsf/cars_data.json', 'r', encoding='windows-1252') as file:
            json_data = json.load(file)

        # {"car_id":"17","power":"55bhp \/ 6500rpm","torque":"65Nm \/ 5500rpm","drive_train":"RWD","engine":"","transmission":"4 gears","weight":"729kg","wdf":"44%","steering_wheel":"835","skin":"","model":"Fiat 126 version 1.2.6 2015-07-19 Frito Fixes by WorkerBee","audio":"aesthetic_sofa (Lorenzo), JJBruce","year":"1977","shifterType":"H-pattern","id":"17"}
        for car in json_data:
            car = Car(**car)
            self.cars.append(car)

        # {"id":"11","name":"WRC 2.0","user_id":"335","main":"22","test":"0","ngp":"6"}
        with open('rsf/cargroups.json', 'r', encoding='windows-1252') as file:
            json_data = json.load(file)

        for car_group in json_data:
            car_group = CarGroup(**car_group)
            self.car_groups.append(car_group)

        # {"group_id":"111","car_id":"91","id":"91","name":"Abarth Grande Punto S2000","ngp":"6"}
        with open('rsf/car_group_map.json', 'r', encoding='windows-1252') as file:
            json_data = json.load(file)

        for car_group_map in json_data:
            # get the car with car_id
            car = next((car for car in self.cars if car.car_id == car_group_map['car_id']), None)
            if car:
                # get the car group with group_id
                car_group = next((car_group for car_group in self.car_groups if car_group.id == car_group_map['group_id']), None)
                if car_group:
                    # append the car to the car group
                    car_group.add_car(car)
                    car.group = car_group

        print(f"Number of cars: {len(self.cars)}")
        print(f"Number of car groups: {len(self.car_groups)}")


class Rally:
    def __init__(self, status, name, description, sf, stages, creator, damage, open, results, car_groups):
        self.status = status
        self.name = name
        self.description = description
        self.sf = sf
        self.stages = stages
        self.creator = creator
        self.damage = damage
        self.open = open
        self.results = results
        self.car_groups = car_groups

    def __str__(self):
        return f"Rally Name: {self.name}, Description: {self.description}, Car Groups: {self.car_groups}"
class RallyScraper:
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

            status = self.parse_td(row, 'rally_list_status')
            name = self.parse_td(row, 'rally_list_name')
            description = self.parse_td(row, 'rally_list_description')
            sf = self.parse_td(row, 'rally_list_sf')
            stages = self.parse_td(row, 'rally_list_stages')
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
            # get the text of the onmouseover attribute
            # split the text by the "Car Groups" string
            # get the second part of the split

            rally = Rally(status, name, description, sf, stages, creator, damage, open, results, car_groups)
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


def main(args):
    url = 'https://www.rallysimfans.hu/rbr/rally_online.php'
    scraper = RallyScraper(url)
    scraper.scrape(args.refresh)

    # for rally in scraper.rallies:
    #     print(rally)

    rsf = Rsf()
    rsf.parse_json()

    car_group = None

    if args.group:
        group_name = args.group
        car_group = next((car_group for car_group in rsf.car_groups if car_group.name == group_name), None)
        if car_group:
            print(f"Car Group: {car_group}")
            for car in car_group.cars:
                print(f"\t{car}")
        else:
            print(f"Car Group {group_name} not found")
            # print all car groups
            for car_group in rsf.car_groups:
                print(f"\t{car_group}")

    for rally in scraper.rallies:
        # check if the rally has a car group
        if rally.car_groups:
            # check if the car group is found
            if car_group:
                # check if the car group is in the rally
                if car_group.name in rally.car_groups:
                    print(rally)
            else:
                print(rally)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rally Data Scraper with Cache Option')
    parser.add_argument('--refresh', action='store_true', help='Refresh data by fetching new content')
    parser.add_argument('--group', type=str, help='Filter rallies for a given car group')
    args = parser.parse_args()
    main(args)
