import requests
import csv
import json
import logging

URL = 'http://api.open-notify.org/astros.json'
PEOPLE_FILE_NAME = 'people.csv'
HEADERS = ['name', 'craft']


def get_people_in_space(request_url: str) -> any:
    logging.info('Calling API...')
    try:
        r = requests.get(request_url, timeout=5).content
    except Exception as err:
        logging.error(err)
        return None
    logging.info('Data fetched')
    return json.loads(r)['people']


def write_to_csv(file_name: str, file_headers: list[str], items: list[any]) -> None:
    with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=file_headers)
        writer.writeheader()
        for row in items:
            writer.writerow(row)


def write_people_to_file(file_name: str, file_headers: list[str], people_list: list[str]) -> None:
    logging.info('Writing people to CSV')
    write_to_csv(file_name, file_headers, people_list)


def sanitize_filename(filename: str) -> str:
    return filename.replace(' _:', '')
                            

def write_crafts_people(file_headers: list[str], people_list: list[dict[str, str]], crafts_list: set[str]) -> None:
    logging.info('Writing crafts to CSV')
    for craft in sorted(list(crafts_list)):
        file_name = f'{sanitize_filename(craft)}.csv'
        people_list_filtered = filter(lambda man: man['craft'] == craft, people_list)
        write_to_csv(file_name, file_headers, list(people_list_filtered))


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    logging.info('Starting script')

    people = get_people_in_space(URL)
    crafts = set(row['craft'] for row in people)

    write_people_to_file(PEOPLE_FILE_NAME, HEADERS, people)
    write_crafts_people(HEADERS, people, crafts)


if __name__ == '__main__':
    main()
