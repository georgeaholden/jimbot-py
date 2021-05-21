"""Adapted version of sheets.py Google Sheets Program
Designed to handle connecting to and updating the GibbonFlix Requests Spreadsheet"""

from dotenv import load_dotenv
import os.path
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

load_dotenv()
SPREADSHEET_ID = os.getenv('SHEETID_REQUESTS')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']  # Allows reading and writing
DB_SHEET = "I'm a Fucking DB lol!"  # Name of Sheet I'm using for persistence to avoid paying for a DB


def get_creds():
    """Gets Google credentials used to connect to the spreadsheet. Taken from token.json if it exists and is valid,
    otherwise uses magic from original python quickstart program to generate a url"""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('credentials/token.json'):
        creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('credentials/token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def connect_to_sheet(creds):
    """Takes the credentials returned by get_creds and connects to Blackmore's Req sheet. Returns sheet, which isn't
    exactly a sheet object but is close enough for me to ignore :)"""
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    return sheet


def get_cell(sheet, range_name):
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
    rows = result.get('values', [])
    return rows[0][0]


def update_cell(sheet, range_name, value):
    values = [
        [value]
    ]
    body = {
        'values': values
    }
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID, range=range_name,
        valueInputOption='RAW', body=body).execute()


def get_counter(sheet):
    """A counter of how many request rows currently exist is stored in the DB sheet in cell A1. This function gets that
    value from the given sheet"""
    range_name = DB_SHEET + 'A2'
    counter = int(get_cell(sheet, range_name))
    return counter


def add_to_counter(sheet, counter, amount=1):
    """A counter of how many request rows currently exist is stored in the DB sheet in cell A1. This function increments
    that counter by amount (default 1)"""
    range_name = DB_SHEET + 'A2'
    update_cell(sheet, range_name, counter + amount)


def add_request(sheet, title, author):
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


def changelog_printed(sheet, version):
    printed = get_cell(sheet, DB_SHEET + 'B2')
    if printed == version:
        return True
    else:
        update_cell(sheet, DB_SHEET + 'B2', version)
        return False


def test_req(sheet):
    """No longer useful beyond testing, but I'll keep for now just in case"""
    row_counter = 0
    title = 'Test Movie'
    add_request(sheet, title, row_counter)


def test_changelog(sheet):
    version = '0.1.1'
    print(changelog_printed(sheet, version))


if __name__ == '__main__':
    creds = get_creds()
    test_sheet = connect_to_sheet(creds)
    # test_req(test_sheet)
    test_changelog(test_sheet)
