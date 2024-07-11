import os.path
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of the target spreadsheet.
SAMPLE_SPREADSHEET_ID = "1UtvvgqI-WaAGfVTySM07nI9KYpCkXewZJupSmIN6KCM"
SAMPLE_RANGE_NAME = "Sheet1!A1"

def read_log_file(file_path):
    with open(file_path, 'r') as file:
        log_entries = file.readlines()
    return log_entries

def parse_log_entries(log_entries):
    return [[entry.strip()] for entry in log_entries]

def main():
    """Shows basic usage of the Sheets API.
    Writes log data to a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credit.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        while True:
            # Read and parse the log file
            log_entries = read_log_file("logtext.txt")
            parsed_entries = parse_log_entries(log_entries)

            # Write the parsed data to the Google Sheet
            body = {
                'values': parsed_entries
            }
            result = sheet.values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=SAMPLE_RANGE_NAME,
                valueInputOption="RAW",
                body=body
            ).execute()


            # Wait for 5 seconds before updating again
            time.sleep(5)

    except HttpError as err:
        print(err)

if __name__ == "__main__":
    main()
