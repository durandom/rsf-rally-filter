from rich.console import Console
from rich.table import Table

class RallyUI:
    def __init__(self):
        self.console = Console()

    def display_rallies(self, rallies):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Rally Name")
        table.add_column("Car Group")
        # Add more columns as needed

        for rally in rallies:
            # Assuming rally is an object with properties 'name' and 'car_group'
            table.add_row(rally.name, rally.car_groups[0])

        self.console.print(table)

    def display_car_group(self, car_group):
        self.console.print(f"Car Group: {car_group.name}")
        for car in car_group.cars:
            self.console.print(f"\t{car.model}")

