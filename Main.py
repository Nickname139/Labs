import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableView, QPushButton, QLineEdit, QDateEdit, QSpinBox,
                             QLabel, QMessageBox, QFileDialog, QComboBox)
from PyQt6.QtCore import QDate, Qt, QAbstractTableModel
from datetime import datetime

class VehiclePass:

    def __init__(self, pass_date: datetime, vehicle_number, color, brand):
        self.__pass_date = pass_date
        self.__vehicle_number = vehicle_number
        self.__color = color
        self.__brand = brand
    
    @property
    def pass_date(self):
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

class PersonalCar(VehiclePass):

    def __init__(self, pass_date, vehicle_number, color, brand, speed):
        super().__init__(pass_date, vehicle_number, color, brand)
        self.__speed = speed
    
    @property
    def speed(self):
        return self.__speed
    
    def __str__(self):
        return (f"PersonalCar({self.pass_date.strftime('%d.%m.%Y')}, "
                f"\"{self.vehicle_number}\", \"{self.color}\", "
                f"\"{self.brand}\", {self.speed})")

class Truck(VehiclePass):

    def __init__(self, pass_date, vehicle_number, color, brand, weight):
        super().__init__(pass_date, vehicle_number, color, brand)
        self.__weight = weight
    
    @property
    def weight(self):
        return self.__weight
    
    def __str__(self):
        return (f"Truck({self.pass_date.strftime('%d.%m.%Y')}, "
                f"\"{self.vehicle_number}\", \"{self.color}\", "
                f"\"{self.brand}\", {self.weight})")

class Bus(VehiclePass):

    def __init__(self, pass_date, vehicle_number, color, brand, passenger_count):
        super().__init__(pass_date, vehicle_number, color, brand)
        self.__passenger_count = passenger_count
    
    @property
    def passenger_count(self):
        return self.__passenger_count
    
    def __str__(self):
        return (f"Bus({self.pass_date.strftime('%d.%m.%Y')}, "
                f"\"{self.vehicle_number}\", \"{self.color}\", "
                f"\"{self.brand}\", {self.passenger_count})")

class VehicleManager:
    def __init__(self):
        self.vehicles = []
    
    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
    
    def delete_vehicle(self, index):
        if 0 <= index < len(self.vehicles):
            del self.vehicles[index]
    
    def clear_vehicles(self):
        self.vehicles = []
    
    def get_vehicles(self):
        return self.vehicles.copy()

class VehicleTableModel(QAbstractTableModel):
    def __init__(self, vehicle_manager, parent=None):
        super().__init__(parent)
        self.vehicle_manager = vehicle_manager
        self.headers = ["Pass Date", "Number", "Color", "Brand", "Special Attribute"]
    
    def columnCount(self, parent=None):
        return len(self.headers)
    
    def rowCount(self, parent=None):
        return len(self.vehicle_manager.vehicles)
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        
        vehicle = self.vehicle_manager.vehicles[index.row()]
        
        if index.column() == 0:
            return vehicle.pass_date.strftime("%d.%m.%Y")
        elif index.column() == 1:
            return vehicle.vehicle_number
        elif index.column() == 2:
            return vehicle.color
        elif index.column() == 3:
            return vehicle.brand
        elif index.column() == 4:
            if isinstance(vehicle, PersonalCar):
                return f"Speed: {vehicle.speed} km/h"
            elif isinstance(vehicle, Truck):
                return f"Weight: {vehicle.weight} kg"
            elif isinstance(vehicle, Bus):
                return f"Passengers: {vehicle.passenger_count}"
        return None
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.headers[section]
        return None

