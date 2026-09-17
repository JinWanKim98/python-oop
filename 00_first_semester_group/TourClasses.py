from datetime import datetime

# Tour class
class Tour:
    #Initialize Tour class attributes
    def __init__(self,
                 tourCode="",
                 tourName="",
                 departureDate="",  #yyyy-mm-dd HH:MM
                 days=0,
                 nights=0,
                 costPerPax=0.0,
                 capacity=0,
                 available=0,
                 status="Open"
                 ):
        self.tourCode = tourCode
        self.tourName = tourName
        self.departureDate = departureDate
        self.days= int(days)
        self.nights= int(nights)
        self.costPerPax= float(costPerPax)
        self.capacity= int(capacity)
        self.available = int(available)
        self.status= status


    def seat_booked(self, tourCode):
        with open("listTours.txt" , 'r') as file:
            for line in file:
                index = line.strip().split(',')
                if index[0] == tourCode:
                    available = int(index[6]) - int(index[7])
                    return available
            return None
                    
        
        
            
        
                
    # Function to display details of tours
    def displayTourDetails(self):
        print("Tour Code:", self.tourCode)
        print("Tour Name:", self.tourName)
        print("Departure Date:", self.departureDate)
        print("Days:", self.days)
        print("Nights:", self.nights)
        print("Cost per pax: $", self.costPerPax)
        print("Capacity:", self.capacity)
        print("Status:", self.status)
        print("Seats Booked:", self.seat_booked(self.tourCode))
        print()

    def isOpen(self):
        return self.status == "Open"

    def hasCapacity(self):
        return self.available > 0


    def getTourName(self):
        return self.tourName


    def setTourName(self, tourName):
        self.tourName = tourName


    

