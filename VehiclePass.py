from datetime import datetime

class VehiclePass:
    
    def __init__(self, pass_date: datetime, vehicle_number, color, brand):
        self.__pass_date = pass_date
        self.__vehicle_number = vehicle_number
        self.__color = color
        self.__brand = brand
    
    @property
    def pass_date(self) -> datetime:
        return self.__pass_date
    
    @property
    def vehicle_number(self):
        return self.__vehicle_number
    
    @property
    def color(self):
        return self.__color
    
    @property
    def brand(self):
        return self.__brand
    
    def __str__(self):
        raise NotImplementedError("Must be implemented in subclasses")