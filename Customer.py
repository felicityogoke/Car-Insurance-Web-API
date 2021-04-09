import uuid


# Represents the customer of the car insurance company
class Customer:
    def __init__(self, name, address):
        self.ID = str(uuid.uuid1())
        self.name = name
        self.address = address
        self.cars = []
        self.claims = []
        self.payments = 0

    def addCar(self, car):
        self.cars.append(car)

        # removing car

    def deleteCar(self, car):
        for c in self.cars:
            if c == car:
                self.cars.remove(c)

    def File_claim(self, claim):
        self.claims.append(claim)

    # convert object to JSON
    def serialize(self):
        return {
            'id': self.ID,
            'name': self.name,
            'address': self.address,
            'Cars': self.cars,
            'claims': self.claims
        }


class Car:
    def __init__(self, model_name, number_plate, motor_power, year):
        self.name = model_name
        self.number_plate = number_plate
        self.motor_power = motor_power
        self.year = year

    def serialize(self):
        return {
            'model_name': self.name,
            'number_plate': self.number_plate,
            'motor_power': self.motor_power,
            'year': self.year
        }
