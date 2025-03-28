from __future__ import annotations

import csv
import logging
import os
import sys
import traceback

from thefuzz import fuzz

from database import Database
from collections import defaultdict
from typing import List
import ujson as json
import psycopg

logging.basicConfig(level=logging.INFO)

def progress_bar(current, total, bar_length=40):
    """
    Prints a progress bar and the currently reading game message.

    Args:
        current (int): The number of games parsed so far.
        total (int): The total number of games to parse.
        bar_length (int): The length of the progress bar in characters.
    """
    progress = current / total
    block = int(bar_length * progress)
    bar = '#' * block + '-' * (bar_length - block)

    # Print the progress bar and elapsed time
    sys.stdout.write(
        f"\rParsing games: |{bar}| {current}/{total} ({progress * 100:.2f}%) - "
        f"Currently reading game: {current}"
    )
    sys.stdout.flush()

class ESTA:
    """
    ESTA Dataset parser Class.
    """
    def __init__(self, start_gameid: int):
        # Database connection
        self.database = Database()

        self.database.init_files('../SQL/Tables')
        self.cur = self.database.cur

        # Local dictionary instead of key querying everytime
        # Dictionary for easy getting of id's and key list to not create that object each time its needed
        self.weaponIds = {}
        self.weaponKeys = []
        self.weaponClasses = {}
        self.weaponClassesKeys = []

        self.teamID = 1
        self.teamIds = {}
        self.teamKeys = []

        self.playerID = 1
        self.playerIds = {}
        self.playerKeys = []

        self.tournamentID = 1
        self.tournamentIds = {}
        self.tournamentKeys = []

        self.start_gameid = start_gameid

        # Local serial key holding instead of returning id's after insert
        self.gameID = 1
        self.gameRoundID = 1
        self.frameID = 1
        self.playerFrameID = 1

        self.serverVarID = 1

        self.teamGameSideID = 1
        self.playerGameSideID = 1

        self.matchmakingRanksID = 1

        self.spotterID = 1

        # Unique Id's
        self.killID = 1
        self.flashID = 1
        self.damageID = 1
        self.grenadeID = 1
        self.weaponFireID = 1
        self.bombEventID = 1

        self.projectileID = 1

    def write_csv(self,
                  data: List[dict[str: str | int | float | bool]],
                  keys: List[str],
                  name: str) -> None:
        """
        Write data to csv file
        :param data: Data to be written into csv file
        :param keys: Keys of data which should be written into csv file
        :param name: Name of the csv file
        """
        filtered_data = [
            {key: row[key] for key in keys if key in row}
            for row in data
        ]

        with open(f"{name}.csv", "w", newline="") as f:
            # Initialize DictWriter with the specified keys
            w = csv.DictWriter(f, keys)
            w.writeheader()
            w.writerows(filtered_data)

    def copy_csv(self, name: str, query: str) -> None:
        """
        Copy csv file to the database
        :param name: Name of the csv file
        :param query: Query to copy csv file into database
        """
        with open(f"{name}.csv", "r") as f:
            with self.cur.copy(f"COPY {query} FROM STDIN WITH CSV HEADER") as copy:
                while data := f.read(1024):
                    copy.write(data)

    def load_keys(self):
        keys = {
            "killID": "kill",
            "flashID": "flash",
            "damageID": "damage",
            "grenadeID": "grenade",
            "weaponFireID": "weaponFire",
            "bombEventID": "bombEvent",
            "gameRoundID": "gameRounds",
            "frameID": "frame",
            "playerFrameID": "playerFrame",
            "serverVarID": "serverVar",
            "teamGameSideID": "teamGameSide",
            "playerGameSideID": "playerGameSide",
            "spotterID": "spotter",
            "projectileID": "projectile",
            "matchmakingRanksID": "matchmakingRanks",
            "gameID": "game",
            "tournamentID": "tournament",
            "playerID": "player",
            "teamID": "team",
        }

        for id, table in keys.items():
            self.cur.execute(f"SELECT MAX({id}) FROM {table}")
            id_val = self.cur.fetchone()[0]
            if id_val is not None:
                if id == "gameID":
                    self.start_gameid = id_val + 1
                else:
                    setattr(self, id, id_val + 1)
            else:
                setattr(self, id, 1)
        self.gameID = 1

    def read_all_esta_demos(self):
        directory = '../Datasets/esta/data'
        # Reset all dictionaries
        self.cur.execute("SELECT weaponID, weaponName, weaponClass FROM Weapon")
        result = self.cur.fetchall()
        self.weaponIds = {row[1]: row[0] for row in result}
        self.weaponKeys = list(self.weaponIds.keys())
        self.weaponClasses = {row[1]: row[2] for row in result}
        self.weaponClassesKeys = list(self.weaponClasses.keys())

        self.cur.execute("SELECT teamID, teamName FROM Team")
        result = self.cur.fetchall()
        self.teamIds = {self.fuzzy_format_team_name(name): id for id, name in result}
        self.teamKeys = list(self.teamIds.keys())

        self.cur.execute("SELECT playerID, steamID FROM Player")
        result = self.cur.fetchall()
        self.playerIds = {steamID: id for id, steamID in result}
        self.playerKeys = list(self.playerIds.keys())

        self.cur.execute("SELECT tournamentID, tournamentName FROM Tournament")
        result = self.cur.fetchall()
        self.tournamentIds = {name: id for id, name in result}
        self.tournamentKeys = list(self.tournamentIds.keys())

        if self.start_gameid > 1:
            self.load_keys()

        self._read_demos_from_directory(f'{directory}/online')
        self._read_demos_from_directory(f'{directory}/lan')

        # Add all primary and foreign keys constraints
        self.database.init_file('../SQL/Keys/PrimaryKeys.sql')
        self.database.init_file('../SQL/Keys/ForeignKeys.sql')
        self.database.init_files('../SQL/Constraints')

    def _read_demos_from_directory(self, directory: str) -> None:
        try:
            for json_file in os.listdir(directory):
                if json_file.endswith('.json'):
                    if self.gameID >= self.start_gameid:
                        self.read_esta_demo(os.path.join(directory, json_file))
                    else:
                        print("Skipping game :", self.gameID, self.start_gameid)
                    self.gameID += 1
        except FileNotFoundError as e:
            logging.error(f"No more demos to read in {directory}: {e}")

    def read_esta_demo(self, path: str):
        """
        Read given path file into json dictionary and parse data
        :param path: Path of demo json file
        """
        with open(path, 'r') as demo_file:
            progress_bar(self.gameID, 1558)

            demo = json.load(demo_file)

            # Read Team Entity
            self.insert_team_id(demo['gameRounds'][0]['ctTeam'])
            self.insert_team_id(demo['gameRounds'][0]['tTeam'])

            # Read Tournament Entity
            self.read_tournament(demo['competitionName'])

            # Read ServerVar Entity
            self.read_servervars(demo['serverVars'])

            # Read Game Entity
            self.read_game(demo)

            # Read all game matchphases
            self.insert_matchphases("AnnouncementFinalRound", demo['matchPhases']['announcementFinalRound'])
            self.insert_matchphases("AnnouncementLastRoundHalf", demo['matchPhases']['announcementLastRoundHalf'])
            self.insert_matchphases("AnnouncementMatchStarted", demo['matchPhases']['announcementMatchStarted'])
            self.insert_matchphases("GameHalfEnded", demo['matchPhases']['gameHalfEnded'])
            self.insert_matchphases("MatchStart", demo['matchPhases']['matchStart'])
            self.insert_matchphases("TeamSwitch", demo['matchPhases']['teamSwitch'])
            self.insert_matchphases("WarmupChanged", demo['matchPhases']['warmupChanged'])

            # Read player ranks
            self.insert_matchmaking_ranks(demo['matchmakingRanks'])

            # Read all gamerounds Entities (gameRound, frames, events etc.)
            self.read_gameplay(demo['gameRounds'])

    def insert_spotters(self, spotters: List[dict]) -> None:
        """
        Read Spotter into database
        :param spotters: Spotter dictionary list
        """
        columns = ["spotterID", "playerID", "playerFrameID"]
        self.write_csv(spotters, columns, "Spotter")
        self.copy_csv("Spotter", f'Spotter ({", ".join(columns)})')

    def insert_matchmaking_ranks(self, matchmakingranks: List[dict]) -> None:
        """
        Read MatchmakingRank into database
        :param matchmakingranks: MatchmakingRank dictionary list
        """
        for matchmakingrank in matchmakingranks:
            matchmakingrank['gameID'] = self.gameID
            matchmakingrank['matchmakingRanksID'] = self.matchmakingRanksID
            matchmakingrank['playerID'] = self.playerIds[matchmakingrank['playerName']]
            self.matchmakingRanksID += 1

        columns = ["matchmakingRanksID", "rankOld", "rankNew", "rankChange", "winCount", "playerID", "gameID"]
        self.write_csv(matchmakingranks, columns, "MatchmakingRank")
        self.copy_csv("MatchmakingRank", f'MatchmakingRanks ({", ".join(columns)})')

    def insert_matchphases(self, type: str, ticks: List[int]):
        """
        Insert matchphases of type (tick, gameID) into database
        :param type: Type of matchphase
        :param ticks: List of ticks
        """
        columns = ["tick", "gameID"]
        data = []
        for tick in ticks:
            data.append({"tick": tick, "gameID": self.gameID})
        self.write_csv(data, columns, type)
        self.copy_csv(type, f'{type} ({", ".join(columns)})')

    def read_tournament(self, tournamentName: str):
        if tournamentName in self.tournamentKeys:
            return

        query = """
                    INSERT INTO Tournament (tournamentID, tournamentName) VALUES (%s, %s)
                """

        self.cur.execute(query, (self.tournamentID, tournamentName))

        self.tournamentIds[tournamentName] = self.tournamentID
        self.tournamentKeys.append(tournamentName)

        self.tournamentID += 1

    def read_player(self, playerName: str, steamID: int):
        if steamID in self.playerKeys:
            return

        query = """
                INSERT INTO Player (playerID, name, steamID) VALUES (%s, %s, %s)
            """

        self.cur.execute(query, (self.playerID, playerName, steamID))

        self.playerIds[steamID] = self.playerID
        self.playerKeys.append(steamID)

        self.playerID += 1

    def read_teamGameSide(self, team: str, side: str, game_round_id) -> int:
        query = """
                INSERT INTO TeamGameSide (teamGameSideID, side, teamID, gameRoundID)
                VALUES (%s, %s, %s, %s)
        """
        teamID = self.insert_team_id(team)
        self.cur.execute(query, (self.teamGameSideID, side, teamID, game_round_id))
        self.teamGameSideID += 1
        return self.teamGameSideID - 1

    def read_playerGameSide(self, steamId: str, teamGameSideID: int):
        query = """
                        INSERT INTO PlayerGameSide (playerGameSideID, teamGameSideID, playerID)
                        VALUES (%s, %s, %s)
                """

        self.cur.execute(query, (self.playerGameSideID, teamGameSideID, self.playerIds[steamId]))
        self.playerGameSideID += 1

    def read_game(self, game: dict):
        """
        Read Game into database
        :param game: Game dictionary
        """
        columns = [
            "gameID", "demoId", "playbackFramesCount", "playbackTicks", "parsedToFrameIdx",
            "tickRate", "matchId", "matchName", "hltvUrl",
            "matchDate", "tournamentID", "clientName", "mapName", "serverVarID"
        ]

        game['tournamentID'] = self.tournamentIds[game['competitionName']]
        game['gameID'] = self.gameID
        game['serverVarID'] = self.serverVarID
        game['matchDate'] = int(game['matchDate'] / 1000)

        self.write_csv([game], columns, "Game")
        self.copy_csv("Game", f'Game ({", ".join(columns)})')

    def read_servervars(self, data: dict) -> int:
        """
        Read ServerVars into database
        :param data: ServerVars dictionary
        :return: ServerVarID
        """
        search_query = """
                SELECT serverVarID FROM ServerVar
                WHERE cashBombPlanted = %(cashBombPlanted)s
                  AND cashBombDefused = %(cashBombDefused)s
                  AND bombTimer = %(bombTimer)s
                  AND buyTime = %(buyTime)s
                  AND freezeTime = %(freezeTime)s
                  AND roundRestartDelay = %(roundRestartDelay)s
                  AND roundTimeDefuse = %(roundTimeDefuse)s
                  AND roundTime = %(roundTime)s
                  AND cashTeamLoserBonusConsecutive = %(cashTeamLoserBonusConsecutive)s
                  AND maxRounds = %(maxRounds)s
                  AND timeoutsAllowed = %(timeoutsAllowed)s
                  AND cashTeamTWinBomb = %(cashTeamTWinBomb)s
                  AND coachingAllowed = %(coachingAllowed)s
                  AND cashWinElimination = %(cashWinElimination)s
                  AND cashWinTimeRunOut = %(cashWinTimeRunOut)s
                  AND cashWinDefuse = %(cashWinDefuse)s
                  AND cashPlayerKilledDefault = %(cashPlayerKilledDefault)s
                  AND cashTeamLoserBonus = %(cashTeamLoserBonus)s
                    """

        columns = [
            "cashBombPlanted", "cashBombDefused", "bombTimer", "buyTime", "freezeTime",
            "roundRestartDelay", "roundTimeDefuse", "roundTime", "cashTeamLoserBonusConsecutive",
            "maxRounds", "timeoutsAllowed", "cashTeamTWinBomb", "coachingAllowed",
            "cashWinElimination", "cashWinTimeRunOut", "cashWinDefuse",
            "cashPlayerKilledDefault", "cashTeamLoserBonus"
        ]

        insert_query = """
                        INSERT INTO ServerVar (
                            cashBombPlanted, cashBombDefused, bombTimer, buyTime, freezeTime, 
                            roundRestartDelay, roundTimeDefuse, roundTime, cashTeamLoserBonusConsecutive, 
                            maxRounds, timeoutsAllowed, cashTeamTWinBomb, coachingAllowed, 
                            cashWinElimination, cashWinTimeRunOut, cashWinDefuse, 
                            cashPlayerKilledDefault, cashTeamLoserBonus
                        ) VALUES (
                            %(cashBombPlanted)s, %(cashBombDefused)s, %(bombTimer)s, %(buyTime)s, %(freezeTime)s,
                            %(roundRestartDelay)s, %(roundTimeDefuse)s, %(roundTime)s, %(cashTeamLoserBonusConsecutive)s,
                            %(maxRounds)s, %(timeoutsAllowed)s, %(cashTeamTWinBomb)s, %(coachingAllowed)s,
                            %(cashWinElimination)s, %(cashWinTimeRunOut)s, %(cashWinDefuse)s,
                            %(cashPlayerKilledDefault)s, %(cashTeamLoserBonus)s
                        )
                        RETURNING serverVarID;
                    """

        self.cur.execute(search_query, data)
        server_var_id = self.cur.fetchone()

        if server_var_id is None:
            try:
                self.cur.execute(insert_query, data)
                server_var_id = self.cur.fetchone()
            except psycopg.errors.UniqueViolation as UV:
                # If serverVar conf already exists, ignore
                pass
        return server_var_id[0]

    def insert_player_frames(self, playerFrames: List[dict]) -> None:
        """
        Read PlayerFrame into database
        :param playerFrames: PlayerFrame dictionary list
        """
        columns = [
            "playerFrameID", "x", "y", "z", "velocityX", "velocityY", "velocityZ",
            "viewX", "viewY", "equipmentValue", "equipmentValueFreezetimeEnd",
            "equipmentValueRoundStart", "isReloading", "isWalking", "isPlanting",
            "isDefusing", "isAlive", "isInBuyZone", "isInBombZone", "isStanding",
            "isDucking", "isBlinded", "isAirborne", "activeWeaponID", "zoomLevel",
            "hasDefuse", "hasBomb", "hasHelmet", "totalUtility", "armor", "hp",
            "cashSpendTotal", "cashSpendThisRound", "cash", "frameID", "ping",
            "isUnDuckingInProgress", "isDuckingInProgress", "playerGameSideID"
        ]
        self.write_csv(playerFrames, columns, "PlayerFrame")
        self.copy_csv("PlayerFrame", f'PlayerFrame ({", ".join(columns)})')

    def insert_frames(self, frames: List[dict]) -> None:
        """
        Read Frame into database
        :param frames: Frame dictionary list
        """
        columns = [
            "frameID", "tick", "seconds", "clockTime", "gameRoundID", "bombX", "bombY", "bombZ"
        ]
        self.write_csv(frames, columns, "Frame")
        self.copy_csv("Frame", f'Frame ({", ".join(columns)})')

    def insert_kills(self, kills: List[dict]) -> None:
        """
        Read Kill into database
        :param kills: Kill dictionary list
        """
        columns = [
            "killID", "isSuicide", "attackerBlinded", "victimBlinded", "thruSmoke",
            "isTrade", "isHeadshot", "penetratedObjects", "isFirstKill", "isTeamkill",
            "attackerPlayerFrameID", "victimPlayerFrameID", "assisterPlayerFrameID", "tradedPlayerFrameID",
            "flashThrowerPlayerFrameID", "weaponID", "frameID"
        ]
        self.write_csv(kills, columns, "Kill")
        self.copy_csv("Kill", f'Kill ({", ".join(columns)})')

    def insert_damage(self, damages: List[dict]) -> None:
        """
        Read Damage into database
        :param damages: Damage dictionary list
        """
        columns = [
            "damageID", "isFriendlyFire", "hpDamageTaken",
            "attackerStrafe", "hpDamage", "armorDamage",
            "armorDamageTaken", "hitGroup", "attackerPlayerFrameID",
            "victimPlayerFrameID", "weaponID", "frameID"
        ]
        self.write_csv(damages, columns, "Damage")
        self.copy_csv("Damage", f'Damage ({", ".join(columns)})')

    def insert_weaponfires(self, weaponFires: List[dict]) -> None:
        """
        Read WeaponFire into database
        :param weaponFires: WeaponFire dictionary list
        """
        columns = ["weaponFireID", "playerFrameID", "playerStrafe", "weaponID", "frameID"]
        self.write_csv(weaponFires, columns, "WeaponFire")
        self.copy_csv("WeaponFire", f'WeaponFire ({", ".join(columns)})')

    def insert_bomb_event(self, bombEvents: List[dict]) -> None:
        """
        Read bombEvent into database
        :param bombEvents: BombEvent dictionary list
        """
        columns = ["bombEventID", "bombSite", "bombAction", "playerFrameID", "frameID"]
        self.write_csv(bombEvents, columns, "BombEvent")
        self.copy_csv("BombEvent", f'BombEvent ({", ".join(columns)})')

    def insert_grenades(self, grenades: List[dict]) -> None:
        """
        Read Grenade into database
        :param grenades: Grenade dictionary list
        """
        columns = ["grenadeID", "grenadeX", "grenadeY", "grenadeZ", "grenadeType", "throwFrameID", "destroyFrameID", "throwerPlayerFrameID", "entityId"]
        self.write_csv(grenades, columns, "Grenade")
        self.copy_csv("Grenade", f'Grenade ({", ".join(columns)})')

    def insert_flash(self, flashes: List[dict]) -> None:
        """
        Read Flash into database
        :param flashes: Flash dictionary list
        """
        columns = ["flashID", "flashDuration", "attackerPlayerFrameID", "playerFrameID", "frameID"]
        self.write_csv(flashes, columns, "Flash")
        self.copy_csv("Flash", f'Flash ({", ".join(columns)})')

    def insert_inventory(self, inventories: List[dict]) -> None:
        """
        Read Inventory into database.
        :param inventories: Inventory dictionary list
        """
        columns = ["playerFrameID", "weaponID", "ammoInReserve", "ammoInMagazine"]
        self.write_csv(inventories, columns, "Inventory")
        self.copy_csv("Inventory", f'Inventory ({", ".join(columns)})')

    def insert_game_round(self, gameRounds: List[dict]) -> None:
        """
        Read GameRound into database
        :param gameRounds: GameRound dictionary list
        :return:
        """
        columns = [
            "gameRoundID", "roundNum", "isWarmup", "startTick", "endTick",
            "bombPlantTick", "endOfficialTick", "roundEndReason", "ctRoundStartEqVal",
            "tScore", "endCTScore", "ctScore", "tRoundSpendMoney", "winningSide",
            "tFreezeTimeEndEqVal", "ctBuyType", "ctRoundSpendMoney",
            "tRoundStartEqVal", "ctFreezeTimeEndEqVal", "endTScore",
            "tBuyType", "freezeTimeEndTick", "gameID"
        ]
        self.write_csv(gameRounds, columns, "GameRounds")
        self.copy_csv("GameRounds", f'GameRounds ({", ".join(columns)})')


    def insert_smokes(self, smokes: List[dict]):
        """
        Read fires into Database
        :param smokes: Fires dictionary list
        :return:
        """
        columns = ["grenadeEntityID", "startTick", "x", "y", "z", "frameID"]
        self.write_csv(smokes, columns, "Smoke")
        self.copy_csv("Smoke", f'Smoke ({", ".join(columns)})')

    def insert_fires(self, fires: List[dict]):
        """
        Read fires into Database
        :param fires: Fires dictionary list
        :return:
        """
        columns = ["uniqueID", "x", "y", "z", "frameID"]
        self.write_csv(fires, columns, "Fire")
        self.copy_csv("Fire", f'Fire ({", ".join(columns)})')

    def insert_projectiles(self, projectiles: List[dict]):
        columns = ["projectileID", "projectileType", "x", "y", "z", "frameID"]
        self.write_csv(projectiles, columns, "Projectile")
        self.copy_csv("Projectile", f'Projectile ({", ".join(columns)})')

    def get_weapon_id(self, weapon_name: str, weapon_class: str = "") -> int:
        """
        Get weapon name from weapon dictionary
        :param weapon_class:
        :param weapon_name: Weapon name
        :return: Weapon id
        """
        if weapon_name in self.weaponKeys:
            if weapon_name in self.weaponClassesKeys and self.weaponClasses[weapon_name] == "" and weapon_class != "":
                self.cur.execute("UPDATE Weapon SET weaponClass = %s WHERE weaponName = %s", (
                weapon_class, weapon_name))
                self.weaponClasses[weapon_name] = weapon_class

            return self.weaponIds[weapon_name]

        # If not in dictionary, insert into database
        self.cur.execute("INSERT INTO Weapon (weaponName, weaponClass) VALUES (%s, %s) RETURNING weaponID", (weapon_name, weapon_class))
        weapon_id = self.cur.fetchone()[0]

        self.weaponIds[weapon_name] = weapon_id
        self.weaponKeys = list(self.weaponIds.keys())

        self.weaponClasses[weapon_name] = weapon_class
        self.weaponClassesKeys = list(self.weaponClasses.keys())

        return weapon_id

    def fuzzy_format_team_name(self, team_name: str) -> str:
        s = (team_name.lower()
                    .strip()
                    .replace(" ", "")
                    .replace("esports", "")
                    .replace("team", "")
                    .replace("clan", "")
                    .replace(".", "")
                    .replace("ggbet", ""))
        return s

    def insert_team_id(self, team_name: str) -> int:
        """
        Insert team into database. Returns team ID of the given team.
        :param team_name: Team name
        :return: Team ID
        """
        # Reformat team name to better check for duplicates
        team_name_formatted = self.fuzzy_format_team_name(team_name)

        # Fuzzy string matching to find team
        for team in self.teamKeys:
            if fuzz.ratio(team_name_formatted, team) > 85:
                return self.teamIds[team]

        query = """
            INSERT INTO Team (teamID, teamName) VALUES (%s, %s)
        """

        self.cur.execute(query, (self.teamID, team_name))

        self.teamIds[team_name_formatted] = self.teamID
        self.teamKeys.append(team_name_formatted)

        self.teamID += 1
        return self.teamID - 1

    def get_player_id(self, player_name: str, steamID) -> int:
        """
        Get player id from player dictionary
        :param player_name: Player name
        :return: Player id
        """
        if player_name in self.playerKeys:
            return self.playerIds[player_name]

        # If not in dictionary, insert into database
        self.cur.execute("INSERT INTO Player (name, steamID) VALUES (%s, %s) RETURNING playerID", (player_name, steamID))
        player_id = self.cur.fetchone()[0]

        self.playerIds[player_name] = player_id
        self.playerKeys = self.playerIds.keys()

        return player_id

    def events_in_frame(self, events: List[dict], key="tick") -> dict[int, List[dict]]:
        """
        :param events: Events list
        :return: dictionary with ticks as keys and event as value and dictionary keys
        The return datastructure looks like
        {
            <tick> : [{<event>}, ...],
            ...
        }
        """
        items = defaultdict(list)
        for event in events:
            items[event[key]].append(event)
        return items

    def read_gameplay(self, gameRounds: List[dict]):
        """
        Read Gameround into database. Parses all related frames, events etc. into the database.
        :param gameRounds: Dictionary of all data of game round
        """
        # All data lists for inserts
        spotters_insert_list: List[dict] = []
        player_frames_insert_list: List[dict] = []
        kills_insert_list: List[dict] = []
        bomb_events_insert_list: List[dict] = []
        damages_insert_list: List[dict] = []
        weapon_fires_insert_list: List[dict] = []
        grenades_insert_list: List[dict] = []
        flashes_insert_list: List[dict] = []
        inventories_insert_list: List[dict] = []

        smokes_insert_list: List[dict] = []
        fires_insert_list: List[dict] = []
        projectiles_insert_list: List[dict] = []

        player_game_side_list: List[dict] = []

        prev_player_frames_amount: int = 0
        try:
            for gameRound in gameRounds:
                last_tick = gameRound['frames'][-1]['tick']
                # Precalculate event interpolation to frames
                interpolated_kills = self.interpolate_ticks(gameRound['frames'], gameRound['kills'], 'tick')
                kills_lookup_dict = self.events_in_frame(gameRound['kills'])

                interpolated_bomb_events = self.interpolate_ticks(gameRound['frames'], gameRound['bombEvents'], 'tick')
                bomb_events_lookup_dict = self.events_in_frame(gameRound['bombEvents'])
                bomb_events_lookup_dict = {key:value for key, value in bomb_events_lookup_dict.items() if key <= last_tick}

                interpolated_damages = self.interpolate_ticks(gameRound['frames'], gameRound['damages'], 'tick')
                damages_lookup_dict = self.events_in_frame(gameRound['damages'])
                damages_lookup_dict = {key:value for key, value in damages_lookup_dict.items() if key <= last_tick}

                interpolated_weapon_fires = self.interpolate_ticks(gameRound['frames'], gameRound['weaponFires'], 'tick')
                weapon_fires_lookup_dict = self.events_in_frame(gameRound['weaponFires'])
                weapon_fires_lookup_dict = {key:value for key, value in weapon_fires_lookup_dict.items() if key <= last_tick}

                interpolated_grenades_throw = self.interpolate_ticks(gameRound['frames'], gameRound['grenades'], 'throwTick')
                interpolated_grenades_destroy = self.interpolate_ticks(gameRound['frames'], gameRound['grenades'], 'destroyTick')
                grenades_throw_lookup_dict = self.events_in_frame(gameRound['grenades'], 'throwTick')
                grenades_destroy_lookup_dict = self.events_in_frame(gameRound['grenades'], 'destroyTick')
                grenades_throw_lookup_dict = {key:value for key, value in grenades_throw_lookup_dict.items() if key <= last_tick}
                grenades_destroy_lookup_dict = {key:value for key, value in grenades_destroy_lookup_dict.items() if key <= last_tick}

                interpolated_flashes = self.interpolate_ticks(gameRound['frames'], gameRound['flashes'], 'tick')
                flashes_lookup_dict = self.events_in_frame(gameRound['flashes'])
                flashes_lookup_dict = {key:value for key, value in flashes_lookup_dict.items() if key <= last_tick}
                # Dictionary to hold playerGameSideID for each player in the round
                player_game_side: dict[str, int] = {}

                # Set primary keys
                gameRound['gameID'] = self.gameID
                gameRound['gameRoundID'] = self.gameRoundID
                self.gameRoundID += 1

                # if self.gameID == 21:
                #     print(gameRound['roundNum'], self.gameID)

                # Skip round if no player data
                if gameRound['ctSide']['players'] is None or gameRound['tSide']['players'] is None:
                    logging.warning(f"Round : {gameRound['roundNum']} has no player data. Skipping round.")
                    continue
                else:
                    # Read teams of round
                    ctGameSideID = self.read_teamGameSide(gameRound['ctTeam'], 'CT', gameRound['gameRoundID'])
                    tGameSideID = self.read_teamGameSide(gameRound['tTeam'], 'T', gameRound['gameRoundID'])

                    # Read players of round
                    for ct in gameRound['ctSide']['players']:
                        self.read_player(ct['playerName'], ct['steamID'])
                        # Set playerGameSideID for each player
                        player_game_side[ct['playerName']] = self.playerGameSideID
                        self.read_playerGameSide(ct['steamID'], ctGameSideID)
                    for t in gameRound['tSide']['players']:
                        self.read_player(t['playerName'], t['steamID'])
                        # Set playerGameSideID for each player
                        player_game_side[t['playerName']] = self.playerGameSideID
                        self.read_playerGameSide(t['steamID'], tGameSideID)

                    player_game_side_list += gameRound['ctSide']['players'] + gameRound['tSide']['players']

                # Read Frames
                for frame in gameRound['frames']:
                    frame_tick: int = frame['tick']

                    # Set primary keys
                    frame['frameID'] = self.frameID
                    frame['gameRoundID'] = gameRound['gameRoundID']
                    self.frameID += 1

                    # Read smoke entity
                    smokes_entities = []
                    for smoke in frame['smokes'] or []:
                        # Skip smoke if accidentally repeated in same frame
                        if smoke['grenadeEntityID'] in smokes_entities:
                            continue
                        smokes_entities.append(smoke['grenadeEntityID'])
                        smoke['frameID'] = frame['frameID']
                        smokes_insert_list.append(smoke)

                    # Read fire entity
                    fires_entities = []
                    for fire in frame['fires'] or []:
                        # Skip fire if accidentally repeated in same frame
                        if fire['uniqueID'] in fires_entities:
                            continue
                        fires_entities.append(fire['uniqueID'])
                        fire['frameID'] = frame['frameID']
                        fires_insert_list.append(fire)

                    # Read projectile entity
                    for projectile in frame['projectiles']:
                        projectile['frameID'] = frame['frameID']
                        projectile['projectileID'] = self.projectileID
                        self.projectileID += 1
                        projectiles_insert_list.append(projectile)

                    # Rename keys
                    frame['bombX'], frame['bombY'], frame['bombZ'] = frame['bomb']['x'], frame['bomb']['y'], frame['bomb']['z']

                    # Read player frames
                    player_frame_ids = {None: None}
                    if frame['t']['players'] is not None:
                        players_in_frame = frame['t']['players'] + frame['ct']['players']

                        prev_player_frames_amount = len(players_in_frame)

                        # Read player frames
                        for player in players_in_frame:
                            # If player in playerframes is not in player_game_side, remove player from playerframes
                            if player['name'] not in player_game_side.keys():
                                logging.warning(f"Playerframe referencing player not in current game. Ignoring playerframe")
                                players_in_frame.remove(player)
                                prev_player_frames_amount -= 1
                                continue

                            player['frameID'] = frame['frameID']
                            player['playerFrameID'] = self.playerFrameID
                            self.playerFrameID += 1

                            weapon_id = self.get_weapon_id(player['activeWeapon'], '')
                            player['activeWeaponID'] = weapon_id
                            player['playerGameSideID'] = player_game_side[player['name']]
                            player_frame_ids[player['steamID']] = player['playerFrameID']

                            inventory_weapons = []
                            # read player inventory
                            for inventory in player['inventory'] or []:
                                weapon_id = self.get_weapon_id(inventory['weaponName'], inventory['weaponClass'])
                                inventory['weaponID'] = weapon_id

                                # Check if weapon is already in player inventory. Sometimes weapons are duplicated.
                                if weapon_id in inventory_weapons:
                                    continue

                                inventory_weapons.append(weapon_id)

                                inventory['frameID'] = frame['frameID']
                                inventory['playerFrameID'] = player['playerFrameID']

                                inventories_insert_list.append(inventory)

                            for spotter in player['spotters'] or []:
                                spotter_dict = {
                                    "playerID": self.playerIds[player['steamID']],
                                    "playerFrameID": player['playerFrameID'],
                                    "spotterID": self.spotterID
                                }
                                spotters_insert_list.append(spotter_dict)
                                self.spotterID += 1

                            player_frames_insert_list.append(player)
                    else:
                        # If playerframes are None, reuse the last player frames, i.e. the playerframes from the previous frame
                        # Copy previous player frames
                        logging.warning("Current playerframe is none. Reconstructing playerframe from previous frame.")
                        last_player_frames = player_frames_insert_list[-prev_player_frames_amount:].copy()
                        for old_player in last_player_frames:
                            # Copy dictionary
                            new_player = old_player.copy()

                            # Set new keys
                            new_player['playerFrameID'] = self.playerFrameID
                            new_player['frameID'] = frame['frameID']
                            player_frame_ids[new_player['steamID']] = new_player['playerFrameID']
                            player_frames_insert_list.append(new_player)
                            self.playerFrameID += 1

                    # Read Kill if in frame
                    if frame_tick in interpolated_kills:
                        for kill in kills_lookup_dict[frame_tick] or []:
                            # Skip kill if attackerName is None -> Error when parsing
                            if kill['attackerName'] is None and kill['weapon'] != 'C4' and kill['weapon'] != 'World':
                                logging.warning(f"Kill 'attackername' is none. Ignoring Kill")
                                #kills_lookup_dict[frame_tick].pop(i)
                                continue

                            # Skip kill if player is not in player_frame_ids -> Error when parsing
                            # Sometimes wrong player is used as event -> throw away event because it's useless
                            if kill['attackerSteamID'] not in player_frame_ids.keys():
                                logging.warning(f"Kill referencing non existing player in current frame. Removing kill")
                                #kills_lookup_dict[frame_tick].pop(i)
                                continue

                            # Set primary key
                            kill['killID'] = self.killID
                            self.killID += 1

                            # Set foreign keys
                            kill['frameID'] = frame['frameID']
                            steam_ids = player_frame_ids.keys()

                            if kill['attackerSteamID'] in steam_ids:
                                kill['attackerPlayerFrameID'] = player_frame_ids[kill['attackerSteamID']]
                            elif kill['attackerSteamID'] is not None:
                                logging.warning("Kill 'attackersteamid' doesn't exist in current playerframe steamid's. Setting to None")
                                kill['attackerPlayerFrameID'] = None

                            if kill['victimSteamID'] in steam_ids:
                                kill['victimPlayerFrameID'] = player_frame_ids[kill['victimSteamID']]
                            elif kill['victimSteamID'] is not None:
                                logging.warning("Kill 'victimSteamID' doesn't exist in current playerframe steamid's. Setting to None")
                                kill['victimPlayerFrameID'] = None

                            if kill['assisterSteamID'] in steam_ids:
                                kill['assisterPlayerFrameID'] = player_frame_ids[kill['assisterSteamID']]
                            elif kill['assisterSteamID'] is not None:
                                logging.warning("Kill 'assisterSteamID' doesn't exist in current playerframe steamid's. Setting to None")
                                kill['assisterPlayerFrameID'] = None

                            if kill['playerTradedSteamID'] in steam_ids:
                                kill['tradedPlayerFrameID'] = player_frame_ids[kill['playerTradedSteamID']]
                            elif kill['playerTradedSteamID'] is not None:
                                logging.warning("Kill 'playerTradedSteamID' doesn't exist in current playerframe steamid's. Setting to None")
                                kill['tradedPlayerFrameID'] = None

                            if kill['flashThrowerSteamID'] in steam_ids:
                                kill['flashThrowerPlayerFrameID'] = player_frame_ids[kill['flashThrowerSteamID']]
                            elif kill['flashThrowerSteamID'] is not None:
                                logging.warning("Kill 'flashThrowerSteamID' doesn't exist in current playerframe steamid's. Setting to None")
                                kill['flashThrowerPlayerFrameID'] = None

                            weapon_id = self.get_weapon_id(kill['weapon'])
                            kill['weaponID'] = self.weaponIds[kill['weapon']]
                            kills_insert_list.append(kill)

                    # Read BombEvent if in frame
                    if frame_tick in interpolated_bomb_events:
                        for bomb_event in bomb_events_lookup_dict[frame_tick] or []:
                            # Skip bomb event if playerName is None -> Error when parsing
                            if bomb_event['playerName'] is None:
                                logging.warning("BombEvent playerName is None. Ignoring BombEvent")
                                continue

                            # Set primary key
                            bomb_event['bombEventID'] = self.bombEventID
                            self.bombEventID += 1

                            # Set foreign keys
                            bomb_event['frameID'] = frame['frameID']
                            bomb_event['playerFrameID'] = player_frame_ids[bomb_event['playerSteamID']]

                            bomb_events_insert_list.append(bomb_event)

                    if frame_tick in interpolated_damages:
                        for damage in damages_lookup_dict[frame_tick] or []:
                            # Skip damage event if attackerName is None -> Error when parsing
                            if damage['attackerName'] is None and damage['weapon'] != 'C4' and damage['weapon'] != 'World':
                                logging.warning("Damage attackerName is None. Ignoring Damage")
                                continue

                            # Set primary key
                            damage['damageID'] = self.damageID
                            self.damageID += 1

                            # Set foreign keys
                            damage['frameID'] = frame['frameID']
                            if damage['attackerSteamID'] in player_frame_ids.keys():
                                damage['attackerPlayerFrameID'] = player_frame_ids[damage['attackerSteamID']]
                            elif damage['attackerSteamID'] is not None:
                                logging.warning("Damage 'attackerSteamID' doesn't exist in current playerframe steamid's. Setting to None")
                                damage['attackerPlayerFrameID'] = None

                            if damage['victimSteamID'] in player_frame_ids.keys():
                                damage['victimPlayerFrameID'] = player_frame_ids[damage['victimSteamID']]
                            elif damage['victimSteamID'] is not None:
                                logging.warning("Damage 'victimSteamID' doesn't exist in current playerframe steamid's. Setting to None")
                                damage['victimPlayerFrameID'] = None

                            weapon_id = self.get_weapon_id(damage['weapon'])
                            damage['weaponID'] = weapon_id
                            damages_insert_list.append(damage)

                    if frame_tick in interpolated_weapon_fires:
                        for weapon_fire in weapon_fires_lookup_dict[frame_tick] or []:
                            # Skip weaponFire event if playerName is None -> Error when parsing
                            if weapon_fire['playerName'] is None:
                                logging.warning("WeaponFire playerName is None. Ignoring WeaponFire")
                                continue

                            # Set primary key
                            weapon_fire['weaponFireID'] = self.weaponFireID
                            self.weaponFireID += 1

                            # Set foreign keys
                            weapon_fire['frameID'] = frame['frameID']

                            if weapon_fire['playerSteamID'] in player_frame_ids.keys():
                                weapon_fire['playerFrameID'] = player_frame_ids[weapon_fire['playerSteamID']]
                            elif weapon_fire['playerSteamID'] is not None:
                                logging.warning("Damage 'victimSteamID' doesn't exist in current playerframe steamid's. Setting to None")
                                weapon_fire['playerSteamID'] = None

                            weapon_id = self.get_weapon_id(weapon_fire['weapon'])
                            weapon_fire['weaponID'] = weapon_id
                            weapon_fires_insert_list.append(weapon_fire)

                    if frame_tick in interpolated_grenades_throw:
                        for grenade in grenades_throw_lookup_dict[frame_tick] or []:
                            # Skip grenade event if throwerName is None -> Error when parsing
                            if grenade['throwerName'] is None:
                                logging.warning("Grenade throwerName is None. Ignoring Grenade")
                                continue

                            # Set primary key
                            grenade['grenadeID'] = self.grenadeID
                            self.grenadeID += 1

                            # Set foreign keys
                            grenade['throwFrameID'] = frame['frameID']
                            if grenade['throwerSteamID'] in player_frame_ids.keys():
                                grenade['throwerPlayerFrameID'] = player_frame_ids[grenade['throwerSteamID']]
                            elif grenade['throwerSteamID'] is not None:
                                logging.warning("Grenade 'throwerSteamID' doesn't exist in current playerframe steamid's. Setting to None")
                                grenade['throwerPlayerFrameID'] = None

                    if frame_tick in interpolated_grenades_destroy:
                        for grenade in grenades_destroy_lookup_dict[frame_tick] or []:
                            # Skip grenade event if throwerName is None -> Error when parsing
                            if grenade['throwerName'] is None:
                                logging.warning("Grenade throwerName is None. Ignoring Grenade")
                                continue

                            # Set foreign key
                            grenade['destroyFrameID'] = frame['frameID']
                            grenades_insert_list.append(grenade)

                    if frame_tick in interpolated_flashes:
                        for flash in flashes_lookup_dict[frame_tick] or []:
                            # Skip flash event if attackerPlayerName is None -> Error when parsing
                            if flash['attackerName'] is None:
                                logging.warning("Flash attackerName is None. Ignoring Flash")
                                continue

                            # Set primary key
                            flash['flashID'] = self.flashID
                            self.flashID += 1

                            # Set foreign keys
                            flash['frameID'] = frame['frameID']
                            if flash['attackerSteamID'] in player_frame_ids.keys():
                                flash['attackerPlayerFrameID'] = player_frame_ids[flash['attackerSteamID']]
                            elif flash['attackerSteamID'] is not None:
                                logging.warning("Flash 'attackerSteamID' doesn't exist in current playerframe steamid's. Setting to None")
                                flash['attackerPlayerFrameID'] = None

                            if flash['playerSteamID'] in player_frame_ids.keys():
                                flash['playerFrameID'] = player_frame_ids[flash['playerSteamID']]
                            elif flash['playerSteamID'] is not None:
                                logging.warning("Flash 'playerSteamID' doesn't exist in current playerframe steamid's. Setting to None")
                                flash['playerFrameID'] = None
                            flashes_insert_list.append(flash)

                self.insert_frames(gameRound['frames'])

            self.insert_fires(fires_insert_list)
            self.insert_smokes(smokes_insert_list)
            self.insert_projectiles(projectiles_insert_list)
            self.insert_game_round(gameRounds)
            self.insert_inventory(inventories_insert_list)
            self.insert_player_frames(player_frames_insert_list)
            self.insert_kills(kills_insert_list)
            self.insert_bomb_event(bomb_events_insert_list)
            self.insert_damage(damages_insert_list)
            self.insert_weaponfires(weapon_fires_insert_list)
            self.insert_flash(flashes_insert_list)
            self.insert_grenades(grenades_insert_list)
            self.insert_spotters(spotters_insert_list)
            self.database.conn.commit()
        except Exception as E:
            self.database.conn.rollback()
            print(traceback.format_exc())
            print(E)
            print("Error at game : ", self.gameID)
            quit()
        finally:
            # Delete temporary csv files
            for file in os.listdir('.'):
                if file.endswith(".csv"):
                    os.remove(file)

    def interpolate_ticks(self, frames: List[dict], events: List[dict], key: str) -> List[int]:
        """
        Interpolate ticks such that the event tick belongs to the closest frame
        :param frames: List of frames
        :param events: List of events
        :param key: Dictionary key of event where tick is located
        :return: List of ticks at which event happened
        """
        # Return on empty events list
        if len(events) == 0:
            return []
        event_ticks: List[int] = []
        event_count = 0
        for event in events:
            event_key = event[key]

            for i in range(len(frames)):

                tick_prev = frames[i - 1]['tick'] if i > 0 else -sys.maxsize
                tick_curr = frames[i]['tick']
                tick_next = frames[i + 1]['tick'] if i + 1 < len(frames) else sys.maxsize

                if tick_prev <= event_key <= tick_next:

                    dist_prev = abs(tick_prev - event_key)
                    dist_curr = abs(tick_curr - event_key)
                    dist_next = abs(tick_next - event_key)

                    if dist_curr <= dist_prev and dist_curr <= dist_next:
                        event[key] = tick_curr
                        event_ticks.append(tick_curr)
                        break
                    elif dist_next < dist_prev:
                        event[key] = tick_next
                        event_ticks.append(tick_next)
                        break
                    else:
                        event[key] = tick_prev
                        event_ticks.append(tick_prev)
                        break

        return event_ticks

if __name__ == '__main__':
    esta = ESTA(1)
    esta.read_all_esta_demos()
