import json

def fetchDataFromJson():
    with open('config.json') as json_file:
        data = json.load(json_file)
        json_file.close()
        return data