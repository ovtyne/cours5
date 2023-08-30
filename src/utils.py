import json


def read_file(filename):
    result_list = []
    with open(filename, 'r', encoding="utf-8") as file:
        data = json.load(file)
    for item in data:
        result_list.append((item['id'], item['name']))
    return result_list
