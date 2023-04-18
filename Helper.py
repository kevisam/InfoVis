import pandas as pd


def load_data(nrows):
    data = pd.read_csv("Dataset/events_World_Cup.csv", nrows=nrows)

    return data


def get_match(data, matchId):
    # Filter the matches with ID 0
    matches_with_id = data[data["matchId"] == matchId]

    return matches_with_id


def get_team_side(data, matchId, teamId):
    match = get_match(data, matchId)

    unique_team_ids = match["teamId"].unique()

    team_right = max(unique_team_ids)
    team_left = min(unique_team_ids)

    if team_right == teamId:
        return "right"
    else:
        return "left"
