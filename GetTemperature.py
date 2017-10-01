from __future__ import print_function
import httplib2
from datetime import datetime
import re
import time

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

FILE_TEMPERATURE = r'/sys/bus/w1/devices/28-0416b0a59aff/w1_slave'
CLIENT_SECRET_FILE = r'Temperature in the home-fcc9bfe72949.json'
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
APPLICATION_NAME = 'Temperature'

def get_credentials(secret_file, application_name, scopes):

	credentials = ServiceAccountCredentials.from_json_keyfile_name(secret_file, scopes)
	return credentials

def main(application_name, secret_file, scopes, temperature):
	global last_temperature
	tolerance = 0.2
	credentials = get_credentials(secret_file, application_name, scopes)
	http = credentials.authorize(httplib2.Http())
	discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
					'version=v4')
	service = discovery.build('sheets', 'v4', http=http,
							discoveryServiceUrl=discoveryUrl)

	dt = datetime.now()
	date_now = dt.strftime('%H:%M:%S %d.%m.%Y')

	spreadsheet_id = '1BlPfg3N4POh6Rn3rMcS1k0YDc2YR4tW9Z6C7Qom2o4E'
	range_name = 'A:B'
	value_input_option = "USER_ENTERED"
	if abs(temperature - last_temperature) >= tolerance:
		values = [
			[
				# Cell values ...
				date_now, temperature
			],
			# Additional rows ...
		]
		body = {
			'values': values
			}
		result = service.spreadsheets().values().append(
			spreadsheetId=spreadsheet_id, range=range_name,
			valueInputOption=value_input_option, body=body).execute()


def read_file(file):
	with open(file, 'r', encoding='utf-8') as f:
		return f.read()


def is_signal(text):
	key = r'YES'
	compile_key = re.compile(key)

	if compile_key.search(text):
		return True

	return False


def read_temperature(file):
	tolerance = 0.2
	key = r't=/d+'
	key_compile = re.compile(key)
	text = read_file(file)
	while not is_signal(text):
		time.sleep(0.2)
		text = read_file(file)
	match_obj = key_compile.search(text)
	if match_obj:
		return float(match_obj.string) / 1000.0


if __name__ == '__main__':
	last_temperature = read_temperature(FILE_TEMPERATURE)
	while True:
		main(APPLICATION_NAME, CLIENT_SECRET_FILE, SCOPES, read_temperature(FILE_TEMPERATURE))
		time.sleep(10)