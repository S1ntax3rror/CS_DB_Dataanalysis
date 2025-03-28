from __future__ import annotations

import re
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.lines as mlines

from Scripts.database import Database
from plotting_functions import *
import seaborn as sns

sns.set()
# https://zenodo.org/records/3381072
sns.set_palette(['#117733', '#44AA99', '#88CCEE', '#DDDDDD', '#AA4499', '#882255', '#CC6677', '#999933', '#DDCC77', '#332288'])
db = Database()
query = db.query

holiday_dates = {
    "Easter_14": '2014-04-20 12:00:00',
    "Easter_15": '2015-04-05 12:00:00',
    "Easter_16": '2016-03-27 12:00:00',
    "Easter_17": '2017-04-16 12:00:00',
    "Easter_18": '2018-04-01 12:00:00',
    "Easter_19": '2019-03-24 12:00:00',
    "Easter_20": '2020-04-12 12:00:00',
    "Easter_21": '2021-04-04 12:00:00',
    "Easter_22": '2022-04-17 12:00:00',
    "Easter_23": '2023-04-09 12:00:00',
    "Christmas_14" : '2014-12-24 12:00:00',
    "Christmas_15" : '2015-12-24 12:00:00',
    "Christmas_16" : '2016-12-24 12:00:00',
    "Christmas_17" : '2017-12-24 12:00:00',
    "Christmas_18" : '2018-12-24 12:00:00',
    "Christmas_19" : '2019-12-24 12:00:00',
    "Christmas_20" : '2020-12-24 12:00:00',
    "Christmas_21" : '2021-12-24 12:00:00',
    "Christmas_22" : '2022-12-24 12:00:00',
    "Christmas_23" : '2023-12-24 12:00:00',
    "Chinese_new_year_14" : "2014-01-31 12:00:00",
    "Chinese_new_year_15" : "2015-02-19 12:00:00",
    "Chinese_new_year_16" : "2016-02-08 12:00:00",
    "Chinese_new_year_17" : "2017-01-28 12:00:00",
    "Chinese_new_year_18" : "2018-02-16 12:00:00",
    "Chinese_new_year_19" : "2019-02-05 12:00:00",
    "Chinese_new_year_20" : "2020-01-25 12:00:00",
    "Chinese_new_year_21" : "2021-02-12 12:00:00",
    "Chinese_new_year_22" : "2022-02-01 12:00:00",
    "Chinese_new_year_23" : "2023-01-22 12:00:00",
    "Chinese_new_year_24": "2024-02-10 12:00:00"
}

eventdates = {
    "Steam_Summer_Sale_20_start": '2020-06-25 12:00:00',
    "Steam_Summer_Sale_20_end": '2020-07-09 12:00:00',
    "Steam_Autumn_Sale_20_start": '2020-11-25 12:00:00',
    "Steam_Autumn_Sale_20_end": '2020-12-01 12:00:00',
    "Steam_Winter_Sale_20_start": '2020-12-22 12:00:00',
    "Steam_Winter_Sale_20_end": '2022-1-05 12:00:00',
    "Steam_Summer_Sale_21_start": '2021-06-24 12:00:00',
    "Steam_Summer_Sale_21_end": '2021-07-08 12:00:00',
    "Steam_Autumn_Sale_21_start": '2021-11-24 12:00:00',
    "Steam_Autumn_Sale_21_end": '2021-12-01 12:00:00',
    "Steam_Winter_Sale_21_start": '2021-12-22 12:00:00',
    "Steam_Winter_Sale_21_end": '2022-01-05 12:00:00',
    "Steam_Summer_Sale_22_start": '2022-06-23 12:00:00',
    "Steam_Summer_Sale_22_end": '2022-07-07 12:00:00',
    "Steam_Autumn_Sale_22_start": '2022-11-22 12:00:00',
    "Steam_Autumn_Sale_22_end": '2022-11-29 12:00:00',
    "Steam_Winter_Sale_22_start": '2022-12-22 12:00:00',
    "Steam_Winter_Sale_22_end": '2023-01-05 12:00:00',
}

tournament_dates = {
    "Intel_Extreme_Masters_Rio_Major_2022": ['2022-10-31 00:00:00', '2022-11-13 23:59:59'],

    "PGL_Major_Antwerp_2022": ['2022-05-09 00:00:00', '2022-05-22 23:59:59'],

    "PGL_Major_Stockholm_2021": ['2021-10-26 00:00:00', '2021-11-07 23:59:59'],

    "StarLadder_Berlin_Major_2019": ['2019-08-23 00:00:00', '2019-09-08 23:59:59'],

    "Intel_Extreme_Masters_XIII_Katowice_Major_2019": ['2019-02-13 00:00:00', '2019-03-03 23:59:59'],

    "FACEIT_Major_London_2018": ['2018-09-05 00:00:00', '2018-09-23 23:59:59'],

    "ELEAGUE_Major_Boston_2018": ['2018-01-12 00:00:00', '2018-01-28 23:59:59'],

    "PGL_Major_Kraków_2017": ['2017-07-16 00:00:00', '2017-07-23 23:59:59'],

    "ELEAGUE_Major_Atlanta_2017": ['2017-01-22 00:00:00', '2017-01-29 23:59:59'],

    "ESL_One_Cologne_2016": ['2016-07-05 00:00:00', '2016-07-10 23:59:59'],

    "MLG_Major_Championship_Columbus_2016": ['2016-03-29 00:00:00', '2016-04-03 23:59:59'],

    "DreamHack_Open_Cluj_Napoca_2015": ['2015-10-28 00:00:00', '2015-11-01 23:59:59'],

    "ESL_One_Cologne_2015": ['2015-08-20 00:00:00', '2015-08-23 23:59:59'],

    "ESL_One_Katowice_2015": ['2015-03-12 00:00:00', '2015-03-15 23:59:59'],

    "DreamHack_Winter_2014": ['2014-11-27 00:00:00', '2014-11-29 23:59:59'],

    "ESL_One_Cologne_2014": ['2014-08-14 00:00:00', '2014-08-17 23:59:59'],

    "ESL_Major_Series_One_Katowice_2014": ['2014-03-13 00:00:00', '2014-03-16 23:59:59'],

    "DreamHack_Winter_2013": ['2013-11-28 00:00:00', '2013-11-30 23:59:59'],
}

