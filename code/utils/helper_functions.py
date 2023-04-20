import pandas as pd
from matplotlib import pyplot as plt
data_path = "./code/dataset/cleaned_data.csv"

def load_data(nrows):
    """ Loads and returns the football data """
    data = pd.read_csv(data_path, nrows=nrows)
    return data


def get_match(matchId):
    """ For a given match ID, returns the match data in a pandas dataframe """

    data = pd.read_csv(data_path)
    matches_with_id = data[data["matchId"] == matchId]
    return matches_with_id


def get_team_side(matchId, teamId):
    """ For a given match ID, and team ID returns the side on which the team plays on the pitch """
    
    data = pd.read_csv(data_path)
    match = get_match(matchId)
    unique_team_ids = match["teamId"].unique()

    team_right = max(unique_team_ids)
    team_left = min(unique_team_ids)

    if team_right == teamId:
        return "right"
    else:
        return "left"