import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = r'Temperature in the home-fcc9bfe72949.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, 'https://www.googleapis.com/auth/spreadsheets')
httpAuth = credentials.authorize(httplib2.Http())

service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

result = service.spreadsheets().values().get(spreadsheetId='1BlPfg3N4POh6Rn3rMcS1k0YDc2YR4tW9Z6C7Qom2o4E', range='Class Data!A2:E').execute()

values = result.get('values', [])

if not values:
    print('No data found.')
else:
    print('Name, Major:')
    for row in values:
        # Print columns A and E, which correspond to indices 0 and 4.
        print('%s, %s' % (row[0], row[4]))