def plot_price_amount_and_performance(team_name: str):
    df_team_stickers = query(f"""
        SELECT C.name, C.cosmeticid FROM cosmetic C
            JOIN teamsticker TS ON C.cosmeticid = TS.cosmeticid
            JOIN team T ON TS.teamid = T.teamid
            WHERE teamname = '{team_name}'
    """)

    df_games_data = query(f"""
            SELECT
                GR.gameid,
                endtscore,
                endctscore,
                matchdate,
                MAX(CASE WHEN side = 'T' THEN teamname END) AS T,
                MAX(CASE WHEN side = 'CT' THEN teamname END) AS CT
            FROM gamerounds GR
            JOIN (
                SELECT G.gameid, G.matchdate, MAX(gameroundid) as gameroundid
                FROM game G
                JOIN public.gamerounds g2 ON G.gameid = g2.gameid
                GROUP BY G.gameid, G.matchdate
            ) LASTROUND
            ON LASTROUND.gameroundid = GR.gameroundid
            JOIN public.teamgameside t ON GR.gameroundid = t.gameroundid
            JOIN public.team t2 ON t.teamid = t2.teamid
            WHERE teamname = '{team_name}'
            GROUP BY GR.gameid, endtscore, endctscore, matchdate
            ORDER BY gameid ASC
        """)

    df_games_data['matchdate'] = df_games_data['matchdate'].apply(datetime.fromtimestamp)
    df_team_games = df_games_data[(df_games_data['t'] == team_name) | (df_games_data['ct'] == team_name)]

    Wins = []
    Loses = []
    for i in range(len(df_team_games)):
        row = df_team_games.iloc[i]
        if ((row['endtscore'] > row['endctscore']) and row['t'] == team_name) or (
                (row['endtscore'] < row['endctscore']) and row['ct'] == team_name):
            Wins.append(row['matchdate'])
        else:
            Loses.append(row['matchdate'])

    for index, row in df_team_stickers.iterrows():
        df_team_sticker_price_history = query(f"""
                SELECT amountsold, price, date FROM price
                    JOIN cosmetic C ON price.cosmeticid = C.cosmeticid
                    WHERE C.cosmeticid = {row['cosmeticid']}
            """)
        df_team_sticker_price_history['date'] = df_team_sticker_price_history['date'].apply(datetime.fromtimestamp)

        min_x = min(df_team_sticker_price_history['date'])
        max_x = max(max(Wins), max(Loses))
        min_game = min(min(Wins), min(Loses))
        if min_game > min_x:
            min_x = min_game

        ymin_price = df_team_sticker_price_history['price'].min()
        ymax_price = df_team_sticker_price_history['price'].max()

        ymin_sold = df_team_sticker_price_history['amountsold'].min()
        ymax_sold = df_team_sticker_price_history['amountsold'].max()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8))
        fig.suptitle(row['name'])

        ax1.set_title('Price history')
        ax1.set_xlabel('Date (YYYY-MM)')
        ax1.set_ylabel('Price (CHF)')
        ax1.set_xlim([min_x, max_x])
        ax1.set_ylim([ymin_price, ymax_price])
        ax1.vlines(x=Wins, color='#FF7F0E', alpha=1, label='Win', ymin=ymin_price - 10, ymax=ymax_price + 10)
        ax1.vlines(x=Loses, color='tomato', alpha=1, label='Lose', ymin=ymin_price - 10, ymax=ymax_price + 10)
        sns.lineplot(df_team_sticker_price_history, x='date', y='price', ax=ax1, linewidth=2)

        ax2.set_title('Amount sold history')
        ax2.set_xlabel('Date (YYYY-MM)')
        ax2.set_ylabel('Amount sold')
        ax2.set_xlim([min_x, max_x])
        ax2.set_ylim([ymin_sold, ymax_sold])
        ax2.vlines(x=Wins, color='limegreen', alpha=1, label='Win', ymin=ymin_sold - 10, ymax=ymax_sold + 10)
        ax2.vlines(x=Loses, color='tomato', alpha=1, label='Lose', ymin=ymin_sold - 10, ymax=ymax_sold + 10)
        sns.lineplot(df_team_sticker_price_history, x='date', y='amountsold', ax=ax2, linewidth=2)

        fig.tight_layout()
        fig.show()

def plot_different_quality_stickers(team_name: str):
    df_team_sticker_tournament = query(f"""
        SELECT C.name, C.cosmeticid, TN.tournamentid FROM cosmetic C
            JOIN teamsticker TS ON C.cosmeticid = TS.cosmeticid
            JOIN team T ON TS.teamid = T.teamid
            JOIN tournament TN ON TS.tournamentid = TN.tournamentid
            WHERE teamname = '{team_name}'
            ORDER BY TN.tournamentid
    """)

    df_team_sticker_tournament_grouped = df_team_sticker_tournament.groupby('tournamentid')
    df_team_sticker_tournament_first = df_team_sticker_tournament_grouped.get_group(20)
    df_games_data = query(f"""
                SELECT
                    GR.gameid,
                    endtscore,
                    endctscore,
                    matchdate,
                    MAX(CASE WHEN side = 'T' THEN teamname END) AS T,
                    MAX(CASE WHEN side = 'CT' THEN teamname END) AS CT
                FROM gamerounds GR
                JOIN (
                    SELECT G.gameid, G.matchdate, MAX(gameroundid) as gameroundid
                    FROM game G
                    JOIN public.gamerounds g2 ON G.gameid = g2.gameid
                    GROUP BY G.gameid, G.matchdate
                ) LASTROUND
                ON LASTROUND.gameroundid = GR.gameroundid
                JOIN public.teamgameside t ON GR.gameroundid = t.gameroundid
                JOIN public.team t2 ON t.teamid = t2.teamid
                WHERE teamname = '{team_name}'
                GROUP BY GR.gameid, endtscore, endctscore, matchdate
                ORDER BY gameid ASC
            """)

    df_games_data['matchdate'] = df_games_data['matchdate'].apply(datetime.fromtimestamp)
    df_team_games = df_games_data[(df_games_data['t'] == team_name) | (df_games_data['ct'] == team_name)]

    Wins = []
    Loses = []
    for i in range(len(df_team_games)):
        row = df_team_games.iloc[i]
        if ((row['endtscore'] > row['endctscore']) and row['t'] == team_name) or (
                (row['endtscore'] < row['endctscore']) and row['ct'] == team_name):
            Wins.append(row['matchdate'])
        else:
            Loses.append(row['matchdate'])

    fig, ax = plt.subplots(1, 1, figsize=(15, 8))
    for index, row in df_team_sticker_tournament_first.iterrows():
        df_team_sticker_price_history = query(f"""
                        SELECT amountsold, price, date FROM price
                            JOIN cosmetic C ON price.cosmeticid = C.cosmeticid
                            WHERE C.cosmeticid = {row['cosmeticid']}
                    """)
        df_team_sticker_price_history['date'] = df_team_sticker_price_history['date'].apply(datetime.fromtimestamp)

        ax.set_xlabel('Date (YYYY-MM)')
        ax.set_ylabel('Price (CHF)')
        ax.set_xlim([np.min(df_team_sticker_price_history['date']), np.max(df_team_sticker_price_history['date'])])
        sns.lineplot(df_team_sticker_price_history, x='date', y='price', ax=ax, label=f'{row["name"]}')

    fig.show()

