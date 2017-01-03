#!/usr/local/bin/python3
import calendar
import sys

from budgets.month_budget import MonthBudget
from gsheets.spreadsheet import Spreadsheet


def fina_records(budget):
    month_budget = MonthBudget()
    month_budget.load_from_json(budget)

    sheet_title = calendar.month_abbr[month_budget.month]

    spreadsheet_id = Spreadsheet.find_spreadsheet_id('Test')
    sheets = Spreadsheet.list_sheets(spreadsheet_id)
    sheet = (sh for sh in sheets if sh['title'] == sheet_title).next()
    if sheet:
        # override
        pass
    else:
        print('there is no sheet for {}'.format(sheet_title))

if __name__ == '__main__':
    print(sys.argv[1])
    # fina_records()