import json
import pandas as pd
import streamlit as st
import utils.event_functions as event
import utils.helper_functions as helper
import plotly.express as px
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
from plotly_football_pitch import (
    make_pitch_figure,
    PitchDimensions,
    SingleColourBackground,
)


###############################
# === Define page objects === #
###############################

# Global variables
selected_points_array = []

# Pitch dimensions
pitch_length = 104
pitch_width = 67
dimensions = PitchDimensions()

# Canvas dimensions
canvas_width = 700
canvas_height = 550

# Define football pitch
fig = make_pitch_figure(
    dimensions,
    pitch_background=SingleColourBackground("#A1BFA3"),
)
fig.update_layout(width=canvas_width, height=canvas_height)
fig.update_layout(hovermode="closest")

# Define colors for each event type
colors = {
    "Acceleration": "#B00000",
    "Air duel": "#FF6000",
    "Clearance": "#AF7900",
    "Corner": "#FFC200",
    "Cross": "#FBFF00",
    "Foul": "#C4DF00",
    "Free Kick": "#B9FF00",
    "Free kick cross": "#6DE100",
    "Goal kick": "#1DCA0B",
    "Ground attacking duel": "#2E9076",
    "Ground defending duel": "#00FFFF",
    "Ground loose ball duel": "#00CFFF",
    "Hand foul": "#00AFFF",
    "Hand pass": "#006FFF",
    "Head pass": "#000FFF",
    "High pass": "#4000FF",
    "Launch": "#6400FF",
    "Reflexes": "#8F00FF",
    "Save attempt": "#B200FF",
    "Shot": "#D500FF",
    "Simple pass": "#FF00EC",
    "Smart pass": "#FF00AA",
    "Throw in": "#393939",
    "Touch": "#767676",
}


##########################
# === Render sidebar === #
##########################

# Sidebar title
st.sidebar.title("Match settings")

# Drop-down menu to select the match #
# ================================== #
all_matches = helper.load_all_matches()
all_match_names = all_matches["match_name"].unique().tolist()
selected_match = st.sidebar.selectbox("Select a match:", all_match_names)
# ================================== #

# Drop-down menu to select the team #
# ================================= #
match_teamsData = json.loads(
    (
        all_matches.loc[all_matches["match_name"] == selected_match, "teamsData"].iloc[
            0
        ]
    ).replace("'", '"')
)
match_teamIds = list(match_teamsData.keys())
all_teams = helper.load_all_teams()
selected_match_team_names = (
    all_teams.loc[all_teams["wyId"] == int(match_teamIds[0]), "officialName"].iloc[0],
    all_teams.loc[all_teams["wyId"] == int(match_teamIds[1]), "officialName"].iloc[0],
)
selected_team = st.sidebar.selectbox("Select a team:", selected_match_team_names)
selected_teamId = all_teams.loc[
    all_teams["officialName"] == selected_team, "wyId"
].iloc[0]
## get team side
if selected_match.startswith(selected_team):
    team_side = "left"
else:
    team_side = "right"
# ================================= #

# Filter title
st.sidebar.title(" ")
st.sidebar.title("Filter settings")

# Drop-down menu to select the player #
# =================================== #
matchId = all_matches.loc[all_matches["match_name"] == selected_match, "wyId"].iloc[0]
all_players = helper.load_all_players()
all_match_events = helper.get_match_events(
    matchId=matchId,
    all_events_data=helper.load_all_events(),
    teamId=selected_teamId,
    players="all",
)
all_match_playerIds = all_match_events["playerId"].unique().tolist()
all_match_player_data = all_players[all_players["wyId"].isin(all_match_playerIds)]
all_match_player_names = all_match_player_data["shortName"].unique().tolist()
## decode names
name_encoding_dict = {}
for i in range(len(all_match_player_names)):
    raw_name = all_match_player_names[i]
    decoded_string = all_match_player_names[i].encode().decode("unicode_escape")
    all_match_player_names[i] = decoded_string
    name_encoding_dict[decoded_string] = raw_name
