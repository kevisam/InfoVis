import streamlit as st
import pandas as pd
import numpy as np
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

# TODO: Drop-down menu to select the match.
match_id = 2057954

# TODO: Drop-down menu to select the team (choose between team1_name, team2_name, or both).

# TODO: Drop-down menu to select the player.

# Drop-down menu to select the event type.
match = helper.get_match(match_id)
events = match["subEventName"].unique().tolist()
selected_events = st.sidebar.multiselect("Select an event type:", events)


#######################
# === Render page === #
#######################

# Render title
st.title("Football Game Statistics Visualized")

# Render introduction
st.markdown(
    """
    This app allows for the visualization of different actions and events that occurred during the football matches in 2016, 2017, and 2018. The visualizations can be controlled using a time slider.
    """
)

# Render header
st.write("")
st.write("")
st.subheader("Event visualizer")

# Render slider
end_time = 60 if (match["matchPeriod"] == "1H").any() else 120
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
        match=match,
        game_time=game_time,
        color=colors["Simple pass"],
        ax=ax,
    )

if "High pass" in selected_events:
    ax = event.high_pass_render(
        pitch_height=pitch_height,
        pitch_width=pitch_width,
        match=match,
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
st.write(helper.get_match(match_id))
