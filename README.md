# The year between writing classes and using them

**Four Python assignments from two semesters a year apart (CSIT 121 Object-Oriented Design and
Programming, and a first-semester group assignment before it).**

I put the 2024 one next to the 2025 ones to see what had changed, and the answer was not "I learned
what a class is." I was already writing classes in 2024. Seven of them. What I was not doing was
anything a class is *for*.

| | 2024 · Tour Booking (group) | 2025 · CSIT 121 (solo) |
|---|---|---|
| Classes | **7** | 14 |
| Inheritance | **0** — not one `class X(Y)` | `ABC → Vehicle → Car → ElectricCar`, plus `RentalRecord → Days/Hours` |
| Decorators | **0** | **3 kinds** — `@abstractmethod`, `@property`, `@classmethod` |
| Encapsulation | **0** — no `self.__`, no `self._`, every attribute public | every assignment, two different ways (§3) |
| One shape, one owner | **the same 9-field record defined twice, in two files** | `RentalService` owns the assembly |

---

### 1. Seven classes and nothing holding them together

`Tour` in `TourClasses.py` and `Tours` in `realBookingPart.py` are the same nine fields — tour code,
name, departure date, days, nights, cost per pax, capacity, available, status — declared twice in two
files, in a different order, by two people.

They did not end up the same:

| | `Tour` | `Tours` |
|---|---|---|
| Methods | **7** (`__init__` plus 6) | **1** (`__init__` only) |
| Type conversion | **7** — five in the constructor, two in the seat count | **none** — everything stays a string |
| Behaviour | `seat_booked`, `isOpen`, `hasCapacity`, `displayTourDetails`, getter, setter | none |

So one copy coerces `days` to `int` and the other does not, and whether `available` is a number or the
string `"12"` depends on which file you got your object from. Nothing crashed, because nothing ever
compared them.

**This is what the code remembers about how we worked.** Five of us were registered on the assignment
and four of us wrote code. We did not divide it up by responsibility — we went through it together.
The duplicate happened anyway: the same nine fields were written twice, in two files, and none of us
noticed. Working on a program in the same room is not the same as one person owning a piece of it.
That is not a story I have to tell you — it is sitting in the repository as two class definitions.

The 2025 equivalent is `RentalService`. One class holds the vehicles, the customers and the rental
records, and nothing else constructs them.

---

### 2. What the abstract base class actually forces

```python
class Vehicle(ABC):
    @abstractmethod
    def calculate_rental_cost_by_days(self, days): ...
    @abstractmethod
    def calculate_rental_cost_by_hours(self, hours): ...
```

`Car`, `Bike` and `Truck` each answer those two differently, and `ElectricCar` extends `Car` again.
The point is not that the calculation differs — it did in 2024 too, as a chain of `if` statements on a
type string. The point is that in 2024 **nothing stopped me adding a fourth vehicle and forgetting the
hourly branch.** Here the class will not instantiate.

Five `@abstractmethod`s across two hierarchies: three on `Vehicle` (the two above and `__str__`), two
on `RentalRecord`, which splits into `RentalRecord_Days` and `RentalRecord_Hours`.

```python
def round_to_nearest_5_cent(amount):
    cents = round(amount * 100)
    remainder = cents % 5
    if remainder < 2.5:   cents = cents - remainder
    elif remainder > 2.5: cents = cents + (5 - remainder)
```

That one is a free function on purpose. Rounding to the nearest five cents belongs to Singapore's
cash-payment rule, not to any vehicle, and making it a method would have attached it to the wrong
thing.

The last thing in `notes/02_vehicle_rental.md` is not about my code. The test harness the module
supplied asserts `bike1.__str__() == "[Bike]"` at lines 137–138 — which is not the string
`Bike.__str__()` produces, and the second of the two checks `bike1` again where it means `bike2`.
I wrote both down and said why they were the harness's problem and not the implementation's.
**That file is the module's, so it is not in this repository, and those line numbers point at
something you cannot open here.**

---

### 3. The same idea spelled two ways, and I only worked out why afterwards

Assignments 1 and 3 hide state with a double underscore — `self.__balance`, `self.__name`.
Assignment 2 uses a single one throughout, behind 26 `@property` accessors. Same intent, two
spellings, and for a while I read that as me being inconsistent.

**I did not write down a reason for the underscores at the time.** What I submitted under assignment 2
is in `notes/02_vehicle_rental.md`, and there is nothing about them in it.

