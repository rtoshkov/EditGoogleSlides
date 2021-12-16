import csv
import re

from google_api_call import Create_Service
from settings import CSV_LOCATION, PRESENTATION_URL, CLIENT_SECRET_FILE, DRIVE_API_NAME, DRIVE_API_VERSION, \
    DRIVE_SCOPES, SLIDES_API_NAME, SLIDES_API_VERSION, SLIDES_SCOPES, DESTINATION_FOLDER, CHANGES


def read_file(file_name, number_of_columns=2):
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        not_data = ['', None]
        column_one = []
        column_two = []
        for row in csv_reader:
            if line_count == 0 or row[0] in not_data:
                line_count += 1
                continue
            elif number_of_columns == 2 and row[1] in not_data:
                line_count += 1
                continue
            elif number_of_columns == 2:
                column_one.append(row[0].strip().lower())
                column_two.append(row[1])
            else:
                column_one.append(row[0].strip().lower())

        result = dict(zip(column_one, column_two))

    if number_of_columns == 1:
        return column_one
    return result


# Reads 'CSV_LOCATION' file and 'CHANGES' file then creates variables
#  ---  Example:  SiteName,Telus` Tower  => container['sitename'] = 'Telus` Tower'

container = read_file(CSV_LOCATION)
changes_list = read_file(CHANGES, 1)

# Gets the presentation link from PRESENTATION_URL

text_file = open(PRESENTATION_URL, 'r')
url = text_file.readline().strip()
regex = '\/presentation\/d\/([a-zA-Z0-9-_]+)'
pres_id = re.search(regex, url).group(1)

# Gets the name of the presentation via Drive API

drive_api = Create_Service(CLIENT_SECRET_FILE, DRIVE_API_NAME, DRIVE_API_VERSION, DRIVE_SCOPES)
file_data = drive_api.files().get(fileId=pres_id, fields='name').execute()
presentation_name = file_data['name']

# Creates a copy in DESTINATION_FOLDER

new_file = drive_api.files().copy(fileId=pres_id,
                                  body={'name': f'Copy of {presentation_name}', 'parents': [DESTINATION_FOLDER]},
                                  supportsTeamDrives=True,
                                  ).execute()
new_file_id = new_file.get('id')

# Sends request via Slides API to change the copied file
# --- All placeholders in the files should be {{variable}}, where variable = The first column of CSV_LOCATION file
# --- Example: {{ACCOUNT}} !!! NOT {{ ACCOUNT }}

slides_api = Create_Service(CLIENT_SECRET_FILE, SLIDES_API_NAME, SLIDES_API_VERSION, SLIDES_SCOPES)

reqs = []
for word in changes_list:
    reqs.append(
        {
            "replaceAllText": {
                "containsText": {
                    "text": '{{' + word + '}}',
                    "matchCase": False
                },
                "replaceText": container[word],
            },

        },
    )

slides_api.presentations().batchUpdate(body={'requests': reqs}, presentationId=new_file_id, fields='').execute()
