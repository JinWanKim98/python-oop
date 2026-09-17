class CancellationPenalty:
    def __init__(self, days_prior, penalty_percentage):
        self.days_prior = days_prior
        self.penalty_percentage = penalty_percentage

def save_penalties_to_file(penalties):
    with open("cancellation_penalties.txt", "w") as file:
        for penalty in penalties:
            file.write(f"{penalty.days_prior},{penalty.penalty_percentage}\n")

def load_penalties_from_file():
    penalties = []
    try:
        with open("cancellation_penalties.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                days_prior, penalty_percentage = line.strip().split(",")
                penalties.append(CancellationPenalty(int(days_prior), float(penalty_percentage)))
    except FileNotFoundError:
        print("No existing cancellation penalties file found. Starting with an empty list.")
    return penalties

def add_penalty(penalties):
    print("Adding a new line...")
    days_prior = int(input("Enter days prior to event: "))
    penalty_percentage = float(input("Enter penalty percentage: "))

    # Perform validation
    if penalty_percentage > 100:
        print("Error: Penalty percentage cannot be greater than 100%")
        return

    penalties.append(CancellationPenalty(days_prior, penalty_percentage))
    save_penalties_to_file(penalties)
    print("New line added successfully!")

def update_penalty(penalties):
    print("Updating a line...")
    days_prior = int(input("Enter days prior to event to update: "))
    penalty_percentage = float(input("Enter new penalty percentage: "))

    # Perform validation
    if penalty_percentage > 100:
        print("Error: Penalty percentage cannot be greater than 100%")
        return

    for penalty in penalties:
        if penalty.days_prior == days_prior:
            penalty.penalty_percentage = penalty_percentage
            save_penalties_to_file(penalties)
            print("Line updated successfully!")
            return
    print("Error: Line with days prior", days_prior, "not found.")

def remove_penalty(penalties):
    print("Removing a line...")
    if len(penalties) == 0:
        print("Error: There are no lines to remove.")
        return

    days_prior = int(input("Enter days prior to event to remove: "))
    for i, penalty in enumerate(penalties):
        if penalty.days_prior == days_prior:
            penalties.pop(i)
            save_penalties_to_file(penalties)
            print("Line removed successfully!")
            return
    print("Error: Line with days prior", days_prior, "not found.")

def main_menu():
    penalties = load_penalties_from_file()  # Load existing cancellation penalties
    while True:
        print("\n--- Cancellation Penalties Menu ---")
        print("a. Add new line")
        print("b. Update line")
        print("c. Remove line")
        print("m. Back to main menu")
        option = input("Enter option: ")

        if option == 'a':
            add_penalty(penalties)
        elif option == 'b':
            update_penalty(penalties)
        elif option == 'c':
            remove_penalty(penalties)
        elif option == 'm':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()
