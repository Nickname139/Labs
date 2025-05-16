from PersonalCar import PersonalCar
from Truck import Truck
from Bus import Bus
from datetime import datetime

def file_to_passes_list(filename):
    passes = []
    
    with open(filename, "r") as file:
        for line in file:
            vehicle_type, values = line.strip().split("(")
            values = values[:-1].split(", ")
            
            pass_date = datetime.strptime(values[0], "%d.%m.%Y")
            vehicle_number = values[1].strip('"')
            color = values[2].strip('"')
            brand = values[3].strip('"')
            
            if vehicle_type == "PersonalCar":
                passes.append(PersonalCar(pass_date, vehicle_number, color, brand, int(values[4])))
            elif vehicle_type == "Truck":
                passes.append(Truck(pass_date, vehicle_number, color, brand, int(values[4])))
            elif vehicle_type == "Bus":
                passes.append(Bus(pass_date, vehicle_number, color, brand, int(values[4])))
    
    return passes

if __name__ == "__main__":
    vehicle_passes = file_to_passes_list('vehicle_passes.txt')
    for vehicle_pass in vehicle_passes:
        print(vehicle_pass)