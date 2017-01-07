#!/usr/local/bin/python3
import calendar
import argparse

from budgets.month_budget import MonthBudget
from gsheets.spreadsheet import Spreadsheet


def fina_records(budget):
    month_budget = MonthBudget()
    month_budget.load_from_json(budget)

    sheet_title = calendar.month_abbr[month_budget.month]

    spreadsheet = Spreadsheet('Test')
    sheets = spreadsheet.list_sheets()
    sheet = next((sh for sh in sheets if sh['title'] == sheet_title), None)
    if sheet:
        # override
        pass
    else:

        print('there is no sheet for {}'.format(sheet_title))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file",
                        help="loading budget file for one month")
    args = parser.parse_args()
    fina_records(args.file)
