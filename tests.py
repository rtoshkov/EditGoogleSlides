from google_api_call import Create_Service

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
DRIVE_SCOPES = ['https://www.googleapis.com/auth/drive']

drive_api = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, DRIVE_SCOPES)

new_file = drive_api.files().copy(fileId='1mL7hGZBmH57o5Nvl79rqqG90H83YFlrdHAGUBuMl1pA',
                       body={'name': 'TestFile12345', 'parents': ['1gywvccO1QCx2jA2YkXx0w-YcJ0yptZxw']},
                       supportsTeamDrives=True,
                       ).execute()

new_file_id = new_file.get('id')

print(new_file_id)