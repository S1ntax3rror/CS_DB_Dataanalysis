from __future__ import annotations

import glob
from thefuzz import fuzz

import numpy as np
import re
from database import Database
import ujson as json
import psycopg
from datetime import datetime
from typing import List
import csv




class Market:
    def __init__(self, init_db=False, read_IDS=True):
        # init database
        self.database = Database()

        # create all SQL Tables in Tables folder
        if init_db:
            print("init_db")
            self.database.init_files("../SQL/MarketTables")

        self.mapper = {}
        self.load_mapper()
        self.mapper_keys = self.mapper.keys()

        # init cursor
        self.cur = self.database.cur

        # init ID lists to import from DB
        self.playerID = []
        self.playerName = []
        self.playerID_NAME_MAP = {}

        self.tournamentID = []
        self.tournamentName = []
        self.tournamentID_NAME_MAP = {}

        self.teamID = []
        self.teamName = []
        self.teamID_NAME_MAP = {}

        self.weaponID = []
        self.weaponName = []
        self.weaponID_NAME_MAP = {}
        self.weaponNAME_CLASS_MAP = {}

        if read_IDS:
            self.get_weapon_ids()
            self.get_team_ids()
            self.get_player_ids()
            self.get_tournament_ids()

        # init date conversion
        self.date_parser = datetime.strptime
        self.DATE_FORMAT = "%b %d %Y %H"

    def load_keys(self):
        keys = {
            "priceID": "price",
            "CosmeticID": "cosmetic",
            "weaponSkinID": "weaponSkin",
            "teamStickerID": "teamSticker",
            "playerStickerID": "playerSticker"
        }

        for id, table in keys.items():
            self.cur.execute(f"SELECT MAX({id}) FROM {table}")
            setattr(self, id, self.cur.fetchone()[0] + 1)

    def init_database(self):
        self.database.init_files("../SQL/MarketTables")
        print("initialized data")

    def read_cosmetics(self):
        IDs = []
        hash_names = []
        for key in self.mapper_keys:
            IDs.append(key)
            hash_names.append(self.mapper[key])


        types = []
        weapons = self.get_weapon_names()

        for name in hash_names:
            type_arr = name.split("|")
            if len(type_arr) > 1:
                Ptype = type_arr[0]
                if "★ StatTrak™" in Ptype:
                    Ptype = Ptype.strip("★ StatTrak™")
                if "★" in Ptype:
                    Ptype = Ptype.strip("★")
                if "StatTrak™" in Ptype:
                    Ptype = Ptype.strip("StatTrak™")
                Ptype = Ptype.rstrip()
                Ptype = Ptype.lstrip()

                if "Souvenir" in Ptype or Ptype in weapons:
                    types.append("WeaponSkin")
                elif "Graffiti" in name:
                    types.append("Graffiti")
                elif "Patch" in name:
                    types.append("Patch")
                elif "Charm" in name:
                    types.append("Charm")
                elif "Music Kit" in name:
                    types.append("Music Kit")
                elif "Key" in name:
                    types.append("Key")
                elif "Case" in name:
                    types.append("Case")
                elif "Capsule" in name:
                    types.append("Capsule")
                elif "Sticker" in name:
                    types.append("Sticker")
                elif "Souvenir Package" in name:
                    types.append("Souvenir Package")
                elif "Pin" in name:
                    types.append("Pin")
                elif "★" in name:
                    types.append("WeaponSkin")
                elif "Music Kit Box" in name:
                    types.append("Music Kit Box")
                elif "Pass" in name:
                    types.append("Pass")
                elif ("Legends" in name and "Foil" in name or "Legends" in name and "Holo" in name) or (
                        "Challengers" in name):
                    types.append("Capsule")
                elif "RMR" in name:
                    types.append("Capsule")
                elif "Patch Pack" in name:
                    types.append("Patch Pack")
                else:
                    types.append("Agent")

            elif "Key" in name:
                types.append("Key")
            elif "Case" in name:
                types.append("Case")
            elif "Capsule" in name:
                types.append("Capsule")
            elif "Sticker" in name:
                types.append("Sticker")
            elif "Souvenir Package" in name:
                types.append("Souvenir Package")
            elif "Pin" in name:
                types.append("Pin")
            elif "★" in name:
                types.append("WeaponSkin")
            elif "Music Kit Box" in name:
                types.append("Music Kit Box")
            elif "Pass" in name:
                types.append("Pass")
            elif ("Legends" in name and "Foil" in name or "Legends" in name and "Holo" in name) or ("Challengers" in name):
                types.append("Capsule")
            elif "RMR" in name:
                types.append("Capsule")
            elif "Patch Pack" in name:
                types.append("Patch Pack")
            else:
                types.append("MISC")


        query = """
                     INSERT INTO Cosmetic (CosmeticID, name, type) VALUES (%s, %s, %s)
                """

        self.cur.executemany(query, zip(IDs, hash_names, types))


    def read_WeaponSkin(self):

        keys = self.mapper.keys()
        IDs = []

        hash_names = []
        StatTrak = []
        condition = []
        CosmeticID = []
        game_weaponID = []

        for key in keys:
            IDs.append(key)
            hash_names.append(self.mapper[key])

        weapon_idMap = [self.weaponID, self.weaponName]
        types = []
        weapons = self.get_weapon_names()

        # maps the weaponIDs of the Database to the weapons of the stickers
        weapon_dict = {}

        # get all conditions
        conditions = ["Field-Tested", "Factory New", "Minimal Wear", "Well-Worn", "Battle-Scarred"]

        # Iterate through the weapon names
        for name in weapons:
            # Find the best corresponding entry from weapon_list
            if name in weapon_idMap[1]:
                idx = weapon_idMap[1].index(name)
                weapon_dict[name] = weapon_idMap[0][idx]
            elif "Gloves" in name or "Hand Wraps" in name:
                weapon_dict[name] = self.weaponID_NAME_MAP['']
            elif "Knife" in name or "Karambit" in name or "Bayonet" in name or "Shadow Daggers" in name:
                weapon_dict[name] = self.weaponID_NAME_MAP['Knife']
            elif "M4A1-S" in name:
                weapon_dict[name] = self.weaponID_NAME_MAP['M4A1']
            elif "CZ75-Auto" in name:
                weapon_dict[name] = self.weaponID_NAME_MAP['CZ75 Auto']
            else:
                weapon_dict[name] = None


        for name, ID in zip(hash_names, IDs):
            type_arr = name.split("|")
            if len(type_arr) > 1:
                Ptype = type_arr[0]
                if "★ StatTrak™" in Ptype:
                    Ptype = Ptype.strip("★ StatTrak™")
                if "★" in Ptype:
                    Ptype = Ptype.strip("★")
                if "StatTrak™" in Ptype:
                    Ptype = Ptype.strip("StatTrak™")
                Ptype = Ptype.rstrip()
                Ptype = Ptype.lstrip()

                if "Souvenir" in Ptype or Ptype in weapons:
                    types.append("WeaponSkin")
                    Ptype = Ptype.replace("Souvenir ", "")
                    game_weaponID.append(weapon_dict[Ptype])
                    # get StatTrak
                    if "StatTrak™" in name:
                        StatTrak.append(True)
                    else:
                        StatTrak.append(False)
                    # get condition
                    if conditions[0] in name:
                        condition.append(conditions[0])
                    elif conditions[1] in name:
                        condition.append(conditions[1])
                    elif conditions[2] in name:
                        condition.append(conditions[2])
                    elif conditions[3] in name:
                        condition.append(conditions[3])
                    elif conditions[4] in name:
                        condition.append(conditions[4])
                    else:
                        condition.append(None)
                    CosmeticID.append(ID)
                else:
                    types.append(Ptype)
            else:
                types.append(None)


        query = """
                     INSERT INTO WeaponSkin (weaponSkinID, StatTrak, condition, CosmeticID, game_weaponID) VALUES (%s, %s, %s, %s, %s)
                """
        weaponSkinID = np.arange(1, len(StatTrak)+1)

        # print(weaponSkinID, StatTrak, condition, CosmeticID)
        self.cur.executemany(query, zip(weaponSkinID, StatTrak, condition, CosmeticID, game_weaponID))


    def read_TeamSticker(self):
        mapper = self.mapper
        teams = []

        for id, name in  zip(self.teamID, self.teamName):
            teams.append([id, name])

        keys = mapper.keys()
        IDs = []

        hash_names = []
        teamStickerID = []
        tournamentID = []
        teamID = []
        condition = []
        CosmeticID = []

        Major_stockholm_ID = None
        Major_antwerp_ID = None

        tournamentKeys = self.tournamentID_NAME_MAP.keys()
        for key in tournamentKeys:
            if "Major" and "Stockholm" in self.tournamentID_NAME_MAP[key]:
                Major_stockholm_ID = key
            elif "Major" and "Antwerp" in self.tournamentID_NAME_MAP[key]:
                Major_antwerp_ID = key


        for key in keys:
            IDs.append(key)
            hash_names.append(mapper[key])

        navi_id = self.teamID[self.teamName.index("Natus Vincere")]

        for name, ID in zip(hash_names, IDs):
            if "Sticker" in name:

                if len(name.split("|")) == 1:
                    pass #capsules
                elif len(name.split("|")) == 2:
                    pass #casual stickers
                elif len(name.split("|")) == 3:
                    type_arr = name.split("|")
                    team_or_player_name = type_arr[1].lstrip(" ").split(" ")[0]

                    formated_name = self.fuzzy_format_team_name(team_or_player_name)
                    threshold = 65
                    teamNameID_map = ""
                    for team in self.teamName:
                        formatter_checker_team_name = self.fuzzy_format_team_name(team)
                        if fuzz.ratio(formated_name, formatter_checker_team_name) > threshold:
                            teamNameID_map = (team, self.teamID[self.teamName.index(team)])
                            threshold = fuzz.ratio(formated_name, formatter_checker_team_name)

                    if teamNameID_map != "":
                        best_match_Name, best_match_ID = teamNameID_map

                        if "NAVI" in name or "Natus Vincere" in name:
                            best_match_Name = "Natus Vincere"
                            best_match_ID = navi_id
                        CosmeticID.append(ID)

                        # teamID.append(team_id_list[team_list.index(team_or_player_name)])
                        teamID.append(best_match_ID)

                        if "Stockholm" in type_arr[2]:
                            tournamentID.append(Major_stockholm_ID)
                        elif "Antwerp" in type_arr[2]:
                            tournamentID.append(Major_antwerp_ID)
                        else:
                            tournamentID.append(None)

                        teamStickerID.append(ID)

                        match = re.search(r"\((.*?)\)", type_arr[1])

                        if match:
                            condition.append(match.group(1))
                        else:
                            condition.append("Normal")

        print(condition)
        print(teamID)
        print(tournamentID)
        print(teamStickerID)

        # unique_numbers = {s: i for i, s in enumerate(set(tournamentID))}
        # Assign numbers based on the dictionary
        # assigned_tournament_ids = [unique_numbers[s] for s in tournamentID]
        # print(assigned_tournament_ids)

        query = """
                     INSERT INTO TeamSticker (teamStickerID, condition, tournamentID, teamID, CosmeticID) VALUES (%s, %s, %s, %s, %s)
                """

        print(teamStickerID, condition, tournamentID, teamID, CosmeticID)

        print(len(teamStickerID), len(condition), len(tournamentID), len(teamID), len(CosmeticID))
        self.cur.executemany(query, zip(teamStickerID, condition, tournamentID, teamID, CosmeticID))



    def read_PlayerSticker(self):
        mapper = self.mapper

        keys = mapper.keys()
        IDs = []

        hash_names = []
        playerStickerID = []
        tournamentID = []
        playerID = []
        condition = []
        CosmeticID = []


        for key in keys:
            IDs.append(key)
            hash_names.append(mapper[key])

        # init Major IDs
        Major_stockholm_ID = None
        Major_antwerp_ID = 0
        tournamentKeys = self.tournamentID_NAME_MAP.keys()
        for key in tournamentKeys:
            if "Major" and "Stockholm" in self.tournamentID_NAME_MAP[key]:
                Major_stockholm_ID = key
            elif "Major" and "Antwerp" in self.tournamentID_NAME_MAP[key]:
                Major_antwerp_ID = key

        remove_list = ["Sticker | Bart4k | Paris 2023", "Sticker | Complexity Gaming (Glitter) | Copenhagen 2024",]



        for name, ID in zip(hash_names, IDs):
            if "Sticker" in name:
                # count[len(name.split("|"))] += 1

                if len(name.split("|")) == 1:
                    pass #capsules
                elif len(name.split("|")) == 2:
                    pass #casual stickers
                elif len(name.split("|")) == 3: # and any(year in name for year in years) (Check not needed as there are only tournament stickers with 3 parts)
                    type_arr = name.split("|")
                    best_match_Name = ""
                    formated_name = name.split("|")[1].lower().lstrip(" ").split(" ")[0].strip(" ")

                    for player in self.playerName:
                        if player.lower() in formated_name and len(best_match_Name) < len(player) and len(player) == len(formated_name):

                            if formated_name not in remove_list:
                                best_match_Name = player
                                best_match_ID = self.playerID[self.playerName.index(player)]
                    if best_match_Name != "":
                        CosmeticID.append(ID)
                        playerID.append(best_match_ID)

                        # handle tournament ID (only two Majors were played in the dataset)
                        if "Stockholm" in type_arr[2]:
                            tournamentID.append(Major_stockholm_ID)
                        elif "Antwerp" in type_arr[2]:
                            tournamentID.append(Major_antwerp_ID)
                        else:
                            tournamentID.append(None)

                        playerStickerID.append(ID)

                        match = re.search(r"\((.*?)\)", type_arr[1])

                        if match:
                            condition.append(match.group(1))
                        else:
                            condition.append("Normal")

        print(condition)
        print(playerID)
        print(tournamentID)
        print(playerStickerID)

        query = """
                     INSERT INTO PlayerSticker (playerStickerID, condition, tournamentID, playerID, CosmeticID) VALUES (%s, %s, %s, %s, %s)
                """

        print(playerStickerID, condition, tournamentID, playerID, CosmeticID)

        print(len(playerStickerID), len(condition), len(tournamentID), len(playerID), len(CosmeticID))
        self.cur.executemany(query, zip(playerStickerID, condition, tournamentID, playerID, CosmeticID))

    def read_prices(self):
        # columns = ["spotterID", "playerID", "playerFrameID"]
        # self.write_csv(spotters, columns, "Spotter")
        mapper = self.mapper

        mapping_keys = list(mapper.keys())

        # read all prices
        item_history_path_prefix = "../Datasets/SteamMarketData/items/item"
        item_history_path_suffix = ".json"

        priceID = []
        amountSold = []
        date = []
        CosmeticID = []
        item_cost = []

        # load price history into database
        cnt = 1
        for item_number in mapping_keys:
            with open(item_history_path_prefix + str(item_number) + item_history_path_suffix, "r", encoding='UTF8') as file:
                price_history = json.load(file)
            file.close()
            if cnt % 50 == 0:
                print("loading pricehistory of item: " + str(cnt))
            cnt += 1
            for price in price_history['prices']:

                amountSold.append(price[2])
                date_str = self.convert_date(price[0])
                date.append(date_str)
                CosmeticID.append(item_number)
                item_cost.append(price[1])

        query = """
                             INSERT INTO Price (priceID, amountSold, date, price, CosmeticID) VALUES (%s, %s, %s, %s, %s)
                        """

        priceID = np.arange(1, len(amountSold)+1)

        print(len(priceID), len(amountSold), len(date), len(item_cost), len(CosmeticID))
        self.cur.executemany(query, zip(priceID, amountSold, date, item_cost, CosmeticID))
        print("quarry finished")

    def load_mapper(self):
        with open("../Datasets/SteamMarketData/mapping_all_new.json", "r", encoding='UTF8') as file:
            self.mapper = json.load(file)
        file.close()

    def convert_date(self, date):
        return int(self.date_parser(date.split(":")[0], self.DATE_FORMAT).timestamp())

    def commit(self):
        print("started commit")
        self.database.conn.commit()
        print("committed successfully")


    def get_weapon_names(self):
        """
        Get all weapon names from the database
        :return:
        """
        weapon_knife_string = "Zeus x27 • Bayonet • Bowie Knife • Butterfly Knife • Classic Knife • Falchion Knife • Flip Knife • Gut Knife • Huntsman Knife • Karambit • Kukri Knife • M9 Bayonet • Navaja Knife • Nomad Knife • Paracord Knife • Shadow Daggers • Skeleton Knife • Stiletto Knife • Survival Knife • Talon Knife • Ursus Knife"
        weapon_knife_string = weapon_knife_string.split(" • ")

        gloves = ["Sport Gloves", "Moto Gloves", "Hand Wraps", "Driver Gloves", "Specialist Gloves",
                  "Bloodhound Gloves", "Hydra Gloves", "Broken Fang Gloves"]

        weapon_pistol_string = "CZ75-Auto • Desert Eagle • Dual Berettas • Five-SeveN • Glock-18 • P2000 • P250 • R8 Revolver • Tec-9 • USP-S"
        weapon_pistol_string = weapon_pistol_string.split(" • ")

        weapon_heavy_string = "MAG-7 • Nova • Sawed-Off • XM1014 • M249 • Negev"
        weapon_heavy_string = weapon_heavy_string.split(" • ")

        weapon_smg_string = "MAC-10 • MP5-SD • MP7 • MP9 • P90 • PP-Bizon • UMP-45"
        weapon_smg_string = weapon_smg_string.split(" • ")

        weapon_rifle_string = "AK-47 • AUG • FAMAS • Galil AR • M4A1-S • M4A4 • SG 553 • AWP • G3SG1 • SCAR-20 • SSG 08"
        weapon_rifle_string = weapon_rifle_string.split(" • ")

        weapons = []
        weapons.extend(weapon_rifle_string)
        weapons.extend(weapon_smg_string)
        weapons.extend(weapon_heavy_string)
        weapons.extend(weapon_pistol_string)
        weapons.extend(weapon_knife_string)
        weapons.extend(gloves)
        return weapons

    def fuzzy_format_team_name(self, team_name: str) -> str:

        s = (team_name.lower()
                    .strip()
                    .replace(" ", "")
                    .replace("esports", "")
                    .replace("team", "")
                    .replace("neofrag", "")
                    .replace("gaming", "")
                    .replace("travis", "")
                    .replace("patsi", "")
                    .replace("patti", "")
                    .replace("golden", "")
                    .replace("gold", "")
                    .replace("glitter", "")
                    .replace("holo", "")
                    .replace("foil", "")
                    .replace("clan", "")
                    .replace("champion", "")
                    .replace("contender", "")
                    .replace("legend", "")
                    .replace("challenger", "")
                    .replace("spinx", "")
                    .replace("frozen", "")
                    .replace("krad", "")
                    .replace("rain", "")
                    .replace("fashr", "")
                    .replace("r3salt", "")
                    .replace("faven", "")
                    .replace("neo", "")
                    .replace("sense", "")
                    .replace("flamie", "")
                    .replace("flamez", "")
                    .replace("kaze", "")
                    .replace("spiidi", "")
                    .replace("mir", "")
                    .replace("frozen", "")
                    .replace("sixer", "")
                    .replace("nex", "")
                    .replace("erkast", "")
                    .replace("fame", "")
                    .replace("dreamhack", "")
                    .replace("mou", "")
                    .replace("shroud", "")
                    .replace("skadoodle", "")
                    .replace("karsa", "")
                    .replace("gade", "")
                    .replace("aerial", "")
                    .replace("furlan", "")
                    .replace("hazed", "")
                    .replace("hazed", "")
                    .replace("shara", "")
                    .replace("scream", "")
                    .replace("arya", "")
                    .replace("spaze", "")
                    .replace("hazed", "")
                    .replace("auman", "")
                    .replace("havoc", "")
                    .replace("neofrag", "")
                    .replace("bit", "")
                    .replace("espiranto", "")
                    .replace("neofrag", "")
                    .replace("monte", "")
                    .replace("yam", "")
                    .replace(".", "")
                    .replace("(", "")
                    .replace(")", "")
                    .replace("ggbet", ""))
        if "sk" == s:
            return ""
        if "hs" == s:
            return ""
        if "wolves" in s:
            return ""
        return s

    def get_weapon_ids(self):
        """
        Get all weapon IDs and names from the database
        """
        query = """
            SELECT weaponid, weaponname, weaponclass
            FROM Weapon
        """
        self.cur.execute(query)
        for id, weapon_name, weaponclass in self.cur.fetchall():
            self.weaponID.append(id)
            self.weaponName.append(weapon_name)
            self.weaponNAME_CLASS_MAP[weapon_name] = weaponclass
            self.weaponID_NAME_MAP[weapon_name] = id

    def get_team_ids(self):
        """
        Get all team IDs and names from the database
        """
        query = """
            SELECT teamID, teamname
            FROM Team
        """
        self.cur.execute(query)

        for id, team_name in self.cur.fetchall():
            self.teamID.append(id)
            self.teamName.append(team_name)
            self.teamID_NAME_MAP[id] = team_name

    def get_player_ids(self):
        """
        Get all player IDs and names from the database
        """
        query = """
            SELECT playerid, name
            FROM player

        """
        self.cur.execute(query)
        for id, name in self.cur.fetchall():
            self.playerID.append(id)
            self.playerName.append(name)
            self.playerID_NAME_MAP[id] = name


    def get_tournament_ids(self):
        """
        Get all player IDs and names from the database
        """
        query = """
            SELECT tournamentid, tournamentname
            FROM TOURNAMENT

        """
        self.cur.execute(query)
        for id, name in self.cur.fetchall():
            self.tournamentID.append(id)
            self.tournamentName.append(name)
            self.tournamentID_NAME_MAP[id] = name


    def set_keys(self):
        primary_key_constrains = [
            "ALTER TABLE Cosmetic ADD CONSTRAINT pk_Cosmetic PRIMARY KEY (CosmeticID);",
            "ALTER TABLE PlayerSticker ADD CONSTRAINT pk_playerSticker PRIMARY KEY (playerStickerID);",
            "ALTER TABLE Price ADD CONSTRAINT pk_price PRIMARY KEY (priceID);",
            "ALTER TABLE TeamSticker ADD CONSTRAINT pk_teamSticker PRIMARY KEY (teamStickerID);",
            "ALTER TABLE WeaponSkin ADD CONSTRAINT pk_weaponSkin PRIMARY KEY (weaponSkinID);"
        ]

        foreign_key_constains = [
            "ALTER TABLE PlayerSticker ADD CONSTRAINT fk_tournament FOREIGN KEY (tournamentID) REFERENCES Tournament(tournamentID);",
            "ALTER TABLE PlayerSticker ADD CONSTRAINT fk_player FOREIGN KEY (playerID) REFERENCES Player(playerID);",
            "ALTER TABLE PlayerSticker ADD CONSTRAINT fk_Cosmetic FOREIGN KEY (CosmeticID) REFERENCES Cosmetic(CosmeticID);",
            "ALTER TABLE TeamSticker ADD CONSTRAINT fk_tournament FOREIGN KEY (tournamentID) REFERENCES Tournament(tournamentID);",
            "ALTER TABLE TeamSticker ADD CONSTRAINT fk_team FOREIGN KEY (teamID) REFERENCES Team(teamID);",
            "ALTER TABLE TeamSticker ADD CONSTRAINT fk_Cosmetic FOREIGN KEY (CosmeticID) REFERENCES Cosmetic(CosmeticID);",
            "ALTER TABLE Price ADD CONSTRAINT fk_Cosmetic FOREIGN KEY (CosmeticID) REFERENCES Cosmetic(CosmeticID);",
            "ALTER TABLE WeaponSkin ADD CONSTRAINT fk_weapon FOREIGN KEY (game_weaponID) REFERENCES Weapon(weaponID);",
            "ALTER TABLE WeaponSkin ADD CONSTRAINT fk_Cosmetic FOREIGN KEY (CosmeticID) REFERENCES Cosmetic(CosmeticID);"
        ]

        for command in primary_key_constrains:
            try:
                print("Executing:", command)
                market.database.cur.execute(command)
            except Exception as e:
                print(e)
                self.commit()
            finally:
                pass

        for command in foreign_key_constains:
            try:
                print("Executing:", command)
                market.database.cur.execute(command)
            except Exception as e:
                print(e)
                self.commit()
            finally:
                pass

    def clear_key_constrains(self):
        drop_key_constraints = [
            "ALTER TABLE PlayerSticker DROP CONSTRAINT fk_tournament;",
            "ALTER TABLE PlayerSticker DROP CONSTRAINT fk_player;",
            "ALTER TABLE PlayerSticker DROP CONSTRAINT fk_Cosmetic;",
            "ALTER TABLE TeamSticker DROP CONSTRAINT fk_tournament;",
            "ALTER TABLE TeamSticker DROP CONSTRAINT fk_team;",
            "ALTER TABLE TeamSticker DROP CONSTRAINT fk_Cosmetic;",
            "ALTER TABLE Price DROP CONSTRAINT fk_Cosmetic;",
            "ALTER TABLE WeaponSkin DROP CONSTRAINT fk_weapon;",
            "ALTER TABLE WeaponSkin DROP CONSTRAINT fk_Cosmetic;",
            "ALTER TABLE Cosmetic DROP CONSTRAINT pk_Cosmetic;",
            "ALTER TABLE PlayerSticker DROP CONSTRAINT pk_playerSticker;",
            "ALTER TABLE Price DROP CONSTRAINT pk_price;",
            "ALTER TABLE TeamSticker DROP CONSTRAINT pk_teamSticker;",
            "ALTER TABLE WeaponSkin DROP CONSTRAINT pk_weaponSkin;"
        ]

        for command in drop_key_constraints:
            try:
                print("Executing:", command)
                market.database.cur.execute(command)
            except Exception as e:
                print(e)
                self.commit()
            finally:
                pass


if __name__ == '__main__':
    market = Market(True)
    market.read_cosmetics()
    market.read_WeaponSkin()
    market.read_TeamSticker()
    market.read_PlayerSticker()
    market.read_prices()
    market.set_keys()
    # market.clear_key_constrains()
    market.commit()