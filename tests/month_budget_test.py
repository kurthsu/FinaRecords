import unittest
from budgets.month_budget import MonthBudget


class MonthBudgetTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load_from_json(self):
        month_budget = MonthBudget()
        month_budget.load_from_json('./test_data/month_budget.json')

        self.assertEqual(month_budget.year, 2017)
        self.assertEqual(month_budget.month, 1)
        self.assertEqual(month_budget.total_budget, 50000)

        expenses = [{
            "name": "food",
            "budget": 8000,
            "items": []
        }, {
            "name": "housing",
            "budget": 15000,
            "items": [{
                "name": "rent"
            }, {
                "name": "utilities"
            }]
        }]
        self.assertEqual(month_budget.expenses, expenses)

        investments = [{
            "name": "saving",
            "budget": 10000
        }, {
            "name": "fund",
            "budget": 10000
        }, {
            "name": "insurance",
            "budget": 1000
        }]
        self.assertEqual(month_budget.investments, investments)

        liabilities = [{
            "name": "loan",
            "budget": 10000
        }]
        self.assertEqual(month_budget.liabilities, liabilities)

if __name__ == '__main__':
    unittest.main()