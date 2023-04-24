import pandas as pd
import streamlit as st

################
# === Paths ===#
################

events_path = "./code/dataset/data_clean/clean_events_data.csv"
matches_path = "./code/dataset/data_clean/clean_matches_data.csv"
teams_path = "./code/dataset/data_clean/clean_teams_data.csv"
players_path = "./code/dataset/data_clean/clean_players_data.csv"


####################
# === Functions ===#
####################


def load_all_events():
    """Loads and returns the football events data"""

    data = pd.read_csv(events_path)
    return data


def load_all_matches():
    """Loads and returns the football matches data"""

    data = pd.read_csv(matches_path)
    return data


def load_all_teams():
    """Loads and returns the football matches data"""

    data = pd.read_csv(teams_path)
    return data


def load_all_players():
    """Loads and returns the football matches data"""

    data = pd.read_csv(players_path)
    return data


def get_match_events(matchId, all_events_data, teamId, players):
    """For a given match ID and all events data, returns the match events data in a pandas dataframe"""

    filtered_data = all_events_data[all_events_data["matchId"] == matchId]
    filtered_data = filtered_data[filtered_data["teamId"] == teamId]
    if players == "all":
        return filtered_data
    else:
        filtered_data = filtered_data[filtered_data["playerId"].isin(players)]
        return filtered_data


def get_team_side(matchId, teamId, events_data):
    """For a given match ID, and team ID returns the side on which the team plays on the pitch"""

    data = pd.read_csv(events_path)
    match = get_match_events(matchId, events_data)
    unique_team_ids = match["teamId"].unique()

    team_right = max(unique_team_ids)
    team_left = min(unique_team_ids)

    if team_right == teamId:
        return "right"
    else:
        return "left"


def find_original_point(x, y, team_side, pitch_length, pitch_width, events_data):
    """For a given point on the field, return the original position in the dataset"""

    if team_side == "right":
        x = pitch_length - x

    original_x = round(x / pitch_length * 100)
    original_y = round(y / pitch_width * 100)

    filtered_data = events_data[
        (events_data["pos_orig_x"] == original_x)
        & (events_data["pos_orig_y"] == original_y)
    ]
    return filtered_data


def get_specific_match_data(matchId):
    data = load_all_matches()

    data = data[data["wyId"] == matchId]

    return data


def find_player(playerId):
    players_data = load_all_players()

    filtered_data = players_data[players_data["wyId"] == int(playerId)]
    return filtered_data


# Player plotting


def show_player_info(
    point, matchId, team_side, pitch_length, pitch_width, current_events
):
    origpoint = find_original_point(
        point["x"],
        point["y"],
        team_side,
        pitch_length,
        pitch_width,
        current_events,
    )
    playerId = origpoint["playerId"]
    player = find_player(playerId)
    match_team_id = str(int(origpoint["teamId"]))

    current_team_id = str(player["currentTeamId"])
    matchData = get_specific_match_data(matchId)
    matchData = matchData["teamsData"][0]
    matchData = eval(matchData.replace("'", '"'))

    # st.write("matchdata", matchData)
    # st.write("match_team_id", str(match_team_id))

    bench = matchData[match_team_id]["formation"]["bench"]
    lineup = matchData[match_team_id]["formation"]["lineup"]
    substitutions = matchData[match_team_id]["formation"]["substitutions"]

    for plyr in bench:
        if (plyr["playerId"] == playerId).any():
            st.markdown("Player was initially on the bench")

            for sub in substitutions:
                playerOut = find_player(sub["playerOut"])
                if (sub["playerIn"] == playerId).any():
                    st.markdown(
                        "Player came in at "
                        + str(sub["minute"])
                        + " minutes and replaced "
                        + str(playerOut["shortName"]).encode().decode("unicode_escape")
                    )

    for plyr in lineup:
        if (plyr["playerId"] == playerId).any():
            st.markdown("Player was in the lineup")

    # TODO: Add more info about the player

    # st.write("playerId", playerId)
    # st.write("Point:", point)
    # st.write("orig point", origpoint)
    # st.write("player", player)
