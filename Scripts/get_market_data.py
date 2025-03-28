import random
import time
import glob
import requests
import json

url_prefix = "https://steamcommunity.com/market/pricehistory/?appid=730&market_hash_name="

path_hashnames = "../Datasets/SteamMarketData/all_item_hashnames/failedDataMUSICKITS"
path_to_item_dict = "../Datasets/SteamMarketData/recoveryItems2/"
path_to_steamMarkedData = "../Datasets/SteamMarketData/"

hashname_file = path_hashnames

headers = { # Headers to send with the request (COOKIES ARE REQUIRED) SEE README
    "Cookie": ""
}

def get_and_store_data_from_hashname(url, counter, failed_to_process_counter, hash_name_count_map, name, failed=0):
    """
    Get the data from the hashname and update the hash_name_count_map and store the sales data it in item{counter}.json
    :param url: Is the URL to get the data from
    :param counter: Makes sure that the ID is set correctly
    :param failed_to_process_counter: Keep track of the failed items (due to hashname not being found)
    :param hash_name_count_map: Mapps the hashname to the ID
    :param name: The hashname
    :param failed: The number of times the request failed.
    :return: The updated counter and failed_to_process_counter
    """
    result = requests.get(url, headers=headers)  # Send a GET request to the URL
    counter += 1
    # Ensure the request was successful before trying to print the result
    if result.status_code == 200:
        # Get the JSON response as a Python object
        data = result.json()

        # Add the hashname to the data aswell as to the mapper to make it easier to identify
        hash_name_count_map[counter] = name.strip("\n")
        data['hashname'] = name

        # Write the data to a file with name item{counter}.json where counter is the ID of the item
        with open(path_to_item_dict + "item" + str(counter) + ".json", "w") as file:
            file.write(json.dumps(data, indent=4))
        file.close()
    elif 399 < result.status_code < 450 and failed < 3:
        """
        Handles the exit if STEAM throws us out
        """
        # write mapping data
        mapper_filename = path_to_steamMarkedData + "recovery_mapper_start_" + str(start) + "_end_" + str(
            counter) + "_rand_" + str(random.randint(0, 100)) + ".json"
        with open(mapper_filename, "w", encoding='UTF8') as mapper:
            mapper.write(json.dumps(hash_name_count_map, ensure_ascii=False, indent=4))
        mapper.close()

        for x in failed_to_process_list:
            print(x.strip("\n"))

        print("steam did throw us out!!")
        print("counter: ", counter)
        print("failed_counter: ", failed_to_process_counter)
        print("failed_to_process_list: ", failed_to_process_list)

        print("sleeping due to:" + str(result.status_code))
        quit()


        # time.sleep(3800)
        # get_and_store_data_from_hashname(url, counter, failed_to_process_counter, hash_name_count_map, name, failed+1)

    else:
        print(f"Error: Unable to retrieve data (status code {result.status_code})")
        failed_to_process_counter += 1
        failed_to_process_list.append(name)
    return counter, failed_to_process_counter



# Read the hashnames from file
with open(hashname_file, "r", newline='\n', encoding='UTF8') as hash_names:
    names = hash_names.readlines()
    hash_names.close()

# Set the start and end pointer
# init the counter and the failed_to_process_counter and the failed_to_process_list and the hash_name_count_map
start=23400
counter = start
failed_to_process_counter = 0
end_pointer = 23500
failed_to_process_list = []
hash_name_count_map = {}

# Loop through the hashnames and get the data from the hashname and store it
for name in names:
    name = name.replace("\n", "")
    name = name.replace("\r", "")
    url = url_prefix + name
    print(url, counter, failed_to_process_counter)
    counter, failed_to_process_counter = get_and_store_data_from_hashname(url, counter, failed_to_process_counter, hash_name_count_map, name)



print("failed_to_process_counter: ", failed_to_process_counter)
print("failed_to_process_list: ", failed_to_process_list)

# write mapping data
mapper_filename = path_to_steamMarkedData + "recovery_mapper_start_" + str(start) + "_end_" + str(end_pointer) + "_rand_" + str(random.randint(0,100)) + ".json"
with open(mapper_filename, "w", encoding='UTF8') as mapper:
    mapper.write(json.dumps(hash_name_count_map, ensure_ascii=False, indent=4))
mapper.close()

# print failed items (if you want to save them and recover later)
for x in failed_to_process_list:
    print(x.strip("\n"))

print("failed_to_process_counter: ", failed_to_process_counter)
print("failed_to_process_list: ", failed_to_process_list)


# example link to get data from the Steam API
# url = "https://steamcommunity.com/market/pricehistory/?appid=730&market_hash_name=P90%20%7C%20Blind%20Spot%20(Field-Tested)"

