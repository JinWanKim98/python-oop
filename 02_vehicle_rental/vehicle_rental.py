from abc import ABC, abstractmethod

"""
Vehicle Rental System

This program implements a vehicle rental system with different types of vehicles
and rental options (daily/hourly).
"""


def round_to_nearest_5_cent(amount):
    """Rounds a dollar amount to the nearest 5 cents.
    Examples: $12.72 -> $12.70, $12.75 -> $12.75, $12.78 -> $12.80"""
    cents = round(amount * 100)
    remainder = cents % 5

    if remainder < 2.5:
        cents = cents - remainder  # Round down
    elif remainder > 2.5:
        cents = cents + (5 - remainder)  # Round up

    return cents / 100


class Vehicle(ABC):
    """Abstract base class for all vehicle types"""

    def __init__(self, vehicle_id, brand, rental_rate):
        """Initialize vehicle with ID, brand, and rental rate. All vehicles are initially available for rental."""
        self._vehicle_id = vehicle_id
        self._brand = brand
        self._rental_rate = rental_rate
        self._is_available = True  # Initially available

    @property
    def vehicle_id(self):
        """Get the vehicle's unique identifier"""
        return self._vehicle_id

    @property
    def brand(self):
        """Get the vehicle's brand/manufacturer"""
        return self._brand

    @property
    def rental_rate(self):
        """Get the vehicle's daily rental rate"""
        return self._rental_rate

    @property
    def is_available(self):
        """Check if the vehicle is currently available for rental"""
        return self._is_available

    @abstractmethod
    def calculate_rental_cost_by_days(self, days):
        """Calculate cost for daily rental - must be implemented by subclasses"""
        pass

    @abstractmethod
    def calculate_rental_cost_by_hours(self, hours):
        """Calculate cost for hourly rental - must be implemented by subclasses"""
        pass

    def rent_vehicle(self):
        """Mark vehicle as rented if it's available"""
        if self._is_available:
            self._is_available = False
            return True
        return False

    def return_vehicle(self):
        """Mark vehicle as returned if it's currently rented"""
        if not self._is_available:
            self._is_available = True
            return True
        return False

    @abstractmethod
    def __str__(self):
        """String representation of the vehicle"""
        pass


class Customer:
    """Class to store customer information"""

    def __init__(self, customer_id, name, phone, email):
        """Initialize customer with ID, name, contact details"""
        self._customer_id = customer_id
        self._name = name
        self._phone = phone
        self._email = email

    @property
    def customer_id(self):
        """Get the customer's unique identifier"""
        return self._customer_id

    @property
    def name(self):
        """Get the customer's name"""
        return self._name

    @property
    def phone(self):
        """Get the customer's phone number"""
        return self._phone

    @property
    def email(self):
        """Get the customer's email address"""
        return self._email

    def __str__(self):
        """String representation of customer details"""
        return f"[Customer]\nID: {self._customer_id}, Name: {self._name}\nPhone: {self._phone}, Email: {self._email}\n"


class Car(Vehicle):
    """Standard car implementation"""

    def __init__(self, vehicle_id, brand, rental_rate, seats, fuel_type):
        """Initialize car with vehicle details plus number of seats and fuel type"""
        super().__init__(vehicle_id, brand, rental_rate)
        self._seats = seats
        self._fuel_type = fuel_type

    @property
    def seats(self):
        """Get the number of seats in the car"""
        return self._seats

    @property
    def fuel_type(self):
        """Get the fuel type of the car"""
        return self._fuel_type

    def calculate_rental_cost_by_days(self, days):
        """Calculate daily rental cost - simply multiply daily rate by number of days"""
        return self._rental_rate * days

    def calculate_rental_cost_by_hours(self, hours):
        """Calculate hourly rental cost - daily rate divided by 12 times hours"""
        hourly_rate = self._rental_rate / 12
        return round_to_nearest_5_cent(hourly_rate * hours)

    def __str__(self):
        """String representation of car details"""
        return f"[Car]\nID: {self._vehicle_id}, Brand: {self._brand}\nRate: ${self._rental_rate}/day, Available: {self._is_available}\nSeats: {self._seats}, Fuel Type: {self._fuel_type}\n"


