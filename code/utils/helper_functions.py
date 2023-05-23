import pandas as pd
import streamlit as st
import plotly.figure_factory as ff

################
# === Paths ===#
################

events_path = "./code/dataset/data_clean/clean_events_data.csv"
matches_path = "./code/dataset/data_clean/clean_matches_data.csv"
teams_path = "./code/dataset/data_clean/clean_teams_data.csv"
players_path = "./code/dataset/data_clean/clean_players_data.csv"
rank_path = "./code/dataset/data_clean/playerank.csv"

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


def rank_rescaler(x, old_max, old_min):
    y = 1/(old_max-old_min) * x - (1/(old_max-old_min))*old_min
    return y


def get_playerrank_data():
    data = pd.read_csv(rank_path)

    # scale scores
    old_max = data['playerankScore'].max()
    old_min = data['playerankScore'].min()

    data['playerankScore'] = rank_rescaler(data['playerankScore'], old_max, old_min)
    return data


def get_playerrank(playerId, matchId):
    data = get_playerrank_data()

    match_data = data[data["matchId"] == int(matchId)]
    player_data = match_data[match_data["playerId"] == int(playerId)]

    return player_data


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
    matchData = matchData["teamsData"].iloc[0]
    matchData = eval(matchData.replace("'", '"'))
    playerRankData = get_playerrank_data()
    matchRankData = playerRankData[playerRankData["matchId"] == matchId]

    bench = matchData[match_team_id]["formation"]["bench"]
    lineup = matchData[match_team_id]["formation"]["lineup"]
    substitutions = matchData[match_team_id]["formation"]["substitutions"]
    playerInfo = []
    playerRank = get_playerrank(playerId, matchId)
    playerScore = playerRank["playerankScore"].iloc[0]

    entranceTime = ""
    cardText = ""
    for plyr in bench:
        if (plyr["playerId"] == playerId).any():
            cardText += "Player was initially on the bench. "
            playerInfo = plyr
            for sub in substitutions:
                playerOut = find_player(sub["playerOut"])
                if (sub["playerIn"] == playerId).any():
                    entranceTime = (
                        "Replaced "
                        + str(
                            playerOut["shortName"]
                            .iloc[0]
                            .encode()
                            .decode("unicode_escape")
                        )
                        + " at "
                        + str(sub["minute"])
                        + "min. "
                    )

    for plyr in lineup:
        if (plyr["playerId"] == playerId).any():
            playerInfo = plyr
            entranceTime = "Player was in the lineup."

    st.subheader(f"Player stats: {player['shortName'].iloc[0].encode().decode('unicode_escape')}")

    col1, col2, col3 = st.columns(3)

    if playerInfo["goals"] != "null":
        col1.info(f"Goals: {playerInfo['goals']} ", icon="🥇")
    else:
        col1.info(f"Goals: 0 ", icon="🥇")
    col1.info(f"Assists: {playerInfo['assists']} ", icon="🥈")
    col2.info(f"Red cards: {playerInfo['redCards']} ", icon="🟥")
    col2.info(f"Yellow cards: {playerInfo['yellowCards']} ", icon="🟨")
    col3.info(entranceTime, icon="ℹ️")
    col3.info(f"Minutes played: {int(playerRank['minutesPlayed'])}", icon="⏱️")

    fig = ff.create_distplot(
        [matchRankData["playerankScore"]], ["Distribution of Player Rank Scores"], 0.025
    )

    # Add a vertical line at the specified value
    fig.update_layout(
        shapes=[
            dict(
                type="line",
                x0=playerScore,
                x1=playerScore,
                yref="paper",
                y0=0,
                y1=1,  # fraction of plot height
                line=dict(color="red", width=2, dash="dash"),
                name="Player's Score",
            )
        ],
        xaxis=dict(title="Player Rank Score Range", tickformat=".0%"),
        yaxis=dict(title="Number of Players"),
        title=f"Rank score of {player['shortName'].iloc[0].encode().decode('unicode_escape')} compared to other players in the match",
    )

    return st.plotly_chart(fig)


def create_player_color(default_color, player_name):
    decimal_number = int(default_color, 16)
    decimal_number += len(player_name)**2
    hex_number = hex(decimal_number)[2:].zfill(len(default_color))
    return f"#{hex_number}"