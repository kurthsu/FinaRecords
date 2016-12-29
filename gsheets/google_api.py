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


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class GoogleAPI(metaclass=Singleton):
    CLIENT_SECRET_FILE = '../client_secret.json'
    CREDENTIAL_FILE = 'sheets.googleapis.com.fina-reports.json'
    APPLICATION_NAME = 'fina-reports'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    DISCOVERY_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'

    http_client = None

    def __init__(self):
        credentials = GoogleAPI.get_credentials()
        self.http_client = credentials.authorize(httplib2.Http())

    @staticmethod
    def get_credentials():
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, GoogleAPI.CREDENTIAL_FILE)

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(GoogleAPI.CLIENT_SECRET_FILE, GoogleAPI.SCOPES)
            flow.user_agent = GoogleAPI.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def get_drive_service(self):
        return discovery.build('drive', 'v3', http=self.http_client)

    def get_sheets_service(self):
        return discovery.build('sheets', 'v4', http=self.http_client,
                               discoveryServiceUrl=GoogleAPI.DISCOVERY_URL)
