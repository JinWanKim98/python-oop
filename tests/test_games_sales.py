import csv
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('games', Path(__file__).resolve().parents[1] / '03_games_sales/GamesSalesAnalytic.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class GamesSalesTests(unittest.TestCase):
    def test_csv_quoting_invalid_rows_and_filtering(self):
        with tempfile.TemporaryDirectory() as temp:
            original = os.getcwd()
            try:
                os.chdir(temp)
                valid = ['Game, Part II', 'PC', '2020', 'Action', 'Publisher', '1.5', '80', 'Studio', 'T']
                with open('games.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['name', 'platform', 'year', 'genre', 'publisher', 'sales', 'score', 'developer', 'rating'])
                    writer.writerow(valid)
                    writer.writerow(['short', 'PC'])
                    writer.writerow(valid + ['extra'])
                    for value in ['NaN', 'inf', '-1', 'invalid']:
                        row = valid.copy(); row[5] = value; writer.writerow(row)
                data = module.Analytic('games.csv')
                self.assertEqual(data.count, 1)
                self.assertEqual(data.match(platform=['PC'], year_of_release=[2019, 2021])[0]['name'], 'Game, Part II')
                self.assertEqual(data.match(platform=['PS5']), [])
                self.assertEqual(len(Path('errors.txt').read_text().splitlines()), 6)
            finally:
                os.chdir(original)

if __name__ == '__main__':
    unittest.main()
