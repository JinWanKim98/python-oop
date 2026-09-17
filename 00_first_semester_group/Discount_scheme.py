class DiscountScheme:
    def __init__(self, group_size, discount):
        self.group_size = group_size
        self.discount = discount

def save_to_file(schemes):
    with open("discount_schemes.txt", "w") as file:
        for scheme in schemes:
            file.write(f"{scheme.group_size},{scheme.discount}\n")

def load_from_file():
    schemes = []
    try:
        with open("discount_schemes.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                group_size, discount = line.strip().split(",")
                schemes.append(DiscountScheme(int(group_size), float(discount)))
    except FileNotFoundError:
        print("No existing discount schemes file found. Starting with an empty list.")
    return schemes

def add_line(schemes):
    print("Adding a new line...")
    group_size = int(input("Enter group size: "))
    discount = float(input("Enter discount percentage: "))

    # Perform validation
    if discount > 100:
        print("Error: Discount percentage cannot be greater than 100%")
        return
    for scheme in schemes:
        if scheme.group_size >= group_size and scheme.discount < discount:
            print("Warning: Adding this line may cause irregular behavior.")

    schemes.append(DiscountScheme(group_size, discount))
    save_to_file(schemes)
    print("New line added successfully!")

def update_line(schemes):
    print("Updating a line...")
    group_size = int(input("Enter group size to update: "))
    discount = float(input("Enter new discount percentage: "))

    # Perform validation
    if discount > 100:
        print("Error: Discount percentage cannot be greater than 100%")
        return
    for scheme in schemes:
        if scheme.group_size == group_size and scheme.discount < discount:
            print("Warning: Updating this line may cause irregular behavior.")

    for scheme in schemes:
        if scheme.group_size == group_size:
            scheme.discount = discount
            save_to_file(schemes)
            print("Line updated successfully!")
            return
    print("Error: Line with group size", group_size, "not found.")

def remove_line(schemes):
    print("Removing a line...")
    if len(schemes) == 0:
        print("Error: There are no lines to remove.")
        return

    group_size = int(input("Enter group size to remove: "))
    for i, scheme in enumerate(schemes):
        if scheme.group_size == group_size:
            schemes.pop(i)
            save_to_file(schemes)
            print("Line removed successfully!")
            return
    print("Error: Line with group size", group_size, "not found.")

def main_menu():
    schemes = load_from_file()  # Load existing discount schemes
    while True:
        print("\n--- Discount Schemes Menu ---")
        print("a. Add new line")
        print("b. Update line")
        print("c. Remove line")
        print("m. Back to main menu")
        option = input("Enter option: ")

        if option == 'a':
            add_line(schemes)
        elif option == 'b':
            update_line(schemes)
        elif option == 'c':
            remove_line(schemes)
        elif option == 'm':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()
