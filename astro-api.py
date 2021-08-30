import requests
import csv
import json

url = 'http://api.open-notify.org/astros.json'
people_file_name = 'people.csv'
headers = ['name', 'craft']

def get_people_in_space_list(request_url):
    r = requests.get(request_url)
    return json.loads(r.content)['people']

def write_people_to_file(file_name, file_headers, people_list):
    with open(file_name, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, file_headers)
        for row in people_list:
            writer.writerow(row)

def get_craft_list(people_list):
    crafts = []

    for row in people_list:
        crafts.append(row['craft'])

    return crafts

def write_crafts_people(file_headers, people_list, crafts_list):
    for craft in crafts_list:
        with open(craft + '.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, file_headers)
            for row in people_list:
                if row['craft'] == craft:
                    writer.writerow(row)

def init():
    crafts = []
    people_in_space = get_people_in_space_list(url)
    write_people_to_file(people_file_name, headers, people_in_space)
    crafts = get_craft_list(people_in_space)
    crafts = set(crafts)
    write_crafts_people(headers, people_in_space, crafts)

init()
