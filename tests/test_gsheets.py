from gsheets.spreadsheet import Spreadsheet


def main():
    spreadsheet_id = Spreadsheet.find_spreadsheet_id('2016')
    Spreadsheet.list_sheets(spreadsheet_id)

if __name__ == '__main__':
    main()