def sticker_total_change(team_name: str):
    df_team_sticker_tournament = query(f"""
            SELECT C.name, C.cosmeticid, TN.tournamentid FROM cosmetic C
                JOIN teamsticker TS ON C.cosmeticid = TS.cosmeticid
                JOIN team T ON TS.teamid = T.teamid
                JOIN tournament TN ON TS.tournamentid = TN.tournamentid
                WHERE teamname = '{team_name}'
                ORDER BY TN.tournamentid
        """)

    df_team_sticker_tournament_grouped = df_team_sticker_tournament.groupby('tournamentid')
    for name, group in df_team_sticker_tournament_grouped:
        df_team_sticker_tournament_first = df_team_sticker_tournament_grouped.get_group(name)
        df_games_data = query(f"""
                        SELECT
                            GR.gameid,
                            endtscore,
                            endctscore,
                            matchdate,
                            MAX(CASE WHEN side = 'T' THEN teamname END) AS T,
                            MAX(CASE WHEN side = 'CT' THEN teamname END) AS CT
                        FROM gamerounds GR
                        JOIN (
                            SELECT G.gameid, G.matchdate, MAX(gameroundid) as gameroundid
                            FROM game G
                            JOIN public.gamerounds g2 ON G.gameid = g2.gameid
                            GROUP BY G.gameid, G.matchdate
                        ) LASTROUND
                        ON LASTROUND.gameroundid = GR.gameroundid
                        JOIN public.teamgameside t ON GR.gameroundid = t.gameroundid
                        JOIN public.team t2 ON t.teamid = t2.teamid
                        WHERE teamname = '{team_name}'
                        GROUP BY GR.gameid, endtscore, endctscore, matchdate
                        ORDER BY gameid ASC
                    """)

        df_games_data['matchdate'] = df_games_data['matchdate'].apply(datetime.fromtimestamp)
        df_team_games = df_games_data[(df_games_data['t'] == team_name) | (df_games_data['ct'] == team_name)]

        Wins = []
        Loses = []
        for i in range(len(df_team_games)):
            row = df_team_games.iloc[i]
            if ((row['endtscore'] > row['endctscore']) and row['t'] == team_name) or (
                    (row['endtscore'] < row['endctscore']) and row['ct'] == team_name):
                Wins.append(row['matchdate'])
            else:
                Loses.append(row['matchdate'])

        min_x = min(min(Wins), min(Loses))
        max_x = max(max(Wins), max(Loses))

        dataframes = []

        fig, ax = plt.subplots(1, 1, figsize=(15, 5))
        for index, row in df_team_sticker_tournament_first.iterrows():
            df_team_sticker_price_history = query(f"""
                                SELECT amountsold, price, date FROM price
                                    JOIN cosmetic C ON price.cosmeticid = C.cosmeticid
                                    WHERE C.cosmeticid = {row['cosmeticid']}
                                    AND date BETWEEN {datetime.timestamp(min_x)} AND {datetime.timestamp(max_x)}
                            """)
            df_team_sticker_price_history['date'] = df_team_sticker_price_history['date'].apply(datetime.fromtimestamp)
            df_team_sticker_price_history['price'] = df_team_sticker_price_history['price'] / df_team_sticker_price_history['price'].max()

            df_team_sticker_price_history = df_team_sticker_price_history.set_index('date')
            dataframes.append(df_team_sticker_price_history)

        if len(dataframes) == 0 or len(dataframes[0]) == 0:
            continue

        combined = pd.concat(dataframes, axis=1, keys=[f'{i}' for i in range(len(dataframes))])

        combined['total_price'] = 0
        for i in range(len(dataframes)):
            combined['total_price'] += combined[f'{i}']['price'].fillna(0)

        combined['total_price'] /= len(dataframes)

        min_price = combined.index.min()
        if min_x < min_price:
            min_x = min_price

        result = re.sub(r"\s*\(.*?\)", "", df_team_sticker_tournament_first['name'].iloc[0])

        sns.lineplot(combined, x='date', y='total_price', ax=ax)
        ax.set_title(result)
        ax.set_ylim([0, 1])
        ax.set_xlim([min_x, max_x])
        ax.set_xlabel('Date (YYYY-MM)')
        ax.set_ylabel('Price (CHF)')
        ax.vlines(x=Wins, alpha=1, label='Win', ymin=- 10, ymax=+ 10)
        ax.vlines(x=Loses, alpha=1, label='Lose', ymin=- 10, ymax=+ 10)
        plt.show()

def sticker_total_change_avg(team_name: str):
    df_games_data = query(f"""
                        SELECT
                            GR.gameid,
                            endtscore,
                            endctscore,
                            matchdate,
                            MAX(CASE WHEN side = 'T' THEN teamname END) AS T,
                            MAX(CASE WHEN side = 'CT' THEN teamname END) AS CT
                        FROM gamerounds GR
                        JOIN (
                            SELECT G.gameid, G.matchdate, MAX(gameroundid) as gameroundid
                            FROM game G
                            JOIN public.gamerounds g2 ON G.gameid = g2.gameid
                            GROUP BY G.gameid, G.matchdate
                        ) LASTROUND
                        ON LASTROUND.gameroundid = GR.gameroundid
                        JOIN public.teamgameside t ON GR.gameroundid = t.gameroundid
                        JOIN public.team t2 ON t.teamid = t2.teamid
                        WHERE teamname = '{team_name}'
                        GROUP BY GR.gameid, endtscore, endctscore, matchdate
                        ORDER BY gameid ASC
                    """)

    df_team_games = df_games_data[(df_games_data['t'] == team_name) | (df_games_data['ct'] == team_name)]

    Wins = []
    Loses = []
    for i in range(len(df_team_games)):
        row = df_team_games.iloc[i]
        if ((row['endtscore'] > row['endctscore']) and row['t'] == team_name) or (
                (row['endtscore'] < row['endctscore']) and row['ct'] == team_name):
            Wins.append(row['matchdate'])
        else:
            Loses.append(row['matchdate'])
    min_x = min(min(Wins), min(Loses))
    max_x = max(max(Wins), max(Loses))


    df_average = query(f"""
        SELECT date, SUM(amountsold) as sum_amount, AVG(price) as avg_price  FROM price
            JOIN cosmetic C ON price.cosmeticid = C.cosmeticid
            JOIN teamsticker TS ON C.cosmeticid = TS.cosmeticid
            JOIN team T ON TS.teamid = T.teamid
            WHERE  T.teamname = '{team_name}'
            AND date BETWEEN {min_x} AND {max_x}
            GROUP BY date
    """)

    min_date = df_average['date'].min()
    if min_x < min_date:
        min_x = min_date

    df_games_data['matchdate'] = df_games_data['matchdate'].apply(datetime.fromtimestamp)
    df_average['date'] = df_average['date'].apply(datetime.fromtimestamp)

    min_x = datetime.fromtimestamp(min_x)
    max_x = datetime.fromtimestamp(max_x)

    for i in range(len(Wins)):
        Wins[i] = datetime.fromtimestamp(Wins[i])
    for i in range(len(Loses)):
        Loses[i] = datetime.fromtimestamp(Loses[i])

    fig_price, ax_price = plt.subplots(1, 1, figsize=(15, 5))
    ax_price.set_title(f'{team_name} performance and its influence on market price')
    ax_price.set_xlim([min_x, max_x])
    ax_price.set_xlabel('Date (YYYY-MM)')
    ax_price.set_ylabel('Price (CHF)')

    ax_price.set_ylim(0, df_average['avg_price'].max() + 10)

    ax_price.vlines(x=Wins, alpha=1, label='Win', ymin=df_average['avg_price'].min() - 10, ymax=df_average['avg_price'].max() + 10, colors='#44AA99')
    ax_price.vlines(x=Loses, alpha=1, label='Lose', ymin=df_average['avg_price'].min() - 10, ymax=df_average['avg_price'].max() + 10, colors='#CC6677')
    sns.lineplot(df_average, x='date', y='avg_price', ax=ax_price, color='#332288')

    # Legend creation
    line_handle_win = mlines.Line2D([], [], color='#44AA99', markersize=2, label='Win')
    line_handle_lose = mlines.Line2D([], [], color='#CC6677', linewidth=2, label='Lose')
    line_handle_price = mlines.Line2D([], [], color='#332288', linewidth=2, label='Price average (CHF)')
    ax_price.legend(handles=[line_handle_win, line_handle_lose, line_handle_price], loc='upper right')

    fig_price.show()

    fig_amount, ax_amount = plt.subplots(1, 1, figsize=(15, 5))
    ax_amount.set_title(f'{team_name} performance and its influence on market price')
    ax_amount.set_xlim([min_x, max_x])
    ax_amount.set_xlabel('Date (YYYY-MM)')
    ax_amount.set_ylabel('Amount sold')

    ax_amount.set_ylim(0, df_average['avg_amount'].max() + 10)

    ax_amount.vlines(x=Wins, alpha=1, label='Win', ymin=df_average['avg_amount'].min() - 1000, ymax=df_average['avg_amount'].max() + 1000, colors='#44AA99')
    ax_amount.vlines(x=Loses, alpha=1, label='Lose', ymin=df_average['avg_amount'].min() - 1000, ymax=df_average['avg_amount'].max() + 1000, colors='#CC6677')
    sns.lineplot(df_average, x='date', y='avg_amount', ax=ax_amount, color='#332288')

    # Legend creation
    line_handle_win = mlines.Line2D([], [], color='#44AA99', markersize=2, label='Win')
    line_handle_lose = mlines.Line2D([], [], color='#CC6677', linewidth=2, label='Lose')
    line_handle_amount = mlines.Line2D([], [], color='#332288', linewidth=2, label='Price average (CHF)')
    ax_amount.legend(handles=[line_handle_win, line_handle_lose, line_handle_amount], loc='upper right')

    fig_amount.show()

    fig_price.savefig(f'../../Resources/Analysis/g10_{team_name}_win_lose_price.png', bbox_inches='tight')
    fig_amount.savefig(f'../../Resources/Analysis/g10_{team_name}_win_lose_amount.png', bbox_inches='tight')



