from Scripts.database import Database
from map_coordinates import *
from plotting_functions import *
import seaborn as sns
import matplotlib.colors as mcolors

n_colors = 512
blues = plt.cm.Blues_r(np.linspace(0.1, 1, n_colors // 2))
reds = plt.cm.Reds(np.linspace(0.1, 1, n_colors // 2))

combined_colors = np.vstack((blues, [1, 1, 1, 1], reds))

combined_cmap = mcolors.LinearSegmentedColormap.from_list('reds_blues_cmap', combined_colors)


sns.set()
db = Database()
query = db.query

mapping = {
    "de_dust2": map_de_dust2,
    "de_inferno": map_de_inferno,
    "de_mirage": map_de_mirage,
    "de_nuke": map_de_nuke,
    "de_overpass": map_de_overpass,
    "de_train": map_de_train,
    "de_vertigo": map_de_vertigo,
    "de_ancient": map_de_ancient
}

def position_heatmap(
        ax: plt.Axes = None,
        mapname: str = None
):
    save = False

    maps = [mapname]
    if mapname is None:
        maps = query("SELECT DISTINCT mapname FROM game")

    for map in maps['mapname']:
        df_map_positioning = query(f"""
            SELECT gameid, playerx, playery, playerz, side FROM gameplayerframeview 
            WHERE mapname='{map}'
        """)
        df_map_positioning['playerx'], df_map_positioning['playery'], df_map_positioning['playerz'] = mapping[map](df_map_positioning['playerx'], df_map_positioning['playery'], df_map_positioning['playerz'])
        grid = map_players_to_grid(df_map_positioning, map)

        # Check if axis is given. If yes then figure is part of a subplot
        if ax is None:
            fig, ax = plt.subplots()
            save = True

        heatmap_plot(ax, map, grid, mask_value=0, cmap='bwr')

        if save:
            plt.savefig(f'../Resources/Analysis/{map}_position_heatmap.png')

def ct_heatmap(ax: plt.Axes = None):
    save = False
    maps = query("SELECT DISTINCT mapname FROM game")
    for map in maps['mapname']:
        df_map_positioning = query(f"""
                SELECT gameid, playerx, playery, playerz, side FROM gameplayerframeview 
                WHERE mapname='{map}' AND side='CT'
            """)
        df_map_positioning['playerx'], df_map_positioning['playery'], df_map_positioning['playerz'] = mapping[map](
            df_map_positioning['playerx'], df_map_positioning['playery'], df_map_positioning['playerz'])
        grid = map_players_to_grid(df_map_positioning, map)

        # Check if axis is given. If yes then figure is part of a subplot
        if ax is None:
            fig, ax = plt.subplots()
            save = True

        heatmap_plot(ax, map, grid, mask_value=0, cmap='Blues')

        if save:
            plt.savefig(f'../Resources/Analysis/{map}_ct_position_heatmap.png')
        quit()

def t_heatmap(ax: plt.Axes = None):
    save = False
    maps = query("SELECT DISTINCT mapname FROM game")
    for map in maps['mapname']:
        df_map_positioning = query(f"""
                    SELECT gameid, playerx, playery, playerz, side FROM gameplayerframeview 
                    WHERE mapname='{map}' AND side='T'
                """)
        df_map_positioning['playerx'], df_map_positioning['playery'], df_map_positioning['playerz'] = mapping[map](
            df_map_positioning['playerx'], df_map_positioning['playery'], df_map_positioning['playerz'])
        grid = map_players_to_grid(df_map_positioning, map)

        # Check if axis is given. If yes then figure is part of a subplot
        if ax is None:
            fig, ax = plt.subplots()
            save = True

        heatmap_plot(ax, map, grid, mask_value=0, cmap='Reds')

        if save:
            plt.savefig(f'../Resources/Analysis/{map}_t_position_heatmap.png')
        quit()

def kill_heatmap():
    pass

def death_heatmap():
    pass

def smoke_scatter(ax: plt.Axes = None):
    save = False
    maps = query("SELECT DISTINCT mapname FROM game")
    for map in maps['mapname']:
        df_smoke = query(f"""
        SELECT DISTINCT(grenadeentityid), gameid, x, y, z, side FROM gameplayerframeview
        JOIN smoke ON smoke.frameid = gameplayerframeview.frameid
        WHERE mapname = '{map}'
        """)

        df_smoke['x'], df_smoke['y'], df_smoke['z'] = mapping[map](df_smoke['x'], df_smoke['y'], df_smoke['z'])
        grid = map_coordinates_to_grid(df_smoke)

        # Check if axis is given. If yes then figure is part of a subplot
        if ax is None:
            fig, ax = plt.subplots()
            save = True

        scatter_plot(ax, map, grid, size=5, mask_value=5, cmap='Greens')

        if save:
            plt.savefig(f'../Resources/Analysis/{map}_t_position_heatmap.png')


def test(
        map_name: str,
        start_timer: float = None,
        end_timer: float = None,
        mask_value: int = 1
):
    fig_t, (ax1_t, ax2_t, ax3_t) = plt.subplots(1, 3, figsize=(30, 10))
    fig_ct, (ax1_ct, ax2_ct, ax3_ct) = plt.subplots(1, 3, figsize=(30, 10))

    position_query = f"""
        SELECT gameid, playerx, playery, playerz, side FROM gameplayerframeview 
        WHERE mapname='{map_name}'
    """
    
    if start_timer is not None:
        position_query += f" AND seconds > {start_timer}"

    if end_timer is not None:
        position_query += f" AND seconds < {end_timer}"

    df_map_positioning = query(position_query)

    df_game_win = query(f"""
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
        JOIN teamgameside t ON GR.gameroundid = t.gameroundid
        JOIN team t2 ON t.teamid = t2.teamid
        GROUP BY GR.gameid, endtscore, endctscore, matchdate
        ORDER BY gameid ASC;
    """)

    df_t_win = df_game_win[df_game_win['endtscore'] > df_game_win['endctscore']]
    df_ct_win = df_game_win[df_game_win['endtscore'] < df_game_win['endctscore']]

    df_map_positioning_t = df_map_positioning[df_map_positioning['side'] == 'T']
    df_map_positioning_ct = df_map_positioning[df_map_positioning['side'] == 'CT']

    df_map_positioning_t_win = df_map_positioning_t[df_map_positioning_t['gameid'].isin(df_t_win['gameid'])]
    df_map_positioning_ct_win = df_map_positioning_ct[df_map_positioning_ct['gameid'].isin(df_ct_win['gameid'])]

    ax1_t.set_title('Total Game movement')
    ax2_t.set_title('T movement')
    ax3_t.set_title('T movement in winning games')
    grid_t = smooth_scale(df_map_positioning_t.copy(), map_name)
    grid_ct = smooth_scale(df_map_positioning_ct.copy(), map_name)
    grid_t_win = smooth_scale(df_map_positioning_t_win.copy(), map_name)
    grid_ct_win = smooth_scale(df_map_positioning_ct_win.copy(), map_name)
    grid = grid_t - grid_ct

    heatmap_plot(ax1_t, map_name, grid, cmap=combined_cmap, mask_value=mask_value)
    heatmap_plot(ax2_t, map_name, grid_t, cmap='Reds', mask_value=mask_value)
    heatmap_plot(ax3_t, map_name, grid_t_win, cmap='Reds', mask_value=mask_value)

    ax1_ct.set_title('Total Game movement')
    ax2_ct.set_title('CT movement')
    ax3_ct.set_title('CT movement in winning games')
    heatmap_plot(ax1_ct, map_name, grid, cmap=combined_cmap, mask_value=mask_value)
    heatmap_plot(ax2_ct, map_name, grid_ct, cmap='Blues', mask_value=mask_value)
    heatmap_plot(ax3_ct, map_name, grid_ct_win, cmap='Blues', mask_value=mask_value)

    fig_t.savefig(f'../../Resources/Analysis/{map_name}_t_position_heatmap_{start_timer}_{end_timer}.png', bbox_inches='tight')
    fig_ct.savefig(f'../../Resources/Analysis/{map_name}_ct_position_heatmap_{start_timer}_{end_timer}.png', bbox_inches='tight')

if __name__ == '__main__':
    maps = query("SELECT DISTINCT mapname FROM game")
    for map in maps['mapname']:
        test(map)
    for map in maps['mapname']:
        test(map, 0, 10)