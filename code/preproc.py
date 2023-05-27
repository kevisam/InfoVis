import pandas as pd

# Get events and remove unnecessary columns
events = pd.read_csv("./code/dataset/data_raw/events_World_Cup.csv")
events = events[
    [
        "id",
        "subEventName",
        "matchId",
        "teamId",
        "playerId",
        "matchPeriod",
        "eventSec",
        "pos_orig_y",
        "pos_orig_x",
        "pos_dest_y",
        "pos_dest_x",
    ]
]
# add actions
events["action"] = 0
events["action"] = events.groupby("matchId", group_keys=False)["teamId"].apply(
    lambda x: (x != x.shift()).cumsum()
)
events["action"] = "action" + events["action"].astype(str)

# Preprocess bugged passes in the dataset
for i in range(len(events) - 1):
    current_row = events.iloc[i]
    next_row = events.iloc[i + 1]
    if (
        current_row["pos_orig_y"] == current_row["pos_dest_y"]
        and current_row["pos_dest_x"] == current_row["pos_orig_x"]
    ):
        events.at[i, "pos_dest_x"] = next_row["pos_orig_x"]
        events.at[i, "pos_dest_y"] = next_row["pos_orig_y"]


# Get matches
matches = pd.read_csv("./code/dataset/data_raw/matches_World_Cup.csv")
matches = matches[["dateutc", "wyId", "label", "teamsData"]]
matches["match_name"] = matches.apply(
    lambda x: f"{x['label']} ({x['dateutc']})", axis=1
)
matches = matches[["wyId", "match_name", "teamsData"]]


# Get teams
teams = pd.read_csv("./code/dataset/data_raw/teams.csv")
teams = teams[["wyId", "officialName"]]


# Get players
players = pd.read_csv("./code/dataset/data_raw/players.csv")
players = players[
    [
        "wyId",
        "shortName",
        "role",
        "currentTeamId",
        "foot",
        "height",
        "weight",
        "birthDate",
        "passportArea",
    ]
]


# Print
print(events)
print(matches)
print(teams)
print(players)


# Store data
events.to_csv("./code/dataset/data_clean/clean_events_data.csv", index=False)
matches.to_csv("./code/dataset/data_clean/clean_matches_data.csv", index=False)
teams.to_csv("./code/dataset/data_clean/clean_teams_data.csv", index=False)
players.to_csv("./code/dataset/data_clean/clean_players_data.csv", index=False)