def team_performance():
    team_names = query("SELECT teamname FROM team WHERE teamid IN (SELECT DISTINCT teamid FROM teamsticker)")

    teams = []
    win_rate = []
    win_count = []
    lose_count = []
    average = []
    l_max = []
    l_min = []

    for row in team_names.iterrows():
        team_name = row[1]['teamname']
        df_team_games = query(f"""
                                SELECT
                                    GR.gameid,
                                    endtscore,
                                    endctscore,
                                    matchdate,
                                    MAX(CASE WHEN side = 'T' THEN teamname END) AS T,
                                    MAX(CASE WHEN side = 'CT' THEN teamname END) AS CT
                                FROM gamerounds GR
                                JOIN (
                                    SELECT G.gameid, G.matchdate, MAX(gameroundid) as gameroundid
                                    FROM game G
                                    JOIN gamerounds GR ON G.gameid = GR.gameid
                                    GROUP BY G.gameid, G.matchdate
                                ) LASTROUND
                                ON LASTROUND.gameroundid = GR.gameroundid
                                JOIN teamgameside TGS ON GR.gameroundid = TGS.gameroundid
                                JOIN team T ON TGS.teamid = T.teamid
                                WHERE teamname = '{team_name}'
                                GROUP BY GR.gameid, endtscore, endctscore, matchdate
                                ORDER BY gameid ASC;
                            """)
        df_team_games['matchdate'] = df_team_games['matchdate'].apply(datetime.fromtimestamp)
        df_team_games = df_team_games[(df_team_games['t'] == team_name) | (df_team_games['ct'] == team_name)]

        team_win = 0
        team_lose = 0
        Wins_dates = []
        Loses_dates = []
        for i in range(len(df_team_games)):
            row = df_team_games.iloc[i]
            if ((row['endtscore'] > row['endctscore']) and row['t'] == team_name) or (
                    (row['endtscore'] < row['endctscore']) and row['ct'] == team_name):
                team_win += 1
                Wins_dates.append(row['matchdate'])
            else:
                team_lose += 1
                Loses_dates.append(row['matchdate'])

        if len(Wins_dates) == 0:
            Wins_dates = Loses_dates
        if len(Loses_dates) == 0:
            Wins_dates = Wins_dates

        min_x = min(min(Wins_dates), min(Loses_dates))
        max_x = max(max(Wins_dates), max(Loses_dates))
        df_average = query(f"""
            SELECT AVG(price), MAX(price), MIN(price) FROM price P
                JOIN cosmetic C ON P.cosmeticid = C.cosmeticid
                JOIN teamsticker TS ON C.cosmeticid = TS.cosmeticid
                JOIN team T ON TS.teamid = T.teamid
                WHERE teamname = '{team_name}'
                AND date BETWEEN {datetime.timestamp(min_x)} AND {datetime.timestamp(max_x)}
                
        """)
        avg = df_average['avg'][0]

        if np.isnan(avg):
            continue

        teams.append(team_name)
        win_count.append(team_win)
        lose_count.append(team_lose)
        win_rate.append(team_win / (team_win + team_lose) * 100)
        average.append(df_average['avg'][0])
        l_max.append(df_average['max'][0])
        l_min.append(df_average['min'][0])


    all_teams = teams + teams
    all_count = win_count + lose_count
    all_type = ['win' for _ in range(len(win_count))] + ['lose' for _ in range(len(lose_count))]
    df_count = pd.DataFrame({'team': all_teams, 'count': all_count,  'type': all_type})
    df_win_rate = pd.DataFrame({'team': teams, 'win_rate': win_rate})
    df_average = pd.DataFrame({'team': teams, 'average': average, 'max': l_max, 'min': l_min})

    team_total_counts = df_count.groupby('team')['count'].sum().reset_index()
    sorted_teams = team_total_counts.sort_values('count', ascending=False)['team']

    df_count['team'] = pd.Categorical(df_count['team'], categories=sorted_teams, ordered=True)
    df_count = df_count.sort_values(['team', 'type'])

    df_average['team'] = pd.Categorical(df_average['team'], categories=sorted_teams, ordered=True)
    df_average = df_average.sort_values('team')

    fig, ax = plt.subplots(1, 1, figsize=(15, 5))
    ax.set_title('Team performance and its influence on market price')
    sns.barplot(df_count, x='team', y='count', hue='type', ax=ax, palette={'win': '#44AA99', 'lose': '#CC6677'})
    ax.set_xlabel('Team name')
    ax.set_ylabel('Count')
    ax.tick_params(axis='x', rotation=90)

    ax_right = ax.twinx()
    ax_right.grid(False)
    ax_right.set_ylabel('Price average (CHF)')
    sns.lineplot(df_average, x='team', y='average', ax=ax_right, color='#332288')
    sns.lineplot(df_average, x='team', y='max', ax=ax_right, color='#88CCEE')
    sns.lineplot(df_average, x='team', y='min', ax=ax_right, color='#DDCC77')
    ax_right.tick_params(axis='x', rotation=90)

    left_min, left_max = ax.get_ylim()
    right_min, right_max = ax_right.get_ylim()
    ax.set_ylim(0, left_max)
    ax_right.set_ylim(0, right_max)

    # Legend creation
    bar_handle_win = mlines.Line2D([], [], color='#44AA99', marker='s', markersize=10, linestyle='None', label='Win')
    bar_handle_lose = mlines.Line2D([], [], color='#CC6677', marker='s', markersize=10, linestyle='None', label='Lose')
    line_handle = mlines.Line2D([], [], color='#332288', linewidth=2, label='Price average (CHF)')
    ax.legend(handles=[bar_handle_win, bar_handle_lose, line_handle], loc='upper right')

    fig.tight_layout()
    fig.show()

    sorted_teams_win_rate = df_win_rate.sort_values('win_rate', ascending=False)['team']

    df_win_rate['team'] = pd.Categorical(df_win_rate['team'], categories=sorted_teams_win_rate, ordered=True)
    df_win_rate = df_win_rate.sort_values(['team'])

    df_average['team'] = pd.Categorical(df_average['team'], categories=sorted_teams_win_rate, ordered=True)
    df_average = df_average.sort_values('team')

    fig_rate, ax_rate = plt.subplots(1, 1, figsize=(15, 5))
    ax_rate.set_title('Team performance and its influence on market price')
    sns.barplot(df_win_rate, x='team', y='win_rate', ax=ax_rate, color='#44AA99')
    ax_rate.set_xlabel('Team name')
    ax_rate.set_ylabel('Win rate (%)')
    ax_rate.tick_params(axis='x', rotation=90)

    ax_rate_right = ax_rate.twinx()
    ax_rate_right.grid(False)
    ax_rate_right.set_ylabel('Price average (CHF)')
    sns.lineplot(df_average, x='team', y='average', ax=ax_rate_right, color='#332288')
    sns.lineplot(df_average, x='team', y='max', ax=ax_rate_right, color='#88CCEE')
    sns.lineplot(df_average, x='team', y='min', ax=ax_rate_right, color='#DDCC77')
    ax_rate_right.tick_params(axis='x', rotation=90)

    left_min, left_max = ax_rate_right.get_ylim()
    right_min, right_max = ax_rate_right.get_ylim()
    ax_rate_right.set_ylim(0, left_max)
    ax_rate_right.set_ylim(0, right_max)

    # Legend creation
    bar_handle_win_rate = mlines.Line2D([], [], color='#44AA99', marker='s', markersize=10, linestyle='None', label='Win rate (%)')
    line_handle = mlines.Line2D([], [], color='#332288', linewidth=2, label='Price average (CHF)')
    ax_rate.legend(handles=[bar_handle_win_rate, line_handle], loc='upper right')

    fig_rate.tight_layout()
    fig_rate.show()

    fig.savefig(f'../../Resources/Analysis/g10_team_performance_and_price_win_lose.png', bbox_inches='tight')
    fig_rate.savefig(f'../../Resources/Analysis/g10_team_performance_and_price_win_rate.png', bbox_inches='tight')


