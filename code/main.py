import streamlit as st
import pandas as pd
import numpy as np
import json
import utils.event_functions as event
import utils.visual_functions as visual
import utils.helper_functions as helper


###############################
# === Define page objects === #
###############################

# Define football pitch
pitch_width = 100
pitch_height = 60
fig, ax = visual.createPitch(pitch_width, pitch_height, "green")

# Define available colors (available = 1 ; not available = 0)
colors = {
    "Simple pass": "blue",
    "High pass": "red",
}


##########################
# === Render sidebar === #
##########################

# Drop-down menu to select the match.
all_matches = helper.load_all_matches()
all_match_names = all_matches["match_name"].unique().tolist()
selected_match = st.sidebar.selectbox("Select a match:", all_match_names)

# Drop-down menu to select the team (choose between team1_name, team2_name, or both).
teamIds = list(json.loads((all_matches.loc[all_matches['match_name'] == selected_match, 'teamsData'].iloc[0]).replace("'", "\"")).keys())
all_teams = helper.load_all_teams()
selected_match_teams = (all_teams.loc[all_teams['wyId'] == int(teamIds[0]), 'officialName'].iloc[0],
                        all_teams.loc[all_teams['wyId'] == int(teamIds[1]), 'officialName'].iloc[0])
selected_team = st.sidebar.selectbox("Select a team:", selected_match_teams)
selected_teamId = all_teams.loc[all_teams['officialName'] == selected_team, 'wyId'].iloc[0]

# TODO: Drop-down menu to select the player.

# Drop-down menu to select the event type.
match_id = all_matches.loc[all_matches['match_name'] == selected_match, 'wyId'].iloc[0]
match_events = helper.get_match_events(matchId=match_id, all_events_data=helper.load_all_events(), teamId=selected_teamId)
event_names = match_events["subEventName"].unique().tolist()
selected_events = st.sidebar.multiselect("Select an event type:", event_names)


#######################
# === Render page === #
#######################

# Render title
st.title("Football Game Statistics Visualized")

# Render introduction
st.markdown(
    """
    This app allows for the visualization of different actions and events that occurred during the 2018 World Cup matches. The visualizations can be controlled using a time slider.
    """
)

# Render header
st.write("")
st.write("")
st.subheader("Event visualizer")

# Render slider
end_time = 60 if (match_events["matchPeriod"] == "1H").any() else 120
slider_label = "The visualization below shows the locations of events for a chosen event type, performed during a particular match, chosen team(s). Events can be filtered by team or even by player. The time window (in minutes) can be adjusted in the sidebar. The starting time (in minutes) can be set using the slider below."
game_time = st.slider("Select a time period: ", 0, end_time, (0, 5), step=1)


################################
# === Define pitch objects === #
################################

# Define arrows on pitch
if "Simple pass" in selected_events:
    ax = event.simple_pass_render(
        pitch_height=pitch_height,
        pitch_width=pitch_width,
        match=match_events,
        game_time=game_time,
        color=colors["Simple pass"],
        ax=ax,
    )

if "High pass" in selected_events:
    ax = event.high_pass_render(
        pitch_height=pitch_height,
        pitch_width=pitch_width,
        match=match_events,
        game_time=game_time,
        color=colors["High pass"],
        ax=ax,
    )


#######################
# === Render pitch === #
#######################

# Render pitch
fig.set_size_inches(15, 10)
st.pyplot(fig)


#######################
# === For testing === #
#######################

# Render raw data
st.write("")
st.write("")
st.subheader("Raw data")
st.write(match_events)
