import json
import os

def update_cache(path, data):
    with open(path, 'w') as file:
        json.dump(data, file)

def load_cache(path):
    if os.path.exists(path):
        with open(path, 'r') as file:
            return json.load(file)
    else:
        return {}