class ElectricCar(Car):
    """Electric car with eco-discount"""

    def __init__(self, vehicle_id, brand, rental_rate, seats, battery_capacity,
                 charging_time, range_per_charge, eco_discount):
        """Initialize electric car with standard car details plus EV-specific properties"""
        # Call parent constructor with "Electric" as fuel type
        super().__init__(vehicle_id, brand, rental_rate, seats, "Electric")
        self._battery_capacity = battery_capacity
        self._charging_time = charging_time
        self._range_per_charge = range_per_charge
        self._eco_discount = eco_discount

    @property
    def battery_capacity(self):
        """Get the battery capacity in kWh"""
        return self._battery_capacity

    @property
    def charging_time(self):
        """Get the charging time in hours"""
        return self._charging_time

    @property
    def range_per_charge(self):
        """Get the range per charge in km"""
        return self._range_per_charge

    @property
    def eco_discount(self):
        """Get the eco-discount percentage"""
        return self._eco_discount

    def calculate_rental_cost_by_days(self, days):
        """Calculate daily rental cost with eco-discount applied"""
        # Get base cost, then apply eco discount
        base_cost = super().calculate_rental_cost_by_days(days)
        discounted_cost = base_cost * (1 - self._eco_discount / 100)
        return discounted_cost

    def calculate_rental_cost_by_hours(self, hours):
        """Calculate hourly rental cost with eco-discount applied"""
        # Calculate with discount directly
        base_cost = self._rental_rate / 12 * hours
        discounted_cost = base_cost * (1 - self._eco_discount / 100)
        return round_to_nearest_5_cent(discounted_cost)

    def __str__(self):
        """String representation of electric car details"""
        return f"[ElectricCar]\nID: {self._vehicle_id}, Brand: {self._brand}\nRate: ${self._rental_rate}/day, Available: {self._is_available}\nSeats: {self._seats}, Fuel Type: {self._fuel_type}\nBattery: {self._battery_capacity} kWh, Charging Time: {self._charging_time}\nRange: {self._range_per_charge} km, Eco discount: {self._eco_discount}%\n"


class Bike(Vehicle):
    """Motorcycle implementation"""

    def __init__(self, vehicle_id, brand, rental_rate, cc, helmet_provided):
        """Initialize bike with vehicle details plus engine size and helmet info"""
        super().__init__(vehicle_id, brand, rental_rate)
        self._cc = cc  # Engine capacity
        self._helmet_provided = helmet_provided

    @property
    def cc(self):
        """Get the engine capacity in cc"""
        return self._cc

    @property
    def helmet_provided(self):
        """Check if helmet is provided with the bike"""
        return self._helmet_provided

    def calculate_rental_cost_by_days(self, days):
        """Calculate daily rental cost"""
        return self._rental_rate * days

    def calculate_rental_cost_by_hours(self, hours):
        """Calculate hourly rental cost - daily rate divided by 18 times hours"""
        # Bike hourly rate is daily rate divided by 18
        hourly_rate = self._rental_rate / 18
        return round_to_nearest_5_cent(hourly_rate * hours)

    def __str__(self):
        """String representation of bike details"""
        return f"[Bike]\nID: {self._vehicle_id}, Brand: {self._brand}\nRate: ${self._rental_rate}/day, Available: {self._is_available}\nCC: {self._cc}, Helmet Provided: {self._helmet_provided}\n"


class Truck(Vehicle):
    """Truck implementation - no hourly rental available"""

    def __init__(self, vehicle_id, brand, rental_rate, max_load, requires_special_license):
        """Initialize truck with vehicle details plus load capacity and license requirements"""
        super().__init__(vehicle_id, brand, rental_rate)
        self._max_load = max_load  # Maximum load capacity in tons
        self._requires_special_license = requires_special_license

    @property
    def max_load(self):
        """Get the maximum load capacity in tons"""
        return self._max_load

    @property
    def requires_special_license(self):
        """Check if a special license is required to drive this truck"""
        return self._requires_special_license

    def calculate_rental_cost_by_days(self, days):
        """Calculate daily rental cost"""
        return self._rental_rate * days

    def calculate_rental_cost_by_hours(self, hours):
        """Trucks cannot be rented by the hour"""
        # Trucks cannot be rented by the hour
        return None

    def __str__(self):
        """String representation of truck details"""
        return f"[Truck]\nID: {self._vehicle_id}, Brand: {self._brand}\nRate: ${self._rental_rate}/day, Available: {self._is_available}\nMax Load: {self._max_load} tons, Special License: {self._requires_special_license}\n"