class VehicleFormManager:
    def __init__(self, special_layout):
        self.special_layout = special_layout
        self.special_fields = []
    
    def update_form_fields(self, vehicle_type):
        self.clear_fields()
        
        if vehicle_type == "PersonalCar":
            self.create_personal_car_fields()
        elif vehicle_type == "Truck":
            self.create_truck_fields()
        elif vehicle_type == "Bus":
            self.create_bus_fields()
    
    def clear_fields(self):
        for i in reversed(range(self.special_layout.count())): 
            self.special_layout.itemAt(i).widget().setParent(None)
        self.special_fields = []
    
    def create_personal_car_fields(self):
        speed_label = QLabel("Speed (km/h):")
        speed_input = QSpinBox()
        speed_input.setMinimum(1)
        speed_input.setMaximum(300)
        self.special_layout.addWidget(speed_label)
        self.special_layout.addWidget(speed_input)
        self.special_fields = [speed_input]
    
    def create_truck_fields(self):
        weight_label = QLabel("Weight (kg):")
        weight_input = QSpinBox()
        weight_input.setMinimum(1000)
        weight_input.setMaximum(100000)
        self.special_layout.addWidget(weight_label)
        self.special_layout.addWidget(weight_input)
        self.special_fields = [weight_input]
    
    def create_bus_fields(self):
        passengers_label = QLabel("Passengers:")
        passengers_input = QSpinBox()
        passengers_input.setMinimum(1)
        passengers_input.setMaximum(200)
        self.special_layout.addWidget(passengers_label)
        self.special_layout.addWidget(passengers_input)
        self.special_fields = [passengers_input]
    
    def get_special_field_value(self):
        if self.special_fields:
            return self.special_fields[0].value()
        return None

class VehicleFileHandler:
    @staticmethod
    def save_vehicles(vehicles, filename):
        with open(filename, 'w') as file:
            for vehicle in vehicles:
                file.write(str(vehicle) + "\n")
    
    @staticmethod
    def load_vehicles(filename):
        vehicles = []
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    vehicle_type, values = line.split("(")
                    values = values[:-1].split(", ")
                    
                    pass_date = datetime.strptime(values[0], "%d.%m.%Y")
                    number = values[1].strip('"')
                    color = values[2].strip('"')
                    brand = values[3].strip('"')
                    extra_param = int(values[4])
                    
                    if vehicle_type == "PersonalCar":
                        vehicles.append(PersonalCar(pass_date, number, color, brand, extra_param))
                    elif vehicle_type == "Truck":
                        vehicles.append(Truck(pass_date, number, color, brand, extra_param))
                    elif vehicle_type == "Bus":
                        vehicles.append(Bus(pass_date, number, color, brand, extra_param))
                except Exception as e:
                    print(f"Error parsing line: {line}\n{str(e)}")
        return vehicles

class VehicleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vehicle Pass System")
        self.setGeometry(100, 100, 1000, 600)
        
        self.vehicle_manager = VehicleManager()
        self.file_handler = VehicleFileHandler()
        
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Table View
        self.table_view = QTableView()
        self.table_model = VehicleTableModel(self.vehicle_manager)
        self.table_view.setModel(self.table_model)
        layout.addWidget(self.table_view)
        
        # Form Layout
        form_layout = QHBoxLayout()
        
        # Vehicle Type
        type_layout = QVBoxLayout()
        type_layout.addWidget(QLabel("Vehicle Type:"))
        self.type_select = QComboBox()
        self.type_select.addItems(["PersonalCar", "Truck", "Bus"])
        type_layout.addWidget(self.type_select)
        form_layout.addLayout(type_layout)
        
        # Date
        date_layout = QVBoxLayout()
        date_layout.addWidget(QLabel("Pass Date:"))
        self.date_edit = QDateEdit(QDate.currentDate())
        date_layout.addWidget(self.date_edit)
        form_layout.addLayout(date_layout)
        
        # Number
        number_layout = QVBoxLayout()
        number_layout.addWidget(QLabel("Vehicle Number:"))
        self.number_edit = QLineEdit()
        number_layout.addWidget(self.number_edit)
        form_layout.addLayout(number_layout)
        
        # Color
        color_layout = QVBoxLayout()
        color_layout.addWidget(QLabel("Color:"))
        self.color_edit = QLineEdit()
        color_layout.addWidget(self.color_edit)
        form_layout.addLayout(color_layout)
        
        # Brand
        brand_layout = QVBoxLayout()
        brand_layout.addWidget(QLabel("Brand:"))
        self.brand_edit = QLineEdit()
        brand_layout.addWidget(self.brand_edit)
        form_layout.addLayout(brand_layout)
        
        # Special Fields
        self.special_layout = QHBoxLayout()
        form_layout.addLayout(self.special_layout)
        
        # Form Manager
        self.form_manager = VehicleFormManager(self.special_layout)
        self.type_select.currentTextChanged.connect(self.on_type_changed)
        self.on_type_changed()
        
        # Add Button
        self.add_button = QPushButton("Add Vehicle")
        self.add_button.clicked.connect(self.add_vehicle)
        form_layout.addWidget(self.add_button)
        
        layout.addLayout(form_layout)
        
        # Button Layout
        button_layout = QHBoxLayout()
        
        # Load Button
        self.load_button = QPushButton("Load Data")
        self.load_button.clicked.connect(self.load_vehicles)
        button_layout.addWidget(self.load_button)
        
        # Save Button
        self.save_button = QPushButton("Save Data")
        self.save_button.clicked.connect(self.save_vehicles)
        button_layout.addWidget(self.save_button)
        
        # Delete Button
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_vehicle)
        button_layout.addWidget(self.delete_button)
        
        layout.addLayout(button_layout)
    
    def on_type_changed(self):
        self.form_manager.update_form_fields(self.type_select.currentText())
    
    def add_vehicle(self):
        number = self.number_edit.text().strip()
        color = self.color_edit.text().strip()
        brand = self.brand_edit.text().strip()
        
        if not number or not color or not brand:
            QMessageBox.warning(self, "Warning", "All fields must be filled!")
            return
        
        pass_date = datetime.combine(
            self.date_edit.date().toPyDate(),
            datetime.min.time()
        )
        
        special_value = self.form_manager.get_special_field_value()
        vehicle_type = self.type_select.currentText()
        
        try:
            if vehicle_type == "PersonalCar":
                vehicle = PersonalCar(pass_date, number, color, brand, special_value)
            elif vehicle_type == "Truck":
                vehicle = Truck(pass_date, number, color, brand, special_value)
            else:
                vehicle = Bus(pass_date, number, color, brand, special_value)
            
            self.vehicle_manager.add_vehicle(vehicle)
            self.table_model.layoutChanged.emit()
            self.clear_form()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add vehicle: {str(e)}")
    
    def clear_form(self):
        self.number_edit.clear()
        self.color_edit.clear()
        self.brand_edit.clear()
        if self.form_manager.special_fields:
            self.form_manager.special_fields[0].setValue(0)
    
    def delete_vehicle(self):
        selected = self.table_view.currentIndex()
        if not selected.isValid():
            QMessageBox.warning(self, "Warning", "Please select a vehicle to delete!")
            return
        
        reply = QMessageBox.question(
            self, "Confirm Delete", 
            "Are you sure you want to delete this vehicle?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.vehicle_manager.delete_vehicle(selected.row())
            self.table_model.layoutChanged.emit()
    
    def save_vehicles(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "Text Files (*.txt);;All Files (*)"
        )
        if filename:
            try:
                self.file_handler.save_vehicles(
                    self.vehicle_manager.get_vehicles(),
                    filename
                )
                QMessageBox.information(self, "Success", "Data saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
    
    def load_vehicles(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Text Files (*.txt);;All Files (*)"
        )
        if filename:
            try:
                vehicles = self.file_handler.load_vehicles(filename)
                self.vehicle_manager.clear_vehicles()
                for vehicle in vehicles:
                    self.vehicle_manager.add_vehicle(vehicle)
                self.table_model.layoutChanged.emit()
                QMessageBox.information(self, "Success", "Data loaded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VehicleWindow()
    window.show()
    sys.exit(app.exec())