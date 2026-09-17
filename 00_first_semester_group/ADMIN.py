from realBookingPart import BookingManager
from TourClasses import TourManagementSystem
def main():
    booking_manager = BookingManager()
    tour_manager = TourManagementSystem()
    while True:
        print("^^^^^ BESG ^^^^")
        print("1. Tour Admin")
        print("2. Tour Booking")
        print("0. Exit")
        option = input("Enter option: ")

        if option == "1":
            tour_admin_menu(tour_manager)
        elif option == "2":
            tour_booking_menu(booking_manager)
        elif option == "0":
            break
        else:
            print("Invalid option. Please try again.")
            continue

def tour_admin_menu(tour_manager):
    while True:
        print("<<<< Tour Admin >>>>")
        print("a. List Tours")
        print("b. Setup Tour")
        print("c. Update Tour")
        print("d. Delete Tour")
        print("m. Back to main menu")
        option = input("Enter option: ")

        if option == "a":
            tour_manager.listTours()
        elif option == "b":
            tour_manager.setUpTour()
        elif option == "c":
            tour_manager.updateTour()
        elif option == "d":
            tour_manager.deleteTour()
        elif option == "m":
            break
        else:
            print("Invalid option. Please try again.")
            continue

def tour_booking_menu(booking_manager):
    while True:
        print(">>>> Tour Booking <<<<")
        print("a. Create Booking")
        print("b. Cancel Booking")
        print("c. Search Booking")
        print("d. Booking Report")
        print("m. Back to main menu")
        option = input("Enter option: ")

        if option == "a":
            booking_manager.create_booking()
        elif option == "b":
            booking_manager.cancel_booking()
        elif option == "c":
            booking_manager.search_booking()
        elif option == "d":
            booking_manager.booking_report()
        elif option == "m":
            break
        else:
            print("Invalid option. Please try again.")
            continue



if __name__ == "__main__":
        main()