import pandas as pd

# get events and remove unnecessary columns
events = pd.read_csv("./code/dataset/data_raw/events_World_Cup.csv")
events.drop('eventId', axis=1, inplace=True)
events.drop('eventName', axis=1, inplace=True)
events.drop('subEventId', axis=1, inplace=True)
events.drop('tags', axis=1, inplace=True)
events.drop('tagsList', axis=1, inplace=True)
events.drop('positions', axis=1, inplace=True)

# get match labels
matches = pd.read_csv("./code/dataset/data_raw/matches_World_Cup.csv")
matches = matches[["dateutc", "wyId", "label", "teamsData"]]
matches['match_name'] = matches.apply(lambda x: f"{x['label']} ({x['dateutc']})", axis=1)
matches.drop('dateutc', axis=1, inplace=True)
matches.drop('label', axis=1, inplace=True)

# get teams
teams = pd.read_csv("./code/dataset/data_raw/teams.csv")
teams = teams[["wyId", "officialName"]]

# get players
players = pd.read_csv("./code/dataset/data_raw/players.csv")
players.drop('birthArea', axis=1, inplace=True)
players.drop('firstName', axis=1, inplace=True)
players.drop('middleName', axis=1, inplace=True)
players.drop('lastName', axis=1, inplace=True)
players.drop('currentNationalTeamId', axis=1, inplace=True)

# print
print(events)
print(matches)
print(teams)
print(players)

# store data
events.to_csv("./code/dataset/data_clean/clean_events_data.csv", index=False)
matches.to_csv("./code/dataset/data_clean/clean_matches_data.csv", index=False)
teams.to_csv("./code/dataset/data_clean/clean_teams_data.csv", index=False)
players.to_csv("./code/dataset/data_clean/clean_players_data.csv", index=False)