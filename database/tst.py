import json
with open("db.json", 'r') as f:
    data = json.load(f)
    print(data)