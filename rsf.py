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

class Rally:
    def __init__(self, status, name, description, starts, finishs, legs, stages, creator, damage, open, results, car_groups):
        self.status = status
        self.name = name
        self.description = description
        self.starts = starts
        self.finishs = finishs
        self.legs = legs
        self.stages = stages
        self.creator = creator
        self.damage = damage
        self.open = open
        self.results = results
        self.car_groups = car_groups


    def __str__(self):
        return f"{self.name}"

class Rsf:
    def __init__(self):
        self.cars = []
        self.car_groups = []
        self.rallies = []

    def add_rally(self, rally):
        self.rallies.append(rally)

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



