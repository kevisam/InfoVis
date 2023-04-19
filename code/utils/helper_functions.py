import pandas as pd
from matplotlib import pyplot as plt


def load_data(nrows):
    data = pd.read_csv("dataset/events_World_Cup.csv", nrows=nrows)

    return data


def get_match(matchId):
    data = pd.read_csv("dataset/events_World_Cup.csv")
    matches_with_id = data[data["matchId"] == matchId]

    return matches_with_id


def get_team_side(matchId, teamId):
    data = pd.read_csv("dataset/events_World_Cup.csv")
    match = get_match(matchId)

    unique_team_ids = match["teamId"].unique()

    team_right = max(unique_team_ids)
    team_left = min(unique_team_ids)

    if team_right == teamId:
        return "right"
    else:
        return "left"


def simple_pass_map(matchId, pitch_height, pitch_width, ax):
    match_events = get_match(matchId)

    simple_pass_events = match_events[match_events["subEventName"] == "Simple pass"]

    for event in simple_pass_events.iterrows():
        circle = plt.Circle(
            (event["pos_orig_x"], event["pos_orig_y"]), 1, color="red", alpha=0.5
        )
        ax.add_patch(circle)
    return ax