class RentalRecord(ABC):
    """Abstract base class for rental records"""

    # Class variable for auto-incrementing record IDs
    _next_record_id = 1

    def __init__(self, customer, vehicle):
        """Initialize record with auto-generated ID, customer and vehicle references"""
        self._record_id = RentalRecord._next_record_id
        RentalRecord._next_record_id += 1  # Increment for next record
        self._customer = customer
        self._vehicle = vehicle
        self._is_returned = False  # Initially not returned

    @property
    def record_id(self):
        """Get the rental record's unique identifier"""
        return self._record_id

    @property
    def customer(self):
        """Get the customer who made this rental"""
        return self._customer

    @property
    def vehicle(self):
        """Get the vehicle that was rented"""
        return self._vehicle

    @property
    def is_returned(self):
        """Check if the vehicle has been returned"""
        return self._is_returned

    def mark_returned(self):
        """Mark this rental as returned"""
        if not self._is_returned:
            self._is_returned = True
            return True
        return False

    @abstractmethod
    def cost(self):
        """Get the cost of this rental"""
        pass

    @abstractmethod
    def __str__(self):
        """String representation of the rental record"""
        pass


class RentalRecord_Days(RentalRecord):
    """Daily rental record"""

    def __init__(self, customer, vehicle, days):
        """Initialize daily rental with customer, vehicle and rental period"""
        super().__init__(customer, vehicle)
        self._days = days
        # Calculate cost when record is created
        self._cost = vehicle.calculate_rental_cost_by_days(days)
        # Mark vehicle as rented
        vehicle.rent_vehicle()

    @property
    def days(self):
        """Get the number of days for this rental"""
        return self._days

    @property
    def cost(self):
        """Get the total cost of this rental"""
        return self._cost

    def __str__(self):
        """String representation of daily rental record"""
        vehicle_type = self._vehicle.__class__.__name__
        return f"[RentalRecord:By Day]\nID: {self._record_id}\nCustomer: {self._customer.name}\nVehicle type: {vehicle_type}\nVehicle ID: {self._vehicle.vehicle_id}\nCost: ${self._cost}\nReturned: {self._is_returned}\n"


class RentalRecord_Hours(RentalRecord):
    """Hourly rental record"""

    def __init__(self, customer, vehicle, hours):
        """Initialize hourly rental with customer, vehicle and rental period"""
        super().__init__(customer, vehicle)
        self._hours = hours
        # Calculate cost when record is created
        self._cost = vehicle.calculate_rental_cost_by_hours(hours)
        # Mark vehicle as rented
        vehicle.rent_vehicle()

    @property
    def hours(self):
        """Get the number of hours for this rental"""
        return self._hours

    @property
    def cost(self):
        """Get the total cost of this rental"""
        return self._cost

    def __str__(self):
        """String representation of hourly rental record"""
        vehicle_type = self._vehicle.__class__.__name__
        return f"[RentalRecord:By Hour]\nID: {self._record_id}\nCustomer: {self._customer.name}\nVehicle type: {vehicle_type}\nVehicle ID: {self._vehicle.vehicle_id}\nCost: ${self._cost}\nReturned: {self._is_returned}\n"