## create checkbox to filter by player
filter_by_player = st.sidebar.checkbox("Filter by player")
if filter_by_player:
    selected_players = st.sidebar.multiselect(
        "Select player(s):", all_match_player_names, key='selected_players'
    )
    ## store filtered player data
    selected_players_dict = {}
    for player_name in selected_players:
        player_data = all_players[all_players["shortName"] == name_encoding_dict[player_name]]
        playerId = player_data["wyId"].iloc[0]
        selected_players_dict[playerId] = player_data.iloc[0].to_dict()
    selected_player_Ids = selected_players_dict.keys()
else:
    ## store all player data
    selected_players_dict = {}
    for idx, row in all_match_player_data.iterrows():
        wyId = row["wyId"]
        selected_players_dict[wyId] = row.to_dict()
    selected_player_Ids = "all"
# =================================== #

# Drop-down menu to select the event type #
# ======================================= #
filtered_match_events = helper.get_match_events(
    matchId=matchId,
    all_events_data=helper.load_all_events(),
    teamId=selected_teamId,
    players=selected_player_Ids,
)
event_names = filtered_match_events["subEventName"].unique().tolist()
event_names = [element for element in event_names if isinstance(element, str)]
selected_events = st.sidebar.multiselect("Select event type(s):", sorted(event_names))
# ======================================= #


# Drop-down menu to select the arrow color #
# ======================================== #
if selected_events != []:
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.title("Colors")
    # create unique pairs for all events and players selected
    from itertools import product
    if 'selected_players' in st.session_state:
        pairs = list(product(selected_players, selected_events))
    else:
        pairs = list(product(["All players"], selected_events))

    color_col_0, color_col_1, color_col_2 = st.sidebar.columns([0.33,0.33,0.33])

    # suggest color for each pair
    selected_colors = {}
    for i,pair in enumerate(pairs):
        pair_player = pair[0]
        pair_event = pair[1]

        # get default color
        default_color = helper.create_color(pair_event, pair_player)

        if i%3 == 0:
            with color_col_0:
                col = st.color_picker(f"{pair_player}, {pair_event}", default_color, key=pair)
                st.write("")
                st.write("")
        elif i%3 == 1:
            with color_col_1:
                col = st.color_picker(f"{pair_player}, {pair_event}", default_color, key=pair)
                st.write("")
                st.write("")
        elif i%3 == 2:
            with color_col_2:
                col = st.color_picker(f"{pair_player}, {pair_event}", default_color, key=pair)
                st.write("")
                st.write("")
        
        # store selected color
        selected_colors[pair] = col
# ======================================= #


#######################
# === Render page === #
#######################

# Render title
st.title("Football Game Statistics Visualized")

# Render introduction
st.markdown(
    """
    This app allows for the visualization of player statistics and the different events \
        that occurred during the 2018 World Cup matches. The visualizations \
            can be controlled using the settings in the sidebar and the sliders in the main page.
    """
)

# Render header
st.write("")
st.write("")
st.subheader("Event analyzer")

selected_match_split = selected_match.replace(")", "").split("(")
selected_match_name = selected_match_split[0]
selected_match_datetime = selected_match_split[len(selected_match_split) - 1]
date, time = selected_match_datetime.split(" ")
st.markdown(
    f"You are now visualizing the game of &nbsp; '{selected_match_name}' &nbsp; \
        from the perspective of {selected_team}. This match took place \
            on {date} and started at {time}."
)

# Render slider
default_period = (0, 4)
slider_label = "The visualization below shows the locations of events \
    for a chosen event type, performed during a particular match, chosen team(s). \
    Events can be filtered by team or even by player. The time window (in minutes) \
        can be adjusted in the sidebar. The starting time (in minutes) can be set \
            using the slider below."
game_time = st.slider("Select a time window period: ", 0, 120, default_period, step=1)


################################
# === Define pitch objects === #
################################

# Define empty df for raw display of data
raw_df = filtered_match_events.drop(labels=filtered_match_events.index, axis=0)

# Define arrows on pitch
for event_name in selected_events:
    fig, high_pass_df = event.event_render(
        event_name=event_name,
        pitch_length=pitch_length,
        pitch_width=pitch_width,
        match=filtered_match_events,
        game_time=game_time,
        name_encoding_dict=name_encoding_dict,
        selected_colors=selected_colors,
        fig=fig,
        player_data=selected_players_dict,
        team_side=team_side,
    )
    raw_df = pd.concat([raw_df, high_pass_df], axis=0)

