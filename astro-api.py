import requests
import csv
import json

URL = 'http://api.open-notify.org/astros.json'
PEOPLE_FILE_NAME = 'people.csv'
HEADERS = ['name', 'craft']


def get_people_in_space(request_url: str) -> json:
    print('Calling API...')
    r = requests.get(request_url).content
    print('Data fetched')
    return json.loads(r)['people']


def write_to_csv(file_name: str, file_headers: list[str], items: list[str]) -> None:
    with open(file_name, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=file_headers)
        writer.writeheader()
        for row in items:
            writer.writerow(row)


def write_people_to_file(file_name: str, file_headers: list[str], people_list: list[str]) -> None:
    print('Writing people to CSV')
    write_to_csv(file_name, file_headers, people_list)


def write_crafts_people(file_headers: list[str], people_list: list[str], crafts_list: list[str]) -> None:
    print('Writing crafts to CSV')
    for craft in crafts_list:
        file_name = f'{craft}.csv'
        people_list_filtered = filter(lambda man: man['craft'] == craft, people_list)
        write_to_csv(file_name, file_headers, people_list_filtered)


def start() -> None:
    print('Starting script')
    people = get_people_in_space(URL)
    crafts = set(row['craft'] for row in people)
    write_people_to_file(PEOPLE_FILE_NAME, HEADERS, people)
    write_crafts_people(HEADERS, people, crafts)


start()
