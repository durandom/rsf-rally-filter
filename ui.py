from rich.console import Console
from rich.table import Table

class RallyUI:
    def __init__(self):
        self.console = Console()

    def display_rallies(self, rallies, car_group=None):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Rally Name")
        table.add_column("Description")
        table.add_column("S/F")
        table.add_column("Stages / Legs")
        table.add_column("Car Group")
        # Add more columns as needed

        display = []

        for rally in rallies:
            # Assuming rally is an object with properties 'name' and 'car_group'
            if car_group:
                if car_group.name in rally.car_groups:
                    display.append(rally)
            else:
                display.append(rally)

        # sort display by stages
        display.sort(key=lambda x: x.stages)
        for rally in display:
            table.add_row(rally.name,
                            rally.description,
                            f"{rally.starts} / {rally.finishs}",
                            f"{rally.stages} / {rally.legs}",
                          ', '.join(rally.car_groups)
                          )

        self.console.print(table)

    def display_car_group(self, car_group):
        self.console.print(f"Car Group: {car_group.name}")
        for car in car_group.cars:
            self.console.print(f"\t{car.model}")