def player_performance():
    impact = lambda kpr, apr: 2.13 * kpr + 0.42 * apr - 0.41
    rating = lambda kast, kpr, dpr, impact, adr: 0.0073 * kast + 0.3591 * kpr - 0.5329 * dpr + 0.2372 * impact + 0.0032 * adr

    df_player = query("SELECT DISTINCT P.playerid, P.name FROM playersticker PS JOIN player P ON PS.playerid = P.playerid")
    player = []
    player_rating = []
    for row in df_player.iterrows():
        playerid = row[1]['playerid']
        print(row, df_player.count())
        df_rounds = query(f"""
            SELECT COUNT(DISTINCT PQ.gameroundid) FROM player_query PQ
                WHERE PQ.playerid = {playerid}
        """)

        df_kill = query(f"""
            SELECT COUNT(DISTINCT K.killid) as count FROM player_query PQ 
                JOIN Kill K ON PQ.playerframeid = K.attackerplayerframeid
                WHERE PQ.playerid = {playerid}
        """)

        df_assist = query(f"""
            SELECT COUNT(DISTINCT K.killid) as count FROM player_query PQ 
                JOIN Kill K ON PQ.playerframeid = K.assisterplayerframeid
                WHERE PQ.playerid = {playerid}
        """)

        df_deaths = query(f"""
            SELECT COUNT(DISTINCT K.killid) as count FROM player_query PQ 
                JOIN Kill K ON PQ.playerframeid = K.victimplayerframeid
                WHERE PQ.playerid = {playerid}
        """)

        df_damage = query(f"""
            SELECT SUM(hpdamage + armordamage) as sum FROM player_query PQ 
                JOIN Damage D ON PQ.playerframeid = D.attackerplayerframeid
                WHERE PQ.playerid = {playerid}
        """)

        df_kast = query(f"""
            SELECT COUNT(DISTINCT gameroundid) FROM
                (SELECT DISTINCT PQ.gameroundid FROM player_query PQ
                    JOIN Kill K ON PQ.playerframeid = K.assisterplayerframeid
                    WHERE PQ.playerid = {playerid}
                UNION
                SELECT DISTINCT PQ.gameroundid FROM player_query PQ
                    JOIN Kill K ON PQ.playerframeid = K.attackerplayerframeid
                    WHERE PQ.playerid = {playerid}
                UNION
                SELECT DISTINCT PQ.gameroundid FROM player_query PQ
                    JOIN Kill K ON PQ.playerframeid = K.tradedplayerframeid
                    WHERE PQ.playerid = {playerid}
                UNION
                (
                    SELECT DISTINCT PQ.gameroundid FROM player_query PQ
                        WHERE PQ.playerid = {playerid}
                    EXCEPT
                    SELECT DISTINCT PQ.gameroundid FROM player_query PQ
                        JOIN Kill K ON PQ.playerframeid = K.victimplayerframeid
                        WHERE PQ.playerid = {playerid}
                )) AS A
        """)
        amount_rounds = df_rounds['count'][0]

        kast = df_kast['count'][0] / amount_rounds
        kpr = df_kill['count'][0] / amount_rounds
        apr = df_assist['count'][0] / amount_rounds
        dpr = df_deaths['count'][0] / amount_rounds
        adr = df_damage['sum'][0] / amount_rounds
        imp = impact(kpr, apr)

        current_player_rating = rating(kast, kpr, dpr, 0, adr)

        player.append(row[1]['name'])
        player_rating.append(current_player_rating)


    df_date = query("SELECT MIN(matchdate), MAX(matchdate) FROM game")
    df_average = query(f"""
        SELECT P.name, AVG(PR.price) FROM playersticker PS
            JOIN player P ON PS.playerid = P.playerid
            JOIN price PR ON PR.cosmeticid = PS.cosmeticid
            WHERE date BETWEEN {df_date['min'][0]} AND {df_date['max'][0]}
            GROUP BY P.name
    """)

    df_rating = pd.DataFrame({'player': player, 'rating': player_rating})

    sorted_player_rating = df_rating.sort_values('rating', ascending=False)['player']

    df_rating['player'] = pd.Categorical(df_rating['player'], categories=sorted_player_rating, ordered=True)
    df_rating = df_rating.sort_values(['player'])

    df_average['name'] = pd.Categorical(df_average['name'], categories=sorted_player_rating, ordered=True)
    df_average = df_average.sort_values('name')

    fig, ax = plt.subplots(1, 1, figsize=(30, 5))
    ax.set_xlabel('Player name')
    ax.set_ylabel('HLTV Rating')
    ax.set_title('Player performance and its influence on market price')
    ax.set_xlabel('Player')

    sns.barplot(df_rating, x='player', y='rating', ax=ax, color='#44AA99', dodge=False)
    ax.tick_params(axis='x', rotation=90)
    ax.margins(x=0)
    ax_right = ax.twinx()
    ax_right.set_ylabel('Price average (CHF)')
    ax_right.grid(False)
    sns.lineplot(df_average, x='name', y='avg', color='#332288')
    ax_right.tick_params(axis='x', rotation=90)

    left_min, left_max = ax.get_ylim()
    right_min, right_max = ax_right.get_ylim()
    ax.set_ylim(0, left_max)
    ax_right.set_ylim(0, right_max)
    x_min, x_max = ax.get_xlim()
    ax.set_xlim([x_min, x_max])


    # Legend creation
    bar_handle = mlines.Line2D([], [], color='#44AA99', marker='s', markersize=10, linestyle='None', label='Player rating')
    line_handle = mlines.Line2D([], [], color='#332288', linewidth=2, label='Price average (CHF)')
    ax.legend(handles=[bar_handle, line_handle], loc='upper right')

    fig.tight_layout()
    fig.show()

    fig.savefig(f'../../Resources/Analysis/g10_player_performance_and_price.png', bbox_inches='tight')

