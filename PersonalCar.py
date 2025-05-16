from VehiclePass import VehiclePass

class PersonalCar(VehiclePass):
    
    def __init__(self, pass_date, vehicle_number, color, brand, speed):
        super().__init__(pass_date, vehicle_number, color, brand)
        self.__speed = speed
    
    @property
    def speed(self):
        return self.__speed
    
    def __str__(self):
        return (f"Type: PersonalCar, Date: {self.pass_date.date()}, "
                f"Number: {self.vehicle_number}, Color: {self.color}, "
                f"Brand: {self.brand}, Speed: {self.speed} км/ч")
