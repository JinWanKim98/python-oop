# Assignment 3 — the design notes I submitted under the code

```
# -------- Test Execution Results -------- 
# Main tests completed
# Error tests completed
# All tests completed

# Additional Private Method Implementation:
# I utilized the __validate_record() private method to keep data validation
# logic separate from the main CSV loading process. The method checks if the fields
# are empty and checks data types like year, sales, and critic score. This method is
# beneficial because it keeps the __load_csv() method clean and readable. It also
# organizes the code
# by having all the validation rules in one location, useful when there are
# data format issues.

# Additional Class Implementation:
# I employed the GameRecord class to store data from each game as objects instead of
# dictionaries exclusively. The class stores all the game data saved with private
# variables and contains a to_dict() method to get the object in dictionary form
# when required.
# This class is also handy in that it follows object-oriented programming principles better
# than simple dictionaries would. It also keeps the code nice and tidy and makes it cleaner
# and easier to add to later if we need to add in more game-related features.
# The GameRecord class does not conflict with the present Analytic class and doesn't
# eliminate any of the original functionality.
```
