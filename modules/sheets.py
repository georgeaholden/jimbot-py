"""Adapted version of sheets.py Google Sheets Program
Designed to handle connecting to and updating the GibbonFlix Requests Spreadsheet"""

from dotenv import load_dotenv
import os.path
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class SheetHandler:
    def __init__(self):
        load_dotenv()
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets'] # Allows reading and writing
        self.sheets = {"GIBBONFLIX": os.getenv('SHEET_ID_GIBBONFLIX'), "DB": os.getenv('SHEET_ID_DB')}
        self.sheet_service = connect_to_service()

    def get_range(self, sheet_name, range_name):
        result = self.sheet_service.values().get(
            spreadsheetId=self.sheets[sheet_name], range=range_name).execute()
        rows = result.get('values', [])
        return rows

    def get_cell(self, sheet_name, range_name):
        rows = self.get_range(sheet_name, range_name)
        return rows[0][0]

    def update_cell(self, sheet_name, range_name, value):
        values = [
            [value]
        ]
        body = {
            'values': values
        }
        self.sheet_service.values().update(
            spreadsheetId=self.sheets[sheet_name], range=range_name,
            valueInputOption='RAW', body=body).execute()

    def get_counter(self, sheet):
        """A counter of how many request rows currently exist is stored in the DB sheet in cell A1. This function gets that
        value from the given sheet"""
        range_name = DB_SHEET + 'A2'
        counter = int(get_cell(sheet, range_name))
        return counter

    def add_to_counter(self, sheet, counter, amount=1):
        """A counter of how many request rows currently exist is stored in the DB sheet in cell A1. This function increments
        that counter by amount (default 1)"""
        range_name = DB_SHEET + 'A2'
        update_cell(sheet, range_name, counter + amount)

    def add_request(self, sheet, title, author):
        """Takes a sheet object, to which this funtion will add a new row containing the input title, current date and user
        who used the bot command"""
        counter = get_counter(sheet)
        range_name = 'Requests!A{0}:D{0}'
        now = datetime.now()
        formatted_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        values = [
            [title, formatted_time, author, 'No']
        ]
        body = {
            'values': values
        }
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID, range=range_name.format(2 + counter),
            valueInputOption='RAW', body=body).execute()
        add_to_counter(sheet, counter)
        return True

    def changelog_printed(self, sheet, version):
        printed = get_cell(sheet, DB_SHEET + 'B2')
        if printed == version:
            return True
        else:
            update_cell(sheet, DB_SHEET + 'B2', version)
            return False


def get_creds():
    """Gets Google credentials used to connect to the spreadsheet. Taken from token.json if it exists and is valid,
    otherwise uses magic from original python quickstart program to generate a url"""
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('credentials/token.json'):
        creds = Credentials.from_authorized_user_file('credentials/token.json', scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('credentials/token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def connect_to_service():
    """Takes the credentials returned by get_creds and connects to Blackmore's Req sheet. Returns sheet, which isn't
    exactly a sheet object but is close enough for me to ignore :)"""
    service = build('sheets', 'v4', credentials=get_creds())
    # Call the Sheets API
    sheet_service = service.spreadsheets()
    return sheet_service





def test_req(sheet):
    """No longer useful beyond testing, but I'll keep for now just in case"""
    row_counter = 0
    title = 'Test Movie'
    add_request(sheet, title, row_counter)


def test_changelog(sheet):
    version = '0.1.1'
    print(changelog_printed(sheet, version))