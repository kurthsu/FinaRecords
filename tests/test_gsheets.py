from gsheets.google_sheets import GoogleSheets


def main():
    gsheets = GoogleSheets()
    sheets = gsheets.find_sheets()
    print(len(sheets))

if __name__ == '__main__':
    main()