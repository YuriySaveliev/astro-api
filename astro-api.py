import requests
import csv
import json

URL = 'http://api.open-notify.org/astros.json'
PEOPLE_FILE_NAME = 'people.csv'
HEADERS = ['name', 'craft']


def get_people_in_space_list(request_url):
    r = requests.get(request_url)
    return json.loads(r.content)['people']


def write_people_to_file(file_name, file_headers, people_list):
    with open(file_name, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, file_headers)
        for row in people_list:
            writer.writerow(row)


def write_crafts_people(file_headers, people_list, crafts_list):
    for craft in crafts_list:
        with open(craft + '.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, file_headers)
            for row in people_list:
                if row['craft'] == craft:
                    writer.writerow(row)


def init():
    people_in_space = get_people_in_space_list(URL)
    crafts = set(row['craft'] for row in people_in_space)
    write_people_to_file(PEOPLE_FILE_NAME, HEADERS, people_in_space)
    write_crafts_people(HEADERS, people_in_space, crafts)


init()