# Reset indexing on df for raw data display
raw_df = raw_df.reset_index(drop=True)


########################
# === Render pitch === #
########################

# Render pitch
fig.update_layout(
    title={
        "text": selected_match_name,
        "font": {"size": 20},
        "xanchor": "center",
        "x": 0.5,  # set x to 0.5 for center alignment
        "y": 0.92,  # adjust y position for desired vertical alignment
    }
)
fig.update_traces(
    showlegend=False
)  # Remove the legend on the traces. This removes the traces names

# Create a plot where we can retrieve on click events, and select events (Lasso or Rectangle selection)
selected_points = plotly_events(
    fig,
    select_event=True,
    click_event=True,
    override_height=canvas_height,  # Height of the canvas created
    override_width=canvas_width,  # Width of the canvas created
)

# Show the events related to each selected point
# Here we can add on click or on selection events for the points.
for point in selected_points:
    helper.show_player_info(
        point, matchId, team_side, pitch_length, pitch_width, raw_df
    )
    # TODO Add some stats about the players ?


#####################
# === Play game === #
#####################
import time

st.write("")
st.write("")
st.subheader("Game simulator")
st.markdown("Use the sliders to specify your settings. Press the play button to simulate the whole game.")

# Render play button and slider
play_button_column, play_speed_slider_column, play_time_slider_column, simulation_time = st.columns([0.1,0.2,0.3,0.4])

## Render simulation buttons
with play_button_column:
    st.write("")
    st.write("")
    play_button = st.button("▶")

with play_time_slider_column:
    time_window = st.slider("Select a time window period: ", 1, 15, step=1)

with play_speed_slider_column:
    play_speed = st.slider("Select a play speed: ", 1, 10, step=1)

with simulation_time:
    simulation_time = st.slider("Select a simulation time: ", 1, 120, step=1, value=10)

if play_button:
    st.write('<script>window.scrollTo(0,document.body.scrollHeight);</script>', unsafe_allow_html=True)
    # Set the time settings
    play_time = simulation_time - time_window
    play_window = [0, time_window]

    # Create an empty element to display the plot
    stop_button = st.button("Stop simulation", key='stop_simulation')
    play_plot = st.empty()

    for i in range(play_time+1):
        # Break if stop has been clicked
        if stop_button:
            break
        # Redefine football pitch
        fig = make_pitch_figure(
            dimensions,
            pitch_background=SingleColourBackground("#A1BFA3"),
        )
        fig.update_layout(width=canvas_width, height=canvas_height)
        fig.update_layout(hovermode="closest")

        # Redefine arrows on pitch
        for event_name in selected_events:
            fig, _ = event.event_render(
                event_name=event_name,
                pitch_length=pitch_length,
                pitch_width=pitch_width,
                match=filtered_match_events,
                game_time=play_window,
                name_encoding_dict=name_encoding_dict,
                selected_colors=selected_colors,
                fig=fig,
                player_data=selected_players_dict,
                team_side=team_side,
            )

        # Create a Plotly figure
        fig.update_layout(
            title={
                "text": selected_match_name + f"  (time: {play_window[0]} - {play_window[1]} min)",
                "font": {"size": 20},
                "xanchor": "center",
                "x": 0.5,  # set x to 0.5 for center alignment
                "y": 0.92,  # adjust y position for desired vertical alignment
            }
        )
        fig.update_traces(
            showlegend=False
        )

        # Reset plot
        play_plot.plotly_chart(fig)

        # Update play window
        play_window[0] += 1
        play_window[1] += 1

        # Wait
        time.sleep(2/play_speed)

    play_plot.empty()
    st.experimental_rerun()



############################
# === Raw data display === #
############################

# Raw data checkbox
st.sidebar.title("")
st.sidebar.title("Raw data settings")

# Render raw data when checkbox is ticked
show_raw_data = st.sidebar.checkbox("Show raw data")
if show_raw_data:
    st.write("")
    st.write("")
    st.subheader("Raw data")
    st.write(raw_df)
