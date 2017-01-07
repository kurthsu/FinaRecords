from .google_api import GoogleAPI
from pprint import pprint


class Spreadsheet:
    SHEETS_MIME_TYPE = 'application/vnd.google-apps.spreadsheet'

    spreadsheet_id = None
    service = None

    def __init__(self, name):
        self.spreadsheet_id = Spreadsheet.find_spreadsheet_id(name)
        self.service = GoogleAPI().get_sheets_service()

    @staticmethod
    def search_spreadsheets(keyword=None):
        service = GoogleAPI().get_drive_service()

        if keyword:
            query = "name contains '{}' and mimeType = '{}'".format(keyword, Spreadsheet.SHEETS_MIME_TYPE)
        else:
            query = "mimeType = '{}'".format(Spreadsheet.SHEETS_MIME_TYPE)

        spreadsheets = []
        page_token = None
        while True:
            results = service.files().list(q=query, spaces='drive', pageSize=10,
                                           fields="nextPageToken, files(id, name)",
                                           pageToken=page_token).execute()
            for item in results.get('files', []):
                # print('{0} ({1})'.format(item['name'], item['id']))
                spreadsheets.append(item)

            page_token = results.get('nextPageToken', None)
            if not page_token:
                break
        return spreadsheets

    @staticmethod
    def find_spreadsheet_id(name):
        service = GoogleAPI().get_drive_service()

        query = "name = '{}' and mimeType = '{}'".format(name, Spreadsheet.SHEETS_MIME_TYPE)
        results = service.files().list(q=query, spaces='drive',
                                       fields="files(id)").execute()
        files = results.get('files', [])
        if files:
            return files[0]['id']
        return None

    def list_sheets(self):
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
        sheets = []
        if spreadsheet:
            for sheet in spreadsheet['sheets']:
                sheets.append({
                    'id': sheet['properties']['sheetId'],
                    'index': sheet['properties']['index'],
                    'title': sheet['properties']['title']
                })
                pprint(sheet['properties'])
        return sheets

    def create_sheet(self, title, index, budget):
        requests = [{
            'addSheet': {
                'properties': {
                    'title': title,
                    'index': index
                }
            }
        }]
        response = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id,
                                                           body={'requests': requests}).execute()
        pprint(response)