class RentalService:
    """Main service class to manage vehicles, customers and rentals"""

    def __init__(self):
        """Initialize empty collections for vehicles, customers and rental records"""
        self._vehicles = {}  # Dictionary of vehicles by ID
        self._customers = {}  # Dictionary of customers by ID
        self._records = []  # List of rental records

    def add_car(self, vehicle_id, brand, rental_rate, seats, fuel_type):
        """Add a new car to the system"""
        # Check if ID already exists
        if vehicle_id in self._vehicles:
            return False

        car = Car(vehicle_id, brand, rental_rate, seats, fuel_type)
        self._vehicles[vehicle_id] = car
        return True

    def add_electric_car(self, vehicle_id, brand, rental_rate, seats, battery_capacity,
                         charging_time, range_per_charge, eco_discount):
        """Add a new electric car to the system"""
        if vehicle_id in self._vehicles:
            return False

        ev = ElectricCar(vehicle_id, brand, rental_rate, seats, battery_capacity,
                         charging_time, range_per_charge, eco_discount)
        self._vehicles[vehicle_id] = ev
        return True

    def add_bike(self, vehicle_id, brand, rental_rate, cc, helmet_provided):
        """Add a new bike to the system"""
        if vehicle_id in self._vehicles:
            return False

        bike = Bike(vehicle_id, brand, rental_rate, cc, helmet_provided)
        self._vehicles[vehicle_id] = bike
        return True

    def add_truck(self, vehicle_id, brand, rental_rate, max_load, requires_special_license):
        """Add a new truck to the system"""
        if vehicle_id in self._vehicles:
            return False

        truck = Truck(vehicle_id, brand, rental_rate, max_load, requires_special_license)
        self._vehicles[vehicle_id] = truck
        return True

    def remove_vehicle(self, vehicle_id):
        """Remove a vehicle from the system"""
        # Check if vehicle exists
        if vehicle_id not in self._vehicles:
            return False

        # Can't remove if currently rented
        if not self._vehicles[vehicle_id].is_available:
            return False

        # Remove the vehicle from dictionary
        del self._vehicles[vehicle_id]
        return True

    def get_available_vehicles(self, vehicle_type=None):
        """Get all available vehicles, optionally filtered by type"""
        available_vehicles = []

        for vehicle in self._vehicles.values():
            # Skip if not available
            if not vehicle.is_available:
                continue

            # Skip if vehicle type doesn't match (if specified)
            if vehicle_type and vehicle.__class__.__name__ != vehicle_type:
                continue

            available_vehicles.append(vehicle)

        return available_vehicles

    def register_customer(self, customer_id, name, phone, email):
        """Register a new customer in the system"""
        # Check if customer ID already exists
        if customer_id in self._customers:
            return False

        customer = Customer(customer_id, name, phone, email)
        self._customers[customer_id] = customer
        return True

    def get_customer(self, customer_id):
        """Get customer by ID, return None if not found"""
        # Return None if customer doesn't exist
        return self._customers.get(customer_id, None)

    def get_vehicle(self, vehicle_id):
        """Get vehicle by ID, return None if not found"""
        # Return None if vehicle doesn't exist
        return self._vehicles.get(vehicle_id, None)

    def rent_vehicle_by_days(self, vehicle_id, customer_id, days):
        """Rent a vehicle for a specific number of days"""
        # Get vehicle and customer
        vehicle = self.get_vehicle(vehicle_id)
        customer = self.get_customer(customer_id)

        # Check if vehicle and customer exist
        if not vehicle or not customer:
            return False

        # Check if vehicle is available
        if not vehicle.is_available:
            return False

        # Create rental record
        record = RentalRecord_Days(customer, vehicle, days)
        self._records.append(record)
        return True

    def rent_vehicle_by_hours(self, vehicle_id, customer_id, hours):
        """Rent a vehicle for a specific number of hours"""
        # Get vehicle and customer
        vehicle = self.get_vehicle(vehicle_id)
        customer = self.get_customer(customer_id)

        # Check if vehicle and customer exist
        if not vehicle or not customer:
            return False

        # Check if vehicle is available
        if not vehicle.is_available:
            return False

        # Trucks can't be rented by hour
        if isinstance(vehicle, Truck):
            return False

        # Create rental record
        record = RentalRecord_Hours(customer, vehicle, hours)
        self._records.append(record)
        return True

    def return_vehicle(self, vehicle_id):
        """Process a vehicle return"""
        # Get vehicle
        vehicle = self.get_vehicle(vehicle_id)

        # Check if vehicle exists
        if not vehicle:
            return False

        # Can't return a vehicle that's not rented
        if vehicle.is_available:
            return False

        # Find and update the rental record
        for record in self._records:
            if record.vehicle.vehicle_id == vehicle_id and not record.is_returned:
                record.mark_returned()
                vehicle.return_vehicle()
                return True

        return False

    def get_rental_records(self, vehicle_type=None):
        """Get all rental records, optionally filtered by vehicle type"""
        # Return all records if no type specified
        if not vehicle_type:
            return self._records

        # Filter records by vehicle type
        filtered_records = []
        for record in self._records:
            if record.vehicle.__class__.__name__ == vehicle_type:
                filtered_records.append(record)

        return filtered_records


