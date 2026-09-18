# Python OOP — coursework across two semesters

Four assignments showing how my use of classes changed between a 2024 group tour-booking project and three individual CSIT 121 assignments in 2025 at UOW (SIM Singapore).

## Tech stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)

Standard-library Python, including `abc`, `csv` and `unittest`; no external packages are required.

## What to read

| Folder | Work | Main idea |
|---|---|---|
| `00_first_semester_group/` | Group tour booking | Classes, menus and file-based storage; an earlier example with duplicated record definitions |
| `01_bank_accounts/` | Individual | Customer/account composition and balance operations |
| `02_vehicle_rental/` | Individual | Abstract classes, inheritance, properties and rental calculations |
| `03_games_sales/` | Individual | CSV validation and filtering through `GameRecord` and `Analytic` |

The tour project defines similar nine-field records in `TourClasses.py` and `realBookingPart.py`, with different conversion and behaviour. The later rental assignment centralises vehicles, customers and rentals in `RentalService`. This is a useful example of responsibility and consistency, although the assignments had different requirements and one was group work.

`Vehicle` and `RentalRecord` define abstract methods. Concrete classes must implement those methods before they can be instantiated. The rental code also uses single-underscore attributes and properties. The bank and games assignments use double underscores: Python name-mangles these to reduce accidental name collisions, rather than making them inaccessible to subclasses. Either convention can be used with inheritance.

## Run

Python 3.11 was used for the portfolio checks; these assignments use the standard library.

```bash
python3 02_vehicle_rental/vehicle_rental.py
python3 -m unittest discover -s tests -v
cd 00_first_semester_group
python3 ADMIN.py
```

The tour application reads and writes the text files in its own directory. Use a copy if you want to keep the supplied state. The bank file defines classes; running it directly does not print a demonstration.

The games module needs a nine-column CSV in this order: name, platform, release year, genre, publisher, global sales, critic score, developer, rating. Course data files are not included. The automated test constructs a small temporary CSV, including quoted commas, short/long rows and invalid sales values.

## Portfolio maintenance

The games loader now uses `csv.reader`, rejects rows with the wrong field count, and rejects non-finite sales values. Invalid rows are logged to `errors.txt` and skipped. The original assignment's 1950–2025 release-year range and positive-sales rule remain; this is not a general current-games data importer.

The new regression test checks these fixes without requiring the course fixtures. Other programs retain their coursework implementations. The original submitted commentary and example output are in `notes/`; they describe the submission rather than the later fixes.

## Contribution and limits

The three 2025 assignments were individual work. The 2024 tour application was a five-person group assignment with four coding contributors; it is included as group work, not claimed as solely mine. A saved example booking was previously anonymised with my name and dummy contact details.

The `Analytic` interface, including the keyword filters in `match`, came from the assignment skeleton. The loading, validation, filtering and added `GameRecord` implementation were my coursework contribution. Tests cover the repaired CSV behaviour, not every path in all four programs. The instructor's rental test harness and games datasets are not included.
