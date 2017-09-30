from __future__ import print_function
import httplib2
import os
from datetime import datetime

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.service_account import ServiceAccountCredentials

CLIENT_SECRET_FILE = r'Temperature in the home-fcc9bfe72949.json'
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
APPLICATION_NAME = 'TestSheet'

def get_credentials(secret_file, application_name, scopes):

    credentials = ServiceAccountCredentials.from_json_keyfile_name(secret_file, scopes)
    return credentials

def main(application_name, secret_file, scopes):

    credentials = get_credentials(secret_file, application_name, scopes)
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    dt = datetime.now()
    date_now = dt.strftime('%S:%H:%M %d.%m.%Y')
    value = num
    spreadsheet_id = '1BlPfg3N4POh6Rn3rMcS1k0YDc2YR4tW9Z6C7Qom2o4E'
    range_name = 'A:B'
    value_input_option = "USER_ENTERED"
    values = [
        [
            # Cell values ...
            date_now, value
        ],
        # Additional rows ...
    ]
    body = {
        'values': values
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()



if __name__ == '__main__':

    main(APPLICATION_NAME, CLIENT_SECRET_FILE, SCOPES)