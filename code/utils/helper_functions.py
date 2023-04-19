import pandas as pd
from matplotlib import pyplot as plt


def load_data(nrows):
    """ Loads and returns the football data """

    data = pd.read_csv("dataset/events_World_Cup.csv", nrows=nrows)
    return data


def get_match(matchId):
    """ For a given match ID, returns the match data in a pandas dataframe """

    data = pd.read_csv("dataset/events_World_Cup.csv")
    matches_with_id = data[data["matchId"] == matchId]
    return matches_with_id


def get_team_side(matchId, teamId):
    """ For a given match ID, and team ID returns the side on which the team plays on the pitch """
    
    data = pd.read_csv("dataset/events_World_Cup.csv")
    match = get_match(matchId)
    unique_team_ids = match["teamId"].unique()

    team_right = max(unique_team_ids)
    team_left = min(unique_team_ids)

    if team_right == teamId:
        return "right"
    else:
        return "left"


def simple_pass_render(pitch_height, pitch_width, match_id, game_time, time_window, ax):
    """ For a given match ID and game time, returns plot elements that visualize the passes in the form of arrows """

    match = get_match(match_id)
    data = match[match["subEventName"] == "Simple pass"]
    data = data[data["eventSec"] >= game_time*60]
    data = data[data["eventSec"] <= game_time*60 + time_window*60]

    for idx, event in data.iterrows():
        start_point = (event["pos_orig_x"]/100*pitch_width, event["pos_orig_y"]/100*pitch_height)
        end_point = (event["pos_dest_x"]/100*pitch_width, event["pos_dest_y"]/100*pitch_height)
        ax.annotate('', xy=end_point, xytext=start_point,
            arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle='->'))
    return ax