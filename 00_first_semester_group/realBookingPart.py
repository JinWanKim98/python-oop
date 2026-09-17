
from datetime import datetime
from TourClasses import Tour


class Tours:
    def __init__(self,
                 tourName="",
                 departureDate="",  # yyyy-mm-dd HH:MM
                 tourCode="",
                 days=0,
                 nights=0,
                 costPerPax=0.0,
                 capacity=0,
                 available=0,
                 status="Open"
                 ):
        self.tourName = tourName
        self.departureDate = departureDate
        self.tourCode = tourCode
        self.days = days
        self.nights = nights
        self.costPerPax = costPerPax
        self.capacity = capacity
        self.available = available
        self.status = status




class Booking:
    def __init__(self, booking_id, tour_code, traveler_details):
        self.booking_id = booking_id
        self.tour_code = tour_code
        self.traveler_details = traveler_details

class BookingManager:
    def __init__(self):
        self.bookings = []
        self.current_booking_id = 1000


    def generate_booking_id(self):
        with open("bookings.txt", 'r') as file:
            for line in file:
                index = line.strip().split(',')
                if index and index[0]:  # Check if index is not empty and the first element is not empty
                    self.current_booking_id = int(index[0])
                    self.current_booking_id += 1
        return str(self.current_booking_id).zfill(4)
        
    def update_tours_capacity(self, tour_code, num_travelers):
        with open('listTours.txt', 'r+') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                tour_data = line.strip().split(',')
                if tour_data[0] == tour_code and tour_data[-1] == 'Open':
                    tour_data[7] = str(int(tour_data[6]) - num_travelers)
                    lines[i] = ','.join(tour_data) + '\n'
                    file.seek(0)
                    file.writelines(lines)
                    break    

    def create_booking(self):
        
        def divide_travelers(travelers):
            individuals = []
            groups = []

            for traveler in travelers:
                if traveler['group'] == 'yes':
                    groups.append(traveler)
                else:
                    individuals.append(traveler)
            return individuals, groups

        print()

        with open('listTours.txt', "r") as file:
            for line in file:
                tour_data = line.strip().split(',')
                if tour_data[-1] == 'Open':
                    print("Tour Code: ", tour_data[0], "Tour Name: ", tour_data[1], "Departure Date: ",
                          tour_data[2])
                    print("Days: ", tour_data[3], "Nights: ", tour_data[4], "\tCost Per Pax: ", tour_data[5],
                          "\tAvailable Seats: ", tour_data[7])
                    print("Status: ", tour_data[8])
                    print()


        def get_tour_info_by_code(tour_code):
            with open('listTours.txt', 'r') as file:
                for line in file:
                    tour_info = line.strip().split(',')
                    if tour_info[0] == tour_code:
                        return tour_info
        
        bookings_txt = 'bookings.txt'
        def check_passport_numbers_in_file(bookings_txt, new_passport_number):
            with open(bookings_txt, 'r') as file:
                for line in file:
                    booking_info = line.strip().split(',')
                    if booking_info[3] == new_passport_number:
                        return False
            return True  
            
            
        tour_code_input = input("Enter Tour Code: ")
        tour_info = get_tour_info_by_code(tour_code_input)
        if tour_info:
            print("Tour Information:")
            print("Tour Code:", tour_info[0])
            print("Tour Name:", tour_info[1])
            print("Date:", tour_info[2])
            print("Remaining Seats:", tour_info[7])
            print("costPerPax:", tour_info[5])
            print()
        
            num_travelers = int(input("Enter number of travelers: "))
            travelers = []
            self.discount_cost = float(float(tour_info[5]) * self.discount(num_travelers))
            costPerPax = float(float(tour_info[5]) - self.discount_cost)
            first_traveler_age_ok = False
            group_member_age_ok = False            
        
            for i in range(num_travelers):
                Passno = input("Enter Passport Number: ")
                if not check_passport_numbers_in_file('bookings.txt', Passno):
                    print("Cannot create booking: Passport number is already used.")
                    return              
                name = input("Enter Name: ")
                dob_str = input("Enter DOB (yyyy-mm-dd): ")
                dob = datetime.strptime(dob_str, "%Y-%m-%d")
                age = int((datetime.now() - dob).days / 365)
                group = input("Is this traveler part of a group? (yes/no): ") 
                if i == 0:
                    if age >= 18:
                        first_traveler_age_ok = True
                    elif group == 'yes':
                        pass
                    else:
                        print("Unable to create booking. Age requirement not met.")
                        return  # Exit if the first traveler is under 18 and not part of a group
                    
                elif group == 'yes' and age >= 21:
                    group_member_age_ok = True
                    
                elif group == 'no' and age < 18:
                    print("Unable to create booking. Age requirement not met.")
                    return  # Exit if the age requirement is not met for subsequent travelers
                else:
                    # Continue collecting traveler information...
                    pass                                
                contact = input("Enter Contact: ")
                booking_date = datetime.now()
                travelers.append({'tour_code':tour_code_input, 'Passport':Passno, 'name':name, 'age':age, 'contact':contact,
                                  'group':group, 'Cost Per Pax' :costPerPax, 'booking_date' :booking_date.strftime('%Y-%m-%d')})
                
            if not first_traveler_age_ok and not group_member_age_ok:
                print("Unable to create booking. Age requirement not met.")
                return                
            
            # divide
            individuals, groups = divide_travelers(travelers)
        
            for person in individuals:
                booking_id = self.generate_booking_id()
                booking = Booking(booking_id, person['tour_code'], person)
                self.bookings.append(booking)
                print("Individual booking is added. See confirmatin below:")
                print("Booking ID:", booking_id, person)
        
            # Writing individual travelers to a text file
            with open('bookings.txt', 'a') as file:
                for person in individuals:
                    file.write(
                        f"{booking_id},{person['group']},{person['tour_code']},{person['Passport']},{person['name']},{person['age']},{person['contact']},{person['booking_date']},{person['Cost Per Pax']}\n")
        
        
        
            group_booking_id = self.generate_booking_id()
            group_travelers_list = []  # List of group0
            for group in groups:
                booking = Booking(group_booking_id, group['tour_code'], group)
                self.bookings.append(booking)
                group_travelers_list.append(group)  # add group_travelers
        
            # Writing group travelers to a text file
            with open('bookings.txt', 'a') as file:
                for group in groups:
                    file.write(
                        f"{group_booking_id},{group['group']},{group['tour_code']},{group['Passport']},{group['name']},{group['age']},{group['contact']},{group['booking_date']},{group['Cost Per Pax']},\n")
        
            # Display group
        
        
            self.display_group_booking(group_booking_id)
            
            self.update_tours_capacity(tour_code_input, len(individuals) + len(groups))
        else:
            print("Tour with the entered code was not found.")

    def group_travelers_by_booking_id(self):
        grouped_travelers = {}
        for booking in self.bookings:
            if booking.booking_id not in grouped_travelers:
                grouped_travelers[booking.booking_id] = []
            grouped_travelers[booking.booking_id].append(booking.traveler_details)
        return grouped_travelers
    
    
    def display_group_booking(self, group_booking_id):
        grouped_travelers = self.group_travelers_by_booking_id()
        printed = False
        for booking_id, traveler_list in grouped_travelers.items():
            if booking_id == group_booking_id and not printed:  # Group
                print("Group booking is added. See confirmation below:")
                print("Booking ID:", booking_id)
                for traveler in traveler_list:
                    print(traveler,'\n')
                    print("You got {:.2f} discount for each.".format(self.discount_cost))

                printed = True
            else:
                pass

    def discount(self, num_travelers):
        if num_travelers == 2:
            discount_percentage = 0.10
        elif num_travelers == 4:
            discount_percentage = 0.15
        elif num_travelers == 8:
            discount_percentage = 0.20
        else:
            discount_percentage = 0
    
        return discount_percentage


    
    

    #cancel booking
    
    def cancel_booking(self):
        booking_id= None
        booking_date = None
        tour_code = None
        
        manager = BookingManager()
        booking_id = input("Enter the booking ID to cancel: ")
        
        with open("bookings.txt", "r") as id_file:
            for line in id_file:
                index = line.strip().split(',')
                if index[0] == booking_id:
                    booking_date = datetime.strptime(index[7],'%Y-%m-%d').strftime('%Y-%m-%d')
                    tour_code = index[2]
                    break
                
            if booking_id and tour_code is None:
                print( "Booking ID or tour code is not found.")

        with open("listTours.txt", "r") as status_file:
            for line in status_file:
                index = line.strip().split(',')
                if index[0] == tour_code:
                    if index[-1].strip().lower() == "open":
                        cancel_date = datetime.now().strftime('%Y-%m-%d')
                        if cancel_date == booking_date:
                            self.remove_booking_from_file("bookings.txt", booking_id)
                            print( "Booking canceled successfully" )                       
                        else:
                            penalty_fee = self.penalty(booking_id)
                            total_cost = self.calculate_total_cost(booking_id)
                            self.remove_booking_from_file("bookings.txt", booking_id)
                            print (f"Cancellation penalty fee: {penalty_fee}. Total cost for travelers: {total_cost}")
                        
        return "Booking not found or status is not open"
    
    def remove_booking_from_file(self, file_path, booking_id):
        with open(file_path, "r") as file:
            lines = file.readlines()
    
        updated_lines = [line for line in lines if booking_id not in line.strip().split(',')]
        
        with open(file_path, "w") as file:
            file.writelines(updated_lines)
    
    def calculate_total_cost(self, booking_id):
        num_travelers = 0
        tour_cost = None
        with open("bookings.txt", "r") as id_file:
            for line in id_file:
                index = line.strip().split(',')
                if index[0] == booking_id:
                    num_travelers += 1
                    tour_cost = float(index[8])
    
        if tour_cost is not None:
            total_cost = num_travelers * tour_cost
            print( total_cost)
        else:
            print( "Tour cost not found for the booking ID.")
    
    def penalty(self, booking_id):
        difference_days = (datetime.now() - datetime.strptime(self.get_booking_date(booking_id), '%Y-%m-%d')).days
        if difference_days <= 7:
            cancellation_fee_percentage = 0.3 
        elif 21 <= difference_days <= 45:
            cancellation_fee_percentage = 0.6
        else:
            cancellation_fee_percentage = 0.9
            
        cancellation_fee = cancellation_fee_percentage * self.get_tour_cost(booking_id)
        print(cancellation_fee)
    
    def get_booking_date(self, booking_id):
        with open("bookings.txt", "r") as id_file:
            for line in id_file:
                index = line.strip().split(',')
                if index[0] == booking_id:
                    return datetime.strptime(index[7], '%Y-%m-%d').strftime('%Y-%m-%d')
    
        return None
    
    def get_tour_cost(self, booking_id):
        with open("bookings.txt", "r") as id_file:
            for line in id_file:
                index = line.strip().split(',')
                if index[0] == booking_id:
                    return float(index[8])
    
        return None

    #search booking

    def search_booking(self):
        search_booking_id = input("Enter Booking ID to search: ")
    
        found = False
        general_info_displayed = False
    
        try:
            with open('bookings.txt', 'r') as file:
                for line in file:
                    booking_info = line.strip().split(',')
                    if booking_info and len(booking_info) >= 9 and booking_info[0] == search_booking_id:
                        found = True
                        if not general_info_displayed:
                            print("Booking ID:", booking_info[0])
                            print("Tour Code:", booking_info[2])
                            print("Departure Date:", booking_info[7])
                            print("Total Cost:", booking_info[8])
                            print()
                            print("Passport\t Name \t Age \t Contact")
                            print("-" * 50)
                            general_info_displayed = True
    
                        print(booking_info[3],"\t ",booking_info[4],"\t ",booking_info[5],"\t ",booking_info[6])
    
        except FileNotFoundError:
            print("Booking file not found.")
    
        if not found:
            print("Booking with the entered ID was not found.")

     
    
    def booking_report(self):

        tour_codes_input = input("Enter Tour Codes separated by commas: ")
        tour_codes = [code.strip() for code in tour_codes_input.split(",")]

        # Read bookings from file and filter based on provided Tour Codes
        with open("bookings.txt", "r") as file:
            # Initialize a flag to track if any booking is found
            booking_found = False

            for line in file:
                booking_info = line.strip().split(',')
                if len(booking_info) >= 9 and booking_info[2] in tour_codes:
                    tour_code = booking_info[2]

                    # Print tour code and departure information only once
                    if not booking_found:
                        print(f"Code: {tour_code} Departure: 20-May-2024 8:30")
                        print(f"Capacity: 12 Available: 9 Status: Open")
                        print("ID \t Passport \t Name \t Age \t Contact")
                        print("-" * 60)
                        booking_found = True

                    # Print booking details
                    booking_id = booking_info[0]
                    passport = booking_info[3]
                    name = booking_info[4]
                    age = booking_info[5]
                    contact = booking_info[6]

                    print(f"{booking_id} \t {passport} \t {name} \t {age} \t {contact}")

        # Check if any booking is found, if not, print a message
        if not booking_found:
            print("No bookings found for the provided tour codes.")


