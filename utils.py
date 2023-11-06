import json
import os


def load_schema(name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_sсhemas_dir = os.path.join(current_dir, "json_sсhemas")

    with open(os.path.join(json_sсhemas_dir, name)) as file:
        json_schema = json.loads(file.read())
        return json_schema
