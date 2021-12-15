import csv
import re

from google_api_call import Create_Service
from settings import CSV_LOCATION, PRESENTATION_URL, CREDENTIALS

# Четене на CSV файла - настройка за пътя и името в settings.py

with open(CSV_LOCATION) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    NOT_DATA = ['', None]
    column_one = []
    column_two = []
    for row in csv_reader:
        if line_count == 0 or row[0] in NOT_DATA or row[1] in NOT_DATA:
            line_count += 1
            continue
        else:
            column_one.append(row[0])
            column_two.append(row[1])

    container = dict(zip(column_one, column_two))

# След прочитането на файла се създава речник 'container' който като извикаш в него стойност от колона едно
# ти връща колона 2. Пример container['ACCOUNT'] ще ти даде името на акаунта - например Airbnb.


# Прочитаме подаденият адрес на презентацията в текстовия файл и взимаме ID-то от него

text_file = open(PRESENTATION_URL, 'r')
url = text_file.readline().strip()
regex = '\/presentation\/d\/([a-zA-Z0-9-_]+)'
pres_id = re.search(regex, url).group(1)
print(f'ID-то на презентацията - {pres_id}')

# Извикване API-то на Google Slide.

CLIENT_SECRET_FILE = CREDENTIALS
API_NAME = 'slides'
API_VERSION = 'v1'
SLIDES_SCOPES = ['https://www.googleapis.com/auth/presentations']

slides_api = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SLIDES_SCOPES)

# Правим заявка (req) която създаваме от 'container'.
# Общо взето ако има {{колона_едно}} с какво да бъде заменено - колона_две
# ПРОМЕНЛИВИТЕ В ПРЕСЕНТАЦИЯТА ТРЯБВА ДА СА {{колона_едно}} - не е case sensitive.
# Пример {{account}} ще бъде заменено с Airbnb

reqs = []
for word, value in container.items():
    reqs.append(
        {
            "replaceAllText": {
                "containsText": {
                    "text": '{{' + word + '}}',
                    "matchCase": False
                },
                "replaceText": value,
            },

        },
    )

slides_api.presentations().batchUpdate(body={'requests': reqs}, presentationId=pres_id, fields='').execute()
