from pathlib import Path
import json


class MonthBudget:
    year = 2017
    month = 1
    total_budget = 0
    expenses = []
    investments = []
    liabilities = []

    def __init__(self):
        pass

    def load_from_json(self, file_name):
        file_path = Path(file_name)

        if not file_path.is_file():
            raise Exception("import file not found")

        try:
            with open(file_path) as f:
                data = json.load(f)

            self.year = data['year']
            self.month = data['month']
            self.total_budget = data['total_budget']
            self.expenses = data['expenses']
            self.investments = data['investments']
            self.liabilities = data['liabilities']
        except Exception as e:
            print("Exception on loading json file", e)
