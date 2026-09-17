# Assignment 2 — the test run I submitted under the code

```
“””
Results for functionality and errors

===== Vehicle Rental System Tests =====

1. BASIC FUNCTIONALITY TESTS
---------------------------
Adding vehicles:
Car: True
Electric Car: True
Bike: True
Truck: True

Registering customers:
Customer 1: True
Customer 2: True

Renting vehicles:
Rent car by days: True
Rent bike by hours: True

Returning vehicles:
Return car: True

2. ERROR HANDLING TESTS
----------------------
Test Case 1: Add vehicle with duplicate ID
Result: Failed as expected

Test Case 2: Rent non-existent vehicle
Result: Failed as expected

Test Case 3: Rent to non-existent customer
Result: Failed as expected

Test Case 4: Rent already rented vehicle
Result: Failed as expected

Test Case 5: Return non-existent vehicle
Result: Failed as expected

Test Case 6: Rent truck by hours (not allowed)
Result: Failed as expected

===== Tests Completed =====
“””

“””
Results for assignment2_Testing_Student.py

Test Car pass
Test ElectricCar pass
Test Bike pass
Test Truck pass
Test Customer pass
Test rental_by_days pass
Test rental_by_hours pass
“””

"""
Additional Note:

The assignment2_Testing_Student.py file contains specific errors at lines 137-138:

1. Line 137: "bike1.__str__() == "[Bike]"" - This is incorrect. It should be an assertion and the expected output doesn't match actual Bike.__str__() format.

2. Line 138: Same error as above, and it tests bike1 again instead of testing bike2.

These test file errors do not reflect issues in my implementation. My code correctly implements the Bike class with proper __str__() method and passes all functionality requirements.
```