Reading it back now, the reason is the inheritance. A double underscore name-mangles: `self.__brand`
inside `Vehicle` becomes `_Vehicle__brand`, and `Car`, which inherits from it, cannot see it.
**Assignment 2 is the only one of the three with a class hierarchy, so it is the only one where the
stronger form is unusable.** Assignment 1 has no hierarchy at all, so `__` is free there, and that is
where it is.

So the inconsistency is not one. It is the hierarchy showing up in the syntax — which I could not
have told you in May and can now.

---

### 4. Validation that stays out of the way

`Analytic.__load_csv()` reads the games file; `Analytic.__validate_record()` decides whether a row is
usable. Keeping them apart is the whole reason the error file works: `GamesSales_Errors.csv` contains
deliberately broken rows, and the loader skips them without a branch of its own.

`GameRecord` is the other half. The rows could have stayed dictionaries — the assignment's interface
returns dictionaries and `to_dict()` converts back for exactly that reason — but a dictionary has no
opinion about what a game record is, and a missing key fails at the point of reading rather than at
the point of loading.

---

### Repository Structure

```
python-oop/
├── 00_first_semester_group/    # 2024 · Tour Booking. Group work — see Provenance
│   ├── ADMIN.py                #   menus
│   ├── realBookingPart.py      #   bookings, travellers, grouping
│   ├── TourClasses.py          #   Tour + TourManagementSystem
│   ├── Cancellation_penalties.py  Discount_scheme.py
│   └── bookings.txt  listTours.txt  cancellation_penalties.txt  discount_schemes.txt
├── 01_bank_accounts/           # 2025 A1 · Customer + BankAccount, composition
├── 02_vehicle_rental/          # 2025 A2 · ABC, four-level chain, @property
├── 03_games_sales/             # 2025 A3 · GameRecord + Analytic over a CSV
├── notes/                      # what I submitted underneath each program (see below)
└── README.md
```

Each 2025 assignment was submitted as a **single `.txt` file**: the program, and below it a block of
test output or design commentary. The code is in the numbered folders and that trailing block is in
`notes/`, unchanged. They are separated here because the file as submitted does not run — the notes
sit outside any string literal, and assignment 2's are wrapped in typographic quotes.

### How to Run

```bash
git clone https://github.com/JinWanKim98/python-oop.git
cd python-oop
python3 01_bank_accounts/bank_accounts.py
python3 02_vehicle_rental/vehicle_rental.py
cd 00_first_semester_group && python3 ADMIN.py     # reads the .txt files beside it
```

The 2024 program reads and writes the four `.txt` files in its own folder, so it has to be run from
inside that directory. Assignment 3 expects `GamesSales_2.csv` and `GamesSales_Errors.csv`, which are
the module's data files and are not included.

### Provenance

`01`, `02` and `03` are my own work, submitted solo for CSIT 121 at UOW (SIM Singapore) in 2025.

One edit was made to the submitted files: the single saved booking in `00`'s data had a teammate's
first name in it, and I replaced it with my own. The passport and contact numbers in that row were
already dummy values. Nothing else in any of the four programs was changed.

`00_first_semester_group/` is different, and the comparison this README is built on does not work
unless that is said plainly. It was a group assignment the year before — **a five-person group in
which four of us wrote code.** I am not claiming it as mine. It is here as the earlier measurement,
and what section 1 reads off it is a fact about how the group worked, not about any individual.

The `Analytic` class signature — including `match()`'s keyword filters — came from the assignment
skeleton. The file loading, validation, error-row handling and the matching logic inside that
signature are mine, as is `GameRecord`, which the skeleton does not define.

### Limitations

- **The comparison is between a group assignment and solo ones.** Some of the 2024 duplication is what
  happens when people split a program by file, not what happens when one person does not know about
  inheritance. Both readings are true and the repository cannot separate them.
- **A year is not the only variable.** The 2025 assignments were set by a course that taught abstract
  base classes and properties directly. The 2024 one was not. I did not reach for `ABC` because I grew;
  I reached for it because it had been put in front of me and the assignment asked for it.
- **Nothing here is tested in the sense that word usually means.** The `notes/` blocks are runs I did
  by hand and pasted in. There is no test file in this repository that a reader can execute.
- **`00`'s data files are the state the program was last left in.** They are small and readable, and
  they are not a fixture anyone designed.
