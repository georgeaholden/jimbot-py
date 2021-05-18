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

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_RANGE_NAME = 'Requests!A1:E'
DB_SHEET = "I'm a Fucking DB lol!"


def get_creds():
    """Gets Google credentials used to connect to the spreadsheet. Taken from token.json if it exists and is valid,
    otherwise uses magic from original python quickstart program to generate a url"""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def connect_to_sheet(creds):
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    return sheet


def read_test(sheet):
    range_name = SAMPLE_RANGE_NAME
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
    rows = result.get('values', [])
    print('{0} rows retrieved.'.format(len(rows)))
    print(rows)


def write_test(sheet):
    range_name = 'Requests!A2:C2'
    values = [
        ['Test Movie', '10:20', 'No']
        # Additional rows ...
    ]
    body = {
        'values': values
    }
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID, range=range_name,
        valueInputOption='RAW', body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


def get_counter(sheet):
    range_name = DB_SHEET + 'A1'
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
    rows = result.get('values', [])
    return int(rows[0][0])


def add_to_counter(sheet, counter, amount=1):
    range_name = DB_SHEET + 'A1'
    values = [
        [counter + amount]
    ]
    body = {
        'values': values
    }
    result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID, range=range_name.format(2 + counter),
            valueInputOption='RAW', body=body).execute()


def add_request(sheet, title, author):
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


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = get_creds()
    sheet = connect_to_sheet(creds)

    row_counter = 0

    title = 'Test Movie'
    add_request(sheet, title, row_counter)


if __name__ == '__main__':
    main()
