from VehiclePass import VehiclePass

class Bus(VehiclePass):
    def __init__(self, pass_date, vehicle_number, color, brand, passenger_count):
        super().__init__(pass_date, vehicle_number, color, brand)
        self.__passenger_count = passenger_count
    
    @property
    def passenger_count(self):
        return self.__passenger_count
    
    def __str__(self):
        return (f"Type: Bus, Date: {self.pass_date.date()}, "
                f"Number: {self.vehicle_number}, Color: {self.color}, "
                f"Brand: {self.brand}, Passengers: {self.passenger_count}")