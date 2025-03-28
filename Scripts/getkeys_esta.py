import os
import json

path = "../Datasets/esta/data/lan/"

lanfiles = os.listdir(path)

lan_jsonfiles = []
for file in lanfiles:
    if not ".xz" in file:
        lan_jsonfiles.append(file)

esta_json = lan_jsonfiles[0]
print(esta_json)
data = None
with open(path + esta_json + "/" + esta_json, "r", encoding='ISO-8859-1') as f:
    data = json.load(f)

dict_all = {}
datatypes = []
def get_keys(obj, n, keys):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key not in keys:
                keys[key] = {}
                spacer = "  "*n
                # print(spacer, key)
            get_keys(value, n + 1, keys[key])
    elif isinstance(obj, list):
        list_ptr = True
        for item in obj:
            get_keys(item, n + 1, keys)
            # if not isinstance(item, dict) and list_ptr:
            #     print(obj, keys)
            #     list_ptr = False
    # if type(obj) not in datatypes:
    #     print(type(obj))
    #     datatypes.append(type(obj))
    return keys


# Get all unique keys
unique_keys = get_keys(data, 0, dict_all)
game = list(unique_keys.get("gameRounds").get("frames").get("t").get("players").keys())

with open("../Resources/entities.txt", "r") as file:
    lines = file.readlines()
line = lines[0].split(", ")

for item in game:
    if item not in line:
        print("missing", item)

for item in line:
    if item not in game:
        print("remove", item)

print(game)
print(line)

json.dump(unique_keys, open("../Resources/unique_keys2.json", "w"), indent=4)