def main():
    """Test function to demonstrate functionality and error handling"""
    print("\n===== Vehicle Rental System Tests =====\n")

    # Create rental service
    rental_service = RentalService()

    # 1. BASIC FUNCTIONALITY TESTS
    print("1. BASIC FUNCTIONALITY TESTS")
    print("---------------------------")

    # Add vehicles and customers
    print("Adding vehicles:")
    print("Car:", rental_service.add_car("C001", "Toyota", 50.0, 5, "Petrol"))
    print("Electric Car:", rental_service.add_electric_car("E001", "Tesla", 70.0, 5, 85.0, 8.0, 450.0, 10.0))
    print("Bike:", rental_service.add_bike("B001", "Honda", 30.0, 125, True))
    print("Truck:", rental_service.add_truck("T001", "Ford", 100.0, 5.0, True))

    print("\nRegistering customers:")
    print("Customer 1:", rental_service.register_customer("CU001", "John Smith", "555-1234", "john@example.com"))
    print("Customer 2:", rental_service.register_customer("CU002", "Jane Doe", "555-5678", "jane@example.com"))

    print("\nRenting vehicles:")
    print("Rent car by days:", rental_service.rent_vehicle_by_days("C001", "CU001", 3))
    print("Rent bike by hours:", rental_service.rent_vehicle_by_hours("B001", "CU002", 5))

    print("\nReturning vehicles:")
    print("Return car:", rental_service.return_vehicle("C001"))

    # 2. ERROR HANDLING TESTS
    print("\n2. ERROR HANDLING TESTS")
    print("----------------------")


    # Add vehicles and customers for testing
    rental_service.add_car("C001", "Toyota", 50.0, 5, "Petrol")
    rental_service.add_electric_car("E001", "Tesla", 70.0, 5, 85.0, 8.0, 450.0, 10.0)
    rental_service.add_bike("B001", "Honda", 30.0, 125, True)
    rental_service.add_truck("T001", "Ford", 100.0, 5.0, True)
    rental_service.register_customer("CU001", "John Smith", "555-1234", "john@example.com")

    # Test Case 1: Add vehicle with duplicate ID
    print("Test Case 1: Add vehicle with duplicate ID")
    result = rental_service.add_car("C001", "Honda", 55.0, 4, "Diesel")
    print(f"Result: {'Failed as expected' if result == False else 'Error: Allowed duplicate ID'}\n")

    # Test Case 2: Rent non-existent vehicle
    print("Test Case 2: Rent non-existent vehicle")
    result = rental_service.rent_vehicle_by_days("X999", "CU001", 3)
    print(f"Result: {'Failed as expected' if result == False else 'Error: Allowed renting non-existent vehicle'}\n")

    # Test Case 3: Rent to non-existent customer
    print("Test Case 3: Rent to non-existent customer")
    result = rental_service.rent_vehicle_by_days("C001", "X999", 3)
    print(f"Result: {'Failed as expected' if result == False else 'Error: Allowed renting to non-existent customer'}\n")

    # Test Case 4: Rent vehicle twice
    print("Test Case 4: Rent already rented vehicle")
    rental_service.rent_vehicle_by_days("C001", "CU001", 3)  # First rental
    result = rental_service.rent_vehicle_by_days("C001", "CU001", 2)  # Second rental attempt
    print(f"Result: {'Failed as expected' if result == False else 'Error: Allowed renting already rented vehicle'}\n")

    # Test Case 5: Return non-existent vehicle
    print("Test Case 5: Return non-existent vehicle")
    result = rental_service.return_vehicle("X999")
    print(f"Result: {'Failed as expected' if result == False else 'Error: Allowed returning non-existent vehicle'}\n")

    # Test Case 6: Try renting truck by hours (not allowed)
    print("Test Case 6: Rent truck by hours (not allowed)")
    result = rental_service.rent_vehicle_by_hours("T001", "CU001", 5)
    print(f"Result: {'Failed as expected' if result == False else 'Error: Allowed renting truck by hours'}\n")

    print("===== Tests Completed =====")


if __name__ == "__main__":
    main()