# Tour Management System class
class TourManagementSystem:
    # Initialize tours list and load tours data from a file
    def __init__(self):
        self.tours = []
        self.loadToursfromFile()

    # Load tours from listTours.txt file and append these into self.tours list
    def loadToursfromFile(self):
        with open("listTours.txt", "r") as file:
            for line in file:
                tourDetails = line.strip().split(",")
                tour = Tour(*tourDetails)
                self.tours.append(tour)
                


    # Write each tour from self.tours list to listTours.txt file to keep data updated
    def saveToursToFile(self):
        with open("listTours.txt", "w") as file:
            for tour in self.tours:
                file.write(",".join([tour.tourCode, tour.tourName, tour.departureDate, str(tour.days), str(tour.nights), str(tour.costPerPax), str(tour.capacity), str(tour.available), tour.status]) + "\n")

    # Display the details of each tour in self.tours list
    def listTours(self):
        for tour in self.tours:
            print()
            tour.displayTourDetails()
            print()

    # Set up new Tour and append that into both self.tours list and listTours.txt file
    def setUpTour(self):
        tourName = input("Enter Tour Name: ")

        departureDate = input("Enter Departure Date (yyyy-mm-dd HH:MM) : ")
        while True:
            try:
                datetime.strptime(departureDate, '%Y-%m-%d %H:%M') # CHECK if departureDate is in correct format or not
                break
            except ValueError:
                print("Date Format is Invalid. Please enter again in the format (yyyy-mm-dd HH:MM).") # DISPLAY appropriate error message to input departureDate again when it is in wrong format
                departureDate = input("Enter Departure Date (yyyy-mm-dd HH:MM)")

        tourCode = input("Enter Tour Code (XXX-YYMMDD) ")
        days = int(input("Enter Days: "))
        nights = int(input("Enter Nights: "))
        while ( days - nights) > 1: # CHECK if the difference between days and nights is greater than 1 or not
            print("Difference between Days and Nights should not be greater than 1.") # IF it is greater than 1, DISPLAY appropriate error message.
            days = int(input("Enter Days: "))
            nights = int(input("Enter Nights: "))

        costPerPax = float(input("Enter Cost Per Pax: "))
        capacity = int(input("Enter Capacity: "))
        available = capacity
        status = "Open" # SET status = Open as default
        newTour = Tour(tourCode, tourName, departureDate, days, nights, costPerPax, capacity, available, status) # CREATE a new instance of the Tour class using Inputs from above
        self.tours.append(newTour) # Append that new instance into self.tours list
        self.saveToursToFile() # Call saveToursToFile function to keep the data updated in listTours.txt as well

    # Update Tour Function to update the details of desired tour from existing list of tours
    def updateTour(self):
        tourCode = input("Enter Tour Code to update: ")
        found = False # SET found = False
        for tour in self.tours: # Iterate each tour in self.tours
            if tour.tourCode == tourCode: # CHECK the user input of tourCode matches with each tour code in self.tours list
                found = True # If it is matched, SET found = True
                print()
                tour.displayTourDetails() # Call displayTourDetails function to display the details of the found tour
                available = int(tour.capacity - tour.available)
                if available != 0: # Check available is greater than 0 or not
                    print("You can't update tour since seats have already been booked.") # If it is greater than 0, DISPLAY appropriate message to let user know that tour can't be updated.
                    return
                else:
                    print("Tour Code can't be modified or changed.") # If it is not greater than 1, warn user that Tour Code can't be changed before user proceeds to update details of the tour
                    print()
                    newDepatureDate = input("Enter new Departure Date (yyyy-mm-dd HH:MM) : ")
                    while True:
                        try:
                            datetime.strptime(newDepatureDate, '%Y-%m-%d %H:%M') # CHECK if newDepartureDate is in correct format or not
                            break
                        except ValueError:
                            print("Date Format is Invalid. Please enter again in the format (yyyy-mm-dd HH:MM).") # DISPLAY appropriate error message to get newDepartureDate from user again
                            newDepatureDate = input("Enter new Departure Date (yyyy-mm-dd HH:MM) : ")

                    newDays = int(input("Enter new Days: "))
                    newNights = int(input("Enter new Nights: "))
                    while ( newDays - newNights) > 1: # CHECK if the difference between newDays and newNights is greater than 1 or not
                        print("Difference between Days and Nights should not be greater than 1.") # IF it is greater than 1, DISPLAY appropriate error message.
                        newDays = int(input("Enter new Days: "))
                        newNights = int(input("Enter new Nights: "))

                    newCostPerPax = float(input("Enter new Cost Per Pax: "))
                    newCapacity = int(input("Enter new Capacity: "))
                    newseatsBooked = newCapacity
                    while newCapacity < available: # Below code will be executed while newCapacity is less than available
                        print("Updated Capacity can't be less than the number of seats booked.") # Warn user that newCapacity can't be less than available
                        newCapacity = int(input("Enter new Capacity: "))
                        
                    newStatus = input("Enter new Status (Open/Closed): ").capitalize() # GET newStatus from user and capitalize the first character of the string to prepare for upcoming condition check
                    while newStatus not in ["Open", "Closed"]: # Below code will be executed while newStatus is neither Open nor Closed.
                        print("Updated Status is Invalid. Please enter either 'Open' or 'Closed'.")
                        newStatus = input("Enter new Status (Open/Closed): ").capitalize()

                    # Update the found tour's attributes with new attributes
                    tour.departureDate = newDepatureDate
                    tour.days = newDays
                    tour.nights = newNights
                    tour.costPerPax = newCostPerPax
                    tour.capacity = newCapacity
                    tour.available = newseatsBooked
                    tour.status = newStatus
                    self.saveToursToFile() # Call saveToursToFile function to keep the data updated in listTours.txt as well
                    print("Tour details updated successfully.")
                    return
        # If tour is not found, below code will be executed
        if not found:
            print("Tour with Tour Code you provided is not found.")

    # GET Tour Code from user and delete the tour that has the tour code as user provided
    def deleteTour(self):
        target = input("Enter Tour Code to delete: ")
        for tour in self.tours: # Iterate each tour in self.tours list
            if tour.tourCode == target: # CHECK the user input of tourCode matches with each tour code in self.tours list
                print()
                tour.displayTourDetails()  # Call displayTourDetails function to display the details of the found tour
                print()
                available = int(tour.capacity - tour.available)
                # If available is greater than 0, DISPLAY appropriate error message. Otherwise, remove the found tour from self.tours list and listTours.txt file
                if available > 0:
                    print("You can't delete this tour since seats have already been booked.")
                    return
                else:
                    print("Tour is successfully deleted.")
                    self.tours.remove(tour) # Remove the found tour from self.tours list
                    self.saveToursToFile() # Call saveToursToFile function to keep the data updated in listTours.txt as well
                    return
        print("Tour with Tour Code you provided is not found.")

















# Main Function
# from FinalBooking import BookingManager
# if __name__ == "__main__":
#     tourSystem= TourManagementSystem
#     # bookingSystem = BookingManager()
#     tourSystem.run()
#     bookingSystem.run()