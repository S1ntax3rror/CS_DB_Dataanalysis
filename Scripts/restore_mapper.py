import json
import glob
import random

with open("../Datasets/SteamMarketData/all_item_hashnames/all_hashnames.csv", "r", encoding='UTF8') as file:
    hashnames = file.readlines()
file.close()

with open("../Datasets/SteamMarketData/all_item_hashnames/failed_to_get_data", "r", encoding="UTF8") as file:
    failed_hashnames = file.readlines()
file.close()

mapper_files = glob.glob("../Datasets/SteamMarketData/*.json")
items = glob.glob("../Datasets/SteamMarketData/items/item1*.json")
#
# combined_dict = {}
# for path in mapper_files:
#     with open(path, "r", encoding='UTF8') as file:
#         data = json.load(file)
#         combined_dict.update(data)
#     file.close()

# values = list(combined_dict.values())

# fail_counter = 102
count = 16786
fail_list = []

hash_name_count_map = {}

for i in range(count, 17739):
    for item in items:
        if str(i) in item:
            with open(item, "r", encoding='UTF8') as file:
                price_data = json.load(file)
                hashname = price_data['hashname']
            file.close()
            hash_name_count_map[i] = hashname
    # if hashname not in failed_hashnames:
    #     hash_name_count_map[count] = hashname
    #     count += 1
    # else:
    #     # fail_counter += 1
    #     print(hashname)
    #     failed_hashnames.remove(hashname)


with open("../Datasets/SteamMarketData/mapper_start_16786_end_17738.json", "w", encoding='UTF8') as file:
    file.write(json.dumps(hash_name_count_map, ensure_ascii=False, indent=4))
    file.close()




# plot template

# with open("../Datasets/SteamMarketData/items/item13609.json", "r", encoding='UTF8') as file:
#     data = json.load(file)
#
# data = data['prices']
# print(data)
#
# dates = []
# prices = []
# for x in data:
#     dates.append(x[0])
#     prices.append(float(x[1])+float(x[2]))
#
#
# import matplotlib as plt
#
# plt.plot(data, prices)
#
#
#
#
#
# print("failed_hashnames", failed_hashnames[101:])
#
# print("total", fail_counter + count)
# print("fail_count", fail_counter)
#
#
# mapper_filename = "../Datasets/SteamMarketData/mapper_start_" + str(5001) + "_end_" + str(14000) + "_rand_" + str(random.randint(0,100)) + ".json"
# with open(mapper_filename, "w", encoding='UTF8') as mapper:
#     mapper.write(json.dumps(hash_name_count_map, ensure_ascii=False, indent=4))
# mapper.close()