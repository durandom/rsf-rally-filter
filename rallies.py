import argparse

from rsf import Rsf
from ui import RallyUI
from scraper import Scraper

def main(args):
    url = 'https://www.rallysimfans.hu/rbr/rally_online.php'
    scraper = Scraper(url)
    scraper.scrape(args.refresh)

    rsf = Rsf()
    rsf.parse_json()

    car_group = None

    ui = RallyUI()

    if args.group:
        group_name = args.group
        car_group = next((car_group for car_group in rsf.car_groups if car_group.name == group_name), None)
        if car_group:
            ui.display_car_group(car_group)
        else:
            # print all car groups
            for car_group in rsf.car_groups:
                ui.display_car_group(car_group)

    ui.display_rallies(scraper.rallies, car_group)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rally Data Scraper with Cache Option')
    parser.add_argument('--refresh', action='store_true', help='Refresh data by fetching new content')
    parser.add_argument('--group', type=str, help='Filter rallies for a given car group')
    args = parser.parse_args()
    main(args)
