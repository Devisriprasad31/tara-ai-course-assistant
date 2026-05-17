import json


def load_courses(json_path):
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data