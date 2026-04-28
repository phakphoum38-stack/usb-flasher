import json, os

def load_config():
    if not os.path.exists("config.json"):
        with open("config.json","w") as f:
            json.dump({"auto_update": True}, f)

    with open("config.json") as f:
        return json.load(f)
