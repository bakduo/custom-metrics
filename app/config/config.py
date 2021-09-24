import json

CONFIG_APP = {}

with open("app/config/testing.json") as json_data_file:
    CONFIG_APP = json.load(json_data_file)

