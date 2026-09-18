import csv
import math

# Additional Class Implementation - GameRecord class to encapsulate individual game data
class GameRecord:
    def __init__(self, name, platform, year_of_release, genre, publisher, global_sales, critic_score, developer,
                 rating):
        # Store all game data as private variables for encapsulation
        self.__name = name
        self.__platform = platform
        self.__year_of_release = year_of_release
        self.__genre = genre
        self.__publisher = publisher
        self.__global_sales = global_sales
        self.__critic_score = critic_score
        self.__developer = developer
        self.__rating = rating

    def to_dict(self):
        """Convert the GameRecord object back to dictionary format for compatibility"""
        return {
            'name': self.__name,
            'platform': self.__platform,
            'year_of_release': self.__year_of_release,
            'genre': self.__genre,
            'publisher': self.__publisher,
            'global_sales': self.__global_sales,
            'critic_score': self.__critic_score,
            'developer': self.__developer,
            'rating': self.__rating
        }


class Analytic:
    def __init__(self, filename):
        """Initialize the Analytic class and load CSV data"""
        # Store private variables as required by the assignment
        self.__filename = filename
        self.__data = []  # List to store all valid game records
        self.__headers = []  # List to store CSV column headers
        # Load the CSV file immediately upon initialization
        self.__load_csv(filename)

    # Additional Private Method Implementation - __validate_record method
    def __validate_record(self, values):
        errors = []
        if len(values) != 9:
            return [f"expected 9 fields, got {len(values)}"]

        # Check for empty fields in any column
        for j in range(len(values)):
            if not values[j].strip():
                errors.append(f"index {j} is empty")

        # Only validate data types if no empty fields found
        if not errors:
            # Validate Year_of_Release (index 2) - must be integer and in valid range
            if len(values) > 2:
                try:
                    year = int(values[2])
                    if year < 1950 or year > 2025:
                        errors.append(f"index 2 year out of range")
                except ValueError:
                    errors.append(f"index 2 year is not integer")

            # Validate Global_Sales (index 5) - must be positive float
            if len(values) > 5:
                try:
                    sales = float(values[5])
                    if not math.isfinite(sales) or sales <= 0:
                        errors.append(f"index 5 must be finite and positive")
                except ValueError:
                    errors.append(f"index 5 is not float")

            # Validate Critic_Score (index 6) - must be positive integer
            if len(values) > 6:
                try:
                    score = int(values[6])
                    if score <= 0:
                        errors.append(f"index 6 is not positive")
                except ValueError:
                    errors.append(f"index 6 is not integer")

        return errors

    def __load_csv(self, filename):
        """Private method to load and process CSV file with error handling"""
        with open(filename, newline='', encoding='utf-8-sig') as file, \
                open("errors.txt", "w", encoding="utf-8") as error_file:
            reader = csv.reader(file)
            self.__headers = next(reader, [])
            if not self.__headers:
                return
            if len(self.__headers) != 9:
                raise ValueError("Expected a CSV header with 9 columns")
            for values in reader:
                if not values or all(not value.strip() for value in values):
                    continue
                errors = self.__validate_record(values)
                if errors:
                    error_file.write(f"Line {reader.line_num}: " + ", ".join(errors) + "\n")
                    continue
                game_record = GameRecord(
                    values[0].strip(), values[1].strip(), int(values[2]),
                    values[3].strip(), values[4].strip(), float(values[5]),
                    int(values[6]), values[7].strip(), values[8].strip()
                )
                self.__data.append(game_record.to_dict())

    @property
    def count(self):
        """Return the number of valid records loaded from CSV"""
        return len(self.__data)

    def match(self, name=[], platform=[], year_of_release=[], genre=[], publisher=[], global_sales=[], critic_score=[],
              developer=[], rating=[]):
        """Filter games based on provided criteria and return matching records"""
        result = []

        # Check each game against all provided filter criteria
        for game in self.__data:
            matched = True

            # Apply name filter (OR condition within the list)
            if name and game['name'] not in name:
                matched = False
            # Apply platform filter (OR condition within the list)
            if platform and game['platform'] not in platform:
                matched = False
            # Apply year range filter (between min and max values)
            if year_of_release and len(year_of_release) >= 2:
                if game['year_of_release'] < year_of_release[0] or game['year_of_release'] > year_of_release[1]:
                    matched = False
            # Apply genre filter (OR condition within the list)
            if genre and game['genre'] not in genre:
                matched = False
            # Apply publisher filter (OR condition within the list)
            if publisher and game['publisher'] not in publisher:
                matched = False
            # Apply sales range filter (between min and max values)
            if global_sales and len(global_sales) >= 2:
                if game['global_sales'] < global_sales[0] or game['global_sales'] > global_sales[1]:
                    matched = False
            # Apply critic score range filter (between min and max values)
            if critic_score and len(critic_score) >= 2:
                if game['critic_score'] < critic_score[0] or game['critic_score'] > critic_score[1]:
                    matched = False
            # Apply developer filter (OR condition within the list)
            if developer and game['developer'] not in developer:
                matched = False
            # Apply rating filter (OR condition within the list)
            if rating and game['rating'] not in rating:
                matched = False

            # Add to result if all criteria matched (AND condition between different filters)
            if matched:
                result.append(game)

        return result

    def get_platforms(self):
        """Return list of unique platforms from all games"""
        platforms = set()  # Use set to automatically remove duplicates
        for game in self.__data:
            platforms.add(game['platform'])
        return list(platforms)  # Convert back to list for return

    def get_genres(self):
        """Return list of unique genres from all games"""
        genres = set()  # Use set to automatically remove duplicates
        for game in self.__data:
            genres.add(game['genre'])
        return list(genres)  # Convert back to list for return
