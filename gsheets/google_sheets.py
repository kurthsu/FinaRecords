import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

CLIENT_SECRET_FILE = '../client_secret.json'
CREDENTIAL_FILE = 'sheets.googleapis.com.fina-reports.json'
APPLICATION_NAME = 'fina-reports'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
DISCOVERY_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, CREDENTIAL_FILE)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


class GoogleSheets:
    SHEETS_MIME_TYPE = 'application/vnd.google-apps.spreadsheet'
    http_client = None

    def __init__(self):
        credentials = get_credentials()
        self.http_client = credentials.authorize(httplib2.Http())

    def find_sheets(self, keyword=None):
        service = self._build_drive_service()

        if keyword:
            query = "name contains '{}' and mimeType = '{}'".format(keyword, GoogleSheets.SHEETS_MIME_TYPE)
        else:
            query = "mimeType = '{}'".format(GoogleSheets.SHEETS_MIME_TYPE)

        sheets = []
        page_token = None
        while True:
            results = service.files().list(q=query, spaces='drive', pageSize=10,
                                           fields="nextPageToken, files(id, name)",
                                           pageToken=page_token).execute()
            for item in results.get('files', []):
                print('{0} ({1})'.format(item['name'], item['id']))
                sheets.append(item)

            page_token = results.get('nextPageToken', None)
            if not page_token:
                break
        return sheets

    # private methods
    def _build_drive_service(self):
        return discovery.build('drive', 'v3', http=self.http_client)

    def _build_sheets_service(self):
        return discovery.build('sheets', 'v4', http=self.http_client,
                               discoveryServiceUrl=DISCOVERY_URL)
