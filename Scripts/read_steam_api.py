import argparse
import csv
import json
import time
from datetime import datetime

from database import Database

import requests

"""
Class for the reading and parsing of the information provided by the Steam API market
"""
class SteamAPI:
    """
    Steam API class. Used for the pulling and parsing of the data from the Steam API.
    """
    def __init__(self, cookie: str):
        """
        :param cookie: Steam access Cookie
        """
        self.cookie = cookie
        self.database = Database()


    def get_all_item_names(self):
        """
        Retrieve all item names from Steam Marketplace for CSGO.
        Stored into intermediate .csv file
        """
        prefixUrl = "https://steamcommunity.com/market/search/render/?query=&start="
        suffixUrl = "&count=100&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=730&norender=1"
        hash_names = []
        counter = 0

        # Request every page to get names of every existing item in the CSGO marketplace
        while True:
            # API request
            result = requests.get(f'{prefixUrl}{counter}{suffixUrl}')
            if result.status_code != 200:
                print(f"Unsuccessfull api requst - Code : {result.status_code}")
                quit()

            # Check for when at the end of the pages, i.e. no more data
            data = result.json()
            if len(data['results']) == 0:
                break

            hash_names += [item["hash_name"] for item in data['results']]

            # Prevent request timeout
            counter += 100
            time.sleep(4)

        # Write all names into csv file
        with open('../Datasets/all_items.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            for name in hash_names:
                writer.writerow([name])

    """
    Read entire price history of all market items
    """
    def read_all_items_price_history(self):
        with open('../Datasets/all_items.csv', 'r') as csvfile:
            for hash_name in csvfile:
                self._read_item_price_history(hash_name)

    """
    Read entire price history of market item
    """
    def _read_item_price_history(self, hash_name: str):
        headers = {
            "cookie": self.cookie
        }

        result = requests.get(
            f"https://steamcommunity.com/market/pricehistory/?appid=730&market_hash_name={hash_name}",
            headers=headers)

        if result.status_code != 200:
            print(f"Unsuccessfull api requst - Code : {result.status_code}")
            quit()

        data = result.json()

        # Format date into timestamp
        for entry in data['prices']:
            date = entry[0]

            date = date.split(" ")
            date[3] = date[3] + "00:00"
            date[4] = "+0000"
            datetime_format = datetime.strptime(" ".join(date), "%b %d %Y %H:%M:%S %z")
            timestamp = datetime_format.timestamp()

            entry[0] = timestamp

        # Dump data into json for intermediate storing
        with open(f'../Datasets/items/{hash_name}', 'w') as file:
            file.write(json.dumps({'hash_name': hash_name, 'prices': data['prices']}))

    """
    Parses Steam Market Skin into Database
    """
    def parse_skin_into_database(self, hash_name: str):
        # Format Skin data #
        with open(f'../Datasets/items/{hash_name}') as file:
            data = json.load(file)

        hash_name_split = hash_name.split(' ')

        # Get Skin condition
        condition = next(item.replace('(', '').replace(')', '') for item in hash_name_split if '(' in item)

        # Skin stattrack
        stattrak = next((True for item in hash_name_split if 'StatTrak' in item), False)

        # Skin Weapon
        index1 = hash_name_split.index('|')
        weaponname = ' '.join(hash_name_split[:index1])

        # Skin Name
        index2 = [i for i in range(len(hash_name_split)) if '(' in hash_name_split[i]][0]
        weaponskin = hash_name_split[index1:index2]

        # SQL Queries #

        cur = self.database.conn.cursor()


        cosmeticid = self.database.cursor(
            """
            INSERT INTO Cosmetic (type)
            VALUES ('weapon') RETURINING CosmeticID
            """
        )
        self.database.cursor.commit()

        weaponid = self.database.cursor(
            """
            SELECT WeaponID FROM Weapon WHERE Name = %(weaponname)s
            """, {'weaponname': weaponname}
        )

        self.database.cursor(
            """
            INSERT INTO WeaponSkin (CosmeticID, WeaponID, Name, Condition, StatTrak) 
            VALUES (%(cosmeticid)s, %(weaponid), %(name)s, %(condition)s, %(stattrack)s)
            """, {'cosmeticid': cosmeticid, 'weaponid': weaponid, 'name': weaponskin, 'condition': condition, 'stattrak': stattrak}
        )

        # Iterate over price history and create PriceHistory Entry
        cur.prepare(
            """
            INSERT INTO PriceHistory (comsmeticId, amount, price, timestamp) 
            VALUES (%(cosmeticid)s, %(amount)s, %(price)s, %(timestamp)s)
            """
        )
        for price in data['prices']:
            price['cosmeticid'] = cosmeticid
            cur.addBatch(price)
            if len(cur.getBatch()) >= 1000:
                cur.executeBatch()
        cur.executeBatch()

    """
    Parses Steam Market Sticker into Database
    """
    def parse_sticker_into_database(self, hash_name: str, data: dict):
        # Create Cosmetic Entry
        cosmeticid = self.database.cursor(
            """
            INSERT INTO Cosmetic (type) 
            VALUES ('sticker') RETURNING CosmeticID
            """
        )
        self.database.cursor.commit()

        # Create Sticker Entry
        self.database.cursor(
            """
            INSERT INTO Sticker (CosmeticID) 
            VALUES (%(cosmeticid)s)
            """, {'cosmeticid': cosmeticid}
        )
        self.database.cursor.commit()

        # Iterate over price history and create PriceHistory Entry
        # self.database.
        for price in data['prices']:
            price['cosmeticid'] = cosmeticid
            self.database.cursor(
                """
                INSERT INTO PriceHistory (CosmeticID, amountSold, price, timestamp) 
                VALUES (%(cosmeticid)s, %(amountSold)s, %(price)s, %(timestamp)s)
                """, price
            )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Read Esta Dataset',
        description='Reads the Esta dataset and parses into Database')

    # Set to default to '' for correct reading
    parser.add_argument('--cookie', type=str, help='Steam login cookie', action='store', dest='cookie', default='')
    args = parser.parse_args()

    steamapi = SteamAPI(args.cookie)
    steamapi.get_all_item_names()
