import pandas as pd

def show_table(players):
    data = {
        "Player": [player.name for player in players],
        "Total Participation": [player.get_participation_count() for player in players],
        "Total Place": [player.total_place for player in players],
        "Total Points": [player.total_points for player in players],
        "Total Mod Mean": [player.total_mod_mean for player in players],
        "Total Solkoff": [player.total_solkoff for player in players],
        "Total Cumulative": [player.total_cumulative for player in players],
        "Total Cumulative Opposition": [player.total_cumulative_opposition for player in players],
    }
    df = pd.DataFrame(data)
    df.to_csv("player_totals.csv", index=False)

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    pd.set_option('display.expand_frame_repr', False)

    print(df)

