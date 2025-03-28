import time

import requests
import json


baseUrl = "https://steamcommunity.com/market/search/render/?query=&start="
suffix = "&count=100&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=730&norender=1"

def exit_program(hash_name_storage, id):
    keys = hash_name_storage.keys()
    for key in keys:  # Print the hash names retrieved so far before saving (for recovery)
        print(f"{key}: {hash_name_storage[key]}")
    with open("../Datasets/hash_name_storage.json", "w", encoding='UTF8') as f:
        hash_name_storage['break_ID'] = id
        json.dump(hash_name_storage, f, ensure_ascii=False, indent=4)
        f.close()

def steam_api():
    """
    Function to get hash names from Steam API and save them to a JSON file
    :return: hash_name_storage
    """
    hash_name_storage = {}
    id = 1

    if id != 1:
        with open("../Datasets/hash_name_storage.json", "r", encoding='UTF8') as f:
            hash_name_storage = json.load(f)
        f.close()

    for i in range(3):
        print(f"Iteration {i}")
        result = requests.get(baseUrl + str(i) + suffix)  # Send a GET request to the URL

        # Ensure the request was successful before trying to print the result
        if result.status_code == 200:
            data = result.json()  # Get the JSON response as a Python dictionary

            for item in data['results']:
                hash_name_storage[item['hash_name']] = id
                id += 1
            time.sleep(180) # Sleep for 5 seconds to avoid rate limiting
        else:
            exit_program(hash_name_storage, id)
            print(f"Error: Unable to retrieve data (status code {result.status_code})")

    exit_program(hash_name_storage, id)
    return hash_name_storage
steam_api()