def weapon_usage():
    exclude = ['', 'C4', 'Grenade', 'Incendiary Grenade', 'HE Grenade', 'Smoke Grenade', 'Flashbang', 'Molotov', 'Decoy Grenade', 'World']


    df_weapon_skin_data = query(f"""
        SELECT W.weaponid, W.weaponname, AVG(P.price) as avg, MAX(P.price) as max, MIN(P.price) as min FROM cosmetic C
            JOIN price P ON C.cosmeticid = P.cosmeticid
            JOIN weaponskin WS ON C.cosmeticid = WS.cosmeticid
            JOIN weapon W ON WS.game_weaponid = W.weaponid
            WHERE W.weaponname NOT IN {(str(exclude)).replace("[", "(").replace("]", ")")}
            GROUP BY W.weaponname, W.weaponid
            ORDER BY weaponid
    """)

    df_weapon_usage_total = query(f"""
        SELECT COUNT(*) FROM playerframe PF 
            JOIN weapon W ON PF.activeweaponid = W.weaponid
            WHERE W.weaponname NOT IN {(str(exclude)).replace("[", "(").replace("]", ")")}
    """)

    df_weapon_usage = query(f"""
            SELECT W.weaponname, weaponid, COUNT(*) FROM playerframe PF
                JOIN weapon W ON PF.activeweaponid = W.weaponid
                WHERE W.weaponname NOT IN {(str(exclude)).replace("[", "(").replace("]", ")")}
                GROUP BY W.weaponname, W.weaponid
                ORDER BY count DESC
        """)
    df_weapon_usage['count'] /= df_weapon_usage_total['count'][0]
    df_weapon_usage['count'] *= 100

    weapon_order = df_weapon_usage['weaponname'].tolist()
    df_weapon_skin_data['weaponname'] = pd.Categorical(
        df_weapon_skin_data['weaponname'],
        categories=weapon_order,
        ordered=True
    )
    df_weapon_skin_data = df_weapon_skin_data.sort_values('weaponname')

    fig, ax = plt.subplots(1, 1, figsize=(15, 5))

    ax.set_xlim(-0.5, len(df_weapon_usage['weaponname']) - 0.5)

    sns.barplot(data=df_weapon_usage, x='weaponname', y='count', ax=ax, color='#44AA99')
    ax.set_ylabel('Usage (%)', fontsize=12)
    ax.tick_params(axis='x', rotation=90)

    ax_right = ax.twinx()
    ax_right.grid(False)
    sns.lineplot(data=df_weapon_skin_data, x='weaponname', y='avg', ax=ax_right, color='#332288', linewidth=2, legend=False)
    ax_right.set_ylabel('Price average (CHF)', fontsize=12)

    left_min, left_max = ax.get_ylim()
    right_min, right_max = ax_right.get_ylim()
    ax.set_ylim(0, left_max)
    ax_right.set_ylim(0, right_max)

    # Legend creation
    bar_handle = mlines.Line2D([], [], color='#44AA99', marker='s', markersize=10, linestyle='None', label='Usage (%)')
    line_handle = mlines.Line2D([], [], color='#332288', linewidth=2, label='Price average (CHF)')
    ax.legend(handles=[bar_handle, line_handle], loc='upper right')

    ax.set_xlabel('Weapon Name')
    ax.set_title("Weapon usage and its influence on market price")

    plt.tight_layout()
    plt.show()

    fig.savefig(f'../../Resources/Analysis/g10_weapon_usage_price.png', bbox_inches='tight')

def event_influence():
    exclude = ['Key', 'Case', 'MISC', 'Souvenir Package', 'Music Kit', 'Music Kit Box', 'Patch Pack', 'Pass']

    df_average_weapons = query(f"""
        SELECT C.type, P.date, AVG(P.price) as avg FROM price P 
            JOIN cosmetic C ON C.cosmeticid = P.cosmeticid       
            WHERE C.type NOT IN {(str(exclude)).replace("[", "(").replace("]", ")")}
            GROUP BY P.date, C.type
    """)
    df_average_weapons['date'] = df_average_weapons['date'].apply(datetime.fromtimestamp)

    fig, ax = plt.subplots(1, 1, figsize=(15, 5))
    sns.lineplot(df_average_weapons, x='date', y='avg', hue='type' ,ax=ax)
    fig.show()

    df_average_cases = query("""
        SELECT C.Name, C.type, P.date, AVG(P.price) as avg FROM price P
                JOIN cosmetic C ON C.cosmeticid = P.cosmeticid
                WHERE C.type IN ('Case')
                GROUP BY P.date, C.type, C.Name
    """)
    df_average_cases['date'] = df_average_cases['date'].apply(datetime.fromtimestamp)
    fig, ax = plt.subplots(1, 1, figsize=(15, 5))
    sns.lineplot(df_average_cases, x='date', y='avg', hue='type', ax=ax)
    fig.show()

def event_influence_holidays():
    min_date = datetime.timestamp(datetime.strptime('2014-05-01 12:00:00', '%Y-%m-%d %H:%M:%S'))
    max_date = datetime.timestamp(datetime.strptime('2024-05-01 12:00:00', '%Y-%m-%d %H:%M:%S'))
    df_amount = query(f"""
            SELECT P.date, SUM(P.amountsold) as sum_amount, AVG(P.price) as avg_price FROM price P
                JOIN cosmetic C ON C.cosmeticid = P.cosmeticid
                WHERE C.type = 'Case'
                AND C.name NOT LIKE '%Hardened%'
                AND P.date < {max_date}
                GROUP BY P.date
        """)
    df_amount['date'] = df_amount['date'].apply(datetime.fromtimestamp)

    min_avg = df_amount['sum_amount'].min()
    max_avg = df_amount['sum_amount'].max()

    christmas_dates = [datetime.strptime(v, '%Y-%m-%d %H:%M:%S') for k, v in holiday_dates.items() if 'Christmas' in k]

    fig_christmas, axes_christmas = plt.subplots(len(christmas_dates) // 2 , 2, figsize=(12, len(christmas_dates)))
    axes = []
    for i in range(len(axes_christmas)):
        for j in range(len(axes_christmas[i])):
            axes.append(axes_christmas[i, j])

    for ax_c, christmas_date in zip(axes, christmas_dates):
        start_date = christmas_date - timedelta(days=10)
        end_date = christmas_date + timedelta(days=10)

        subset = df_amount[(df_amount['date'] >= start_date) & (df_amount['date'] <= end_date)]
        subset['sum_amount'] = subset['sum_amount'] / subset['sum_amount'].max()
        subset['avg_price'] = subset['avg_price'] / subset['avg_price'].max()

        sns.lineplot(data=subset, x='date', y='sum_amount', ax=ax_c, color='#332288')
        sns.lineplot(data=subset, x='date', y='avg_price', ax=ax_c, color='#44AA99')

        ax_c.axvline(christmas_date, color='#CC6677', linestyle='--', linewidth=2)
        ax_c.set_title(f'{christmas_date.year}')
        ax_c.set_ylabel('Normalized Values')
        ax_c.set_xlim([start_date, end_date])
        ax_c.set_xticks([])
        ax_c.set_ylabel('Normalized values')
        ax_c.set_xlabel('Date')

    line_handle_christmas = mlines.Line2D([], [], color='#CC6677', linewidth=2, linestyle='--', label='Christmas')
    line_handle_price = mlines.Line2D([], [], color='#44AA99', linewidth=2, label='Price (CHF)')
    line_handle_sold = mlines.Line2D([], [], color='#332288', linewidth=2, label='Amount sold')
    fig_christmas.legend(handles=[line_handle_christmas, line_handle_price, line_handle_sold], loc='lower center', ncol=3, frameon=False)
    fig_christmas.suptitle("Christmas holiday and its influence on the market. 10 days before and after Christmas")
    fig_christmas.tight_layout()
    fig_christmas.show()
    fig_christmas.savefig(f'../../Resources/Analysis/g10_christmas_market.png', bbox_inches='tight')

    quit()

    min_date = df_amount['date'].min()
    max_date = df_amount['date'].max()
    print(df_amount['date'])
    sns.lineplot(df_amount, x='date', y='sum_amount', ax=ax, color='#117733')
    sns.lineplot(df_amount, x='date', y='avg_price', ax=ax, color='#415625')
    ax.set_xlim([min_date, max_date])
    for event in holiday_dates.keys():
        date = holiday_dates[event]
        converted_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        if 'Easter' in event:
            print(converted_date)
            ax.axvline(converted_date, min_avg - 100, max_avg + 100, color='#999933', linewidth=2)

        if 'Christmas' in event:
            ax.axvline(converted_date, min_avg - 100, max_avg + 100, color='#CC6677', linewidth=2)

        if 'Chinese' in event:
            ax.axvline(converted_date, min_avg - 100, max_avg + 100, color='#332288', linewidth=2)

        if 'Halloween' in event:
            ax.axvline(converted_date, min_avg - 100, max_avg + 100, color='#000000', linewidth=2)

    line_handle_easter = mlines.Line2D([], [], color='#999933', linewidth=2, label='Easter')
    line_handle_christmas = mlines.Line2D([], [], color='#CC6677', linewidth=2, label='Christmas')
    line_handle_lunar = mlines.Line2D([], [], color='#332288', linewidth=2, label='Chinese lunar new year')
    line_handle_halloween = mlines.Line2D([], [], color='#000000', linewidth=2, label='Halloween')
    line_handle_amount = mlines.Line2D([], [], color='#000000', linewidth=2, label='Amount sold')
    ax.legend(handles=[line_handle_easter, line_handle_christmas, line_handle_lunar, line_handle_halloween, line_handle_amount], loc='upper right')

    fig.show()

    fig.savefig(f'../../Resources/Analysis/g10_holidays_all.png', bbox_inches='tight')


    fig_year, ax_year = plt.subplots(2, 4, figsize=(15, 5))
    fig_year.suptitle('Global holidays and their influence on the market')
    years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']
    index = {'2015': (0, 0), '2016': (0, 1), '2017': (0, 2), '2018': (0, 3), '2019': (1, 0), '2020': (1, 1), '2021': (1, 2), '2022': (1, 3)}
    for year in years:
        n, m = index[year]
        ax = ax_year[n, m]
        df_year = df_amount[df_amount['date'].dt.year == int(year)]
        df_year['sum_amount'] = df_year['sum_amount'] / df_year['sum_amount'].max()
        df_year['avg_price'] = df_year['avg_price'] / df_year['avg_price'].max()
        sns.lineplot(df_year, x='date', y='sum_amount', ax=ax, color='#117733')
        sns.lineplot(df_year, x='date', y='avg_price', ax=ax, color='#415625')
        ax.set_title(year)
        ax.set_xlabel('')
        ax.set_ylabel('')
        for event in holiday_dates.keys():
            if year[2:] in event:
                date = holiday_dates[event]
                converted_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                if 'Easter' in event:
                    ax.axvline(converted_date, min_avg - 100, max_avg + 100, color='#999933', linewidth=2)

                if 'Christmas' in event:
                    ax.axvline(converted_date, min_avg - 100, max_avg + 100, color='#CC6677', linewidth=2)

                if 'Chinese' in event:
                    ax.axvline(converted_date, min_avg - 100, max_avg + 100, color='#332288', linewidth=2)

                if 'Halloween' in event:
                    ax.axvline(converted_date, min_avg - 100, max_avg + 100, color='#000000', linewidth=2)

    line_handle_easter = mlines.Line2D([], [], color='#999933', linewidth=2, label='Easter')
    line_handle_christmas = mlines.Line2D([], [], color='#CC6677', linewidth=2, label='Christmas')
    line_handle_lunar = mlines.Line2D([], [], color='#332288', linewidth=2, label='Chinese lunar new year')
    line_handle_halloween = mlines.Line2D([], [], color='#000000', linewidth=2, label='Halloween')
    line_handle_amount = mlines.Line2D([], [], color='#000000', linewidth=2, label='Amount sold')

    fig_year.legend(handles=[line_handle_easter, line_handle_christmas, line_handle_lunar, line_handle_halloween, line_handle_amount],
                ncol=2, frameon=False)

    fig_year.supxlabel('Date (YYYY-MM)')
    fig_year.supylabel('Amount sold normalized')
    plt.tight_layout()
    fig_year.show()


def covid_impact():
    min_date = datetime.timestamp(datetime.strptime('2019-06-01 12:00:00', '%Y-%m-%d %H:%M:%S'))
    max_date = datetime.timestamp(datetime.strptime('2022-06-01 12:00:00', '%Y-%m-%d %H:%M:%S'))
    df_data = query(f"""
        SELECT P.date, SUM(P.amountsold) as sum_amount FROM price P
            JOIN cosmetic C ON P.cosmeticid = C.cosmeticid
            WHERE P.date BETWEEN {min_date} AND {max_date} 
            GROUP BY P.date
    """)

    df_data['date'] = df_data['date'].apply(datetime.fromtimestamp)
    ymin = df_data['sum_amount'].min()
    ymax = df_data['sum_amount'].max()

    #https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic
    first = datetime.strptime('2019-11-17 12:00:00', '%Y-%m-%d %H:%M:%S')
    second = datetime.strptime('2020-01-19 12:00:00', '%Y-%m-%d %H:%M:%S')
    third = datetime.strptime('2020-03-11 12:00:00', '%Y-%m-%d %H:%M:%S')
    fourth = datetime.strptime('2020-10-01 12:00:00', '%Y-%m-%d %H:%M:%S')
    fifth = datetime.strptime('2021-01-01 12:00:00', '%Y-%m-%d %H:%M:%S')

    fig, ax = plt.subplots(1, 1, figsize=(15, 5))
    sns.lineplot(df_data, x='date', y='sum_amount', color='#44AA99')

    left_min, left_max = ax.get_ylim()
    ax.set_ylim(left_min, left_max)

    # Adding vertical lines at specified dates
    ax.vlines(first, ymin=ymin - 100, ymax=ymax + 100, colors='#CC6677')
    ax.vlines(second, ymin=ymin - 100, ymax=ymax + 100, colors='#CC6677')
    ax.vlines(third, ymin=ymin - 100, ymax=ymax + 100, colors='#CC6677')
    ax.vlines(fourth, ymin=ymin - 100, ymax=ymax + 100, colors='#CC6677')
    ax.vlines(fifth, ymin=ymin - 100, ymax=ymax + 100, colors='#CC6677')
    ax.set_title('Covid-19 and its influence on the market')
    ax.set_xlabel('Date (YYYY-MM)')
    ax.set_ylabel('Amount sold')
    ax.set_xlim([df_data['date'].min(), df_data['date'].max()])
    # Adding text annotation at the specified position
    ax.text(first - timedelta(days=10), left_max * 0.95, 'First case local', color='#CC6677',
            ha='center', va='top', fontsize=12, rotation=90)
    ax.text(second - timedelta(days=10), left_max * 0.95, 'First case global', color='#CC6677',
            ha='center', va='top', fontsize=12, rotation=90)
    ax.text(third - timedelta(days=10), left_max * 0.95, 'WHO pandemic decleration', color='#CC6677',
            ha='center', va='top', fontsize=12, rotation=90)
    ax.text(third + timedelta(days=15), left_max * 0.95, 'First lockdown', color='#CC6677',
            ha='center', va='top', fontsize=12, rotation=90)
    ax.text(fourth - timedelta(days=10), left_max * 0.95, 'Second lockdown', color='#CC6677',
            ha='center', va='top', fontsize=12, rotation=90)
    ax.text(fifth - timedelta(days=10), left_max * 0.95, 'Third lockdown', color='#CC6677',
            ha='center', va='top', fontsize=12, rotation=90)

    line_handle_amount = mlines.Line2D([], [], color='#44AA99', linewidth=2, label='Amount sold')
    line_handle_event = mlines.Line2D([], [], color='#CC6677', linewidth=2, label='Event')
    ax.legend(handles=[line_handle_amount, line_handle_event], loc='upper right')

    fig.show()
    fig.savefig(f'../../Resources/Analysis/g10_covid_market.png', bbox_inches='tight')

def tournament_impact():
    max_date = datetime.timestamp(datetime.strptime('2024-05-01 12:00:00', '%Y-%m-%d %H:%M:%S'))
    df_data = query(f"""
            SELECT P.date, SUM(P.price) as sum FROM price P
            WHERE P.date <= {max_date}
            GROUP BY P.date
        """)
    df_data['date'] = df_data['date'].apply(datetime.fromtimestamp)
    ymin = df_data['sum'].min()
    ymax = df_data['sum'].max()
    xmin = df_data['date'].min()
    xmax = df_data['date'].max()

    fig, ax = plt.subplots(1, 1, figsize=(15, 5))

    for tournament in tournament_dates.keys():
        start, end = tournament_dates[tournament]
        start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        ax.vlines(start, ymin = 0, ymax = ymax + 1000, linestyles='--', colors='#CC6677')

    sns.lineplot(df_data, x='date', y='sum', ax=ax, color='#44AA99')
    ax.set_xlabel('Date (YYYY)')
    ax.set_ylabel('Sum price (CHF)')
    ax.set_title('Tournaments and their influence on the market')

    line_handle_tournament = mlines.Line2D([], [], color='#CC6677', linewidth=2, label='Tournament', linestyle='--')
    line_handle_amount = mlines.Line2D([], [], color='#44AA99', linewidth=2, label='Sum price (CHF)')

    ax.legend(handles=[line_handle_tournament, line_handle_amount])
    ax.set_xlim([xmin, xmax])

    fig.show()
    fig.savefig(f'../../Resources/Analysis/g10_tournament_price_market.png', bbox_inches='tight')


    max_date = datetime.timestamp(datetime.strptime('2024-05-01 12:00:00', '%Y-%m-%d %H:%M:%S'))
    df_data = query(f"""
        SELECT P.date, SUM(P.amountsold) as sum FROM price P
        WHERE P.date <= {max_date}
        GROUP BY P.date
    """)

    df_data['date'] = df_data['date'].apply(datetime.fromtimestamp)
    ymin = df_data['sum'].min()
    ymax = df_data['sum'].max()
    xmin = df_data['date'].min()
    xmax = df_data['date'].max()

    fig, ax = plt.subplots(1, 1, figsize=(15, 5))


    for tournament in tournament_dates.keys():
        start, end = tournament_dates[tournament]
        start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        ax.vlines(start, ymin = 0, ymax = ymax + 1000, linestyles='--', colors='#CC6677')

    sns.lineplot(df_data, x='date', y='sum', ax=ax, color='#44AA99')
    ax.set_xlabel('Date (YYYY)')
    ax.set_ylabel('Amount sold')
    ax.set_title('Tournaments and their influence on the market')

    line_handle_tournament = mlines.Line2D([], [], color='#CC6677', linewidth=2, label='Tournament', linestyle='--')
    line_handle_amount = mlines.Line2D([], [], color='#44AA99', linewidth=2, label='Amount sold')

    ax.legend(handles=[line_handle_tournament, line_handle_amount])
    ax.set_xlim([xmin, xmax])

    fig.show()
    fig.savefig(f'../../Resources/Analysis/g10_tournament_market.png', bbox_inches='tight')

    df_data = query(f"""
           SELECT P.date, SUM(P.amountsold) as sum FROM price P
           JOIN cosmetic C ON P.cosmeticid = C.cosmeticid
           WHERE P.date < {max_date} AND C.type = 'Sticker'
           GROUP BY P.date
       """)

    df_data['date'] = df_data['date'].apply(datetime.fromtimestamp)
    ymin = df_data['sum'].min()
    ymax = df_data['sum'].max()
    xmin = df_data['date'].min()
    xmax = df_data['date'].max()

    fig_sticker, ax_sticker = plt.subplots(1, 1, figsize=(15, 5))

    for tournament in tournament_dates.keys():
        start, end = tournament_dates[tournament]
        start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        ax_sticker.vlines(start, ymin=0, ymax=ymax + 1000, linestyles='--', colors='#CC6677')

    sns.lineplot(df_data, x='date', y='sum', ax=ax_sticker, color='#44AA99')
    ax_sticker.set_xlabel('Date (YYYY)')
    ax_sticker.set_ylabel('Amount sold')
    ax_sticker.set_title('Tournaments and their influence on the market stickers')

    line_handle_tournament = mlines.Line2D([], [], color='#CC6677', linewidth=2, label='Tournament', linestyle='--')
    line_handle_amount = mlines.Line2D([], [], color='#44AA99', linewidth=2, label='Amount sold')

    ax_sticker.legend(handles=[line_handle_tournament, line_handle_amount])
    ax_sticker.set_xlim([xmin, xmax])

    fig_sticker.show()
    fig_sticker.savefig(f'../../Resources/Analysis/g10_tournament_sticker_market.png', bbox_inches='tight')

if __name__ == "__main__":
    # Script divided into the functions that answer the specific analyis questions

    ############################################################
    #How do official Esport tournaments affect the price of skins?
    ############################################################
    tournament_impact()

    ############################################################
    #Do global events outside of the Esport world have an impact on the
    #steam market?
    ############################################################
    #event_influence_holidays()
    #covid_impact()

    ############################################################
    #How does in-game usability of a weapon affect the price of skins on
    #the marketplace?
    ############################################################
    #weapon_usage()

    ############################################################
    #Does player or team success in tournaments affect the price of team/-
    #player stickers and if yes, how?
    ############################################################
    # Teams
    #team_performance()
    #sticker_total_change_avg('G2 Esports')
    #sticker_total_change_avg('Natus Vincere')

    # Players
    player_performance()
