import json, os

def load_config():
    if not os.path.exists("config.json"):
        json.dump({"auto_update":True},open("config.json","w"))
    return json.load(open("config.json"))
