
import glob
import json

# mapper1 = "../Datasets/SteamMarketData/NEW_MAPPING_1_to_5000.json"
# mapper2 = "../Datasets/SteamMarketData/mapper_start_5000_end_5100_rand_60.json"
# mapper3 = "../Datasets/SteamMarketData/mapper_start_5100_end_10000_rand_32.json"
# mapper4 = "../Datasets/SteamMarketData/mapper_start_10000_end_11986_rand_87.json"
# mapper5 = "../Datasets/SteamMarketData/mapper_start_11985_end_16786_rand_46.json"
# mapper6 = "../Datasets/SteamMarketData/mapper_start_16786_end_17738.json"
# mapper7 = "../Datasets/SteamMarketData/mapper_start_17738_end_18986_rand_8.json"
# mapper8 = "../Datasets/SteamMarketData/mapper_start_18986_end_20402_rand_42.json"
# mapper9 = "../Datasets/SteamMarketData/mapper_start_20402_end_22500_rand_17.json"

# mappers = [mapper1, mapper2, mapper3, mapper4, mapper5, mapper6, mapper7, mapper8, mapper9]
prefix = "../Datasets/SteamMarketData/"
mapper1 = "recovery_mapper_start_23200_end_23500_rand_24.json"
mapper2 = "recovery_mapper_start_23400_end_23500_rand_16.json"
mapper3 = "mapping_all_new.json"
mappers = [prefix+ mapper1, prefix + mapper2, prefix + mapper3]
combined_mapper = {}


for mapper in mappers:
    with open(mapper, "r", encoding='UTF8') as file:
        data = json.load(file)
        combined_mapper.update(data)
        file.close()

print(len(combined_mapper))

with open("../Datasets/SteamMarketData/mapping_all_new.json", "w", encoding='UTF8') as file:
    file.write(json.dumps(combined_mapper, ensure_ascii=False, indent=4))
file.close()
















#
# with open("../Datasets/SteamMarketData/all_item_hashnames/all_hashnames.csv", "r", encoding='UTF8') as file:
#     data = file.readlines()[0:5000]
#     file.close()

# for elem in combined_mapper:
#     print(elem, combined_mapper[elem])
#     with open("../Datasets/SteamMarketData/items/item" + str(elem) + ".json", "r", encoding='UTF8') as file:
#         data = json.load(file)
#         data["hashname"] = combined_mapper[elem]
#         file.close()
#     with open("../Datasets/SteamMarketData/items/subItems2/item" + str(elem) + ".json", "w", encoding='UTF8') as file:
#         file.write(json.dumps(data, ensure_ascii=False, indent=4))
#         file.close()
#
# keys = combined_mapper.keys()
# pairs = []
# for key in keys:
#     item = combined_mapper[key]
#     for i, line in enumerate(data):
#         if item + "\n" == line:
#             # print(key, item, line, i)
#             pairs.append((key, i))
#
# print(pairs)
#
# mapper_5000 = {}
#
# for pair in pairs:
#     # with open("../Datasets/SteamMarketData/items/subItems3/item" + str(pair[0]) + ".json", "r", encoding='UTF8') as file:
#     #     data = json.load(file)
#     #     file.close()
#     # with open("../Datasets/SteamMarketData/items/Correct_1_5000_items/item" + str(pair[1]) + ".json", "w", encoding='UTF8') as file:
#     #     file.write(json.dumps(data, ensure_ascii=False, indent=4))
#     #     file.close()
#
#     mapper_5000[pair[1]] = combined_mapper[pair[0]]

