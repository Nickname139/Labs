from VehiclePass import VehiclePass

class Truck(VehiclePass):
    
    def __init__(self, pass_date, vehicle_number, color, brand, weight):
        super().__init__(pass_date, vehicle_number, color, brand)
        self.__weight = weight
    
    @property
    def weight(self):
        return self.__weight
    
    def __str__(self):
        return (f"Type: Truck, Date: {self.pass_date.date()}, "
                f"Number: {self.vehicle_number}, Color: {self.color}, "
                f"Brand: {self.brand}, Weight: {self.weight} кг")