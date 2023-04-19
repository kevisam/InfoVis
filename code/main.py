import streamlit as st
import pandas as pd
import numpy as np
import utils.visual_functions as visual
import utils.helper_functions as helper
import plotly.graph_objects as go



###############################
# === Define page objects === #
###############################

# Define football pitch
pitch_width = 100
pitch_height = 60
fig, ax = visual.createPitch(pitch_width, pitch_height, "green")



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
selected_event = st.sidebar.selectbox("Select an event type:", events)

# Drop-down menu to select the time window.
time_window = st.sidebar.number_input("Select time window (minutes): ", step=1, value=1)



#######################
# === Render page === #
#######################

# Render title
st.title('Football Game Statistics Visualized')

# Render introduction
st.markdown(
    """
    This app allows for the visualization of different actions and events that occurred during the football matches in 2016, 2017, and 2018. The visualizations can be controlled using a time slider.
    """
    )

# Render header
st.write("");st.write("")
st.subheader('Event visualizer')


# Render slider
slider_label = "The visualization below shows the locations of events for a chosen event type, performed during a particular match, chosen team(s). Events can be filtered by team or even by player. The time window (in minutes) can be adjusted in the sidebar. The starting time (in minutes) can be set using the slider below."
game_time = st.slider(label=slider_label, 
                      min_value=0,
                      max_value=120,
                      step=1)

# Define arrows on pitch
if selected_event == "Simple pass":
    helper.simple_pass_render(pitch_height=pitch_height,
                            pitch_width=pitch_width,
                            match_id=2057954, 
                            game_time=game_time, 
                            time_window=time_window,
                            ax=ax)
else:
    pass



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
st.write("");st.write("")
st.subheader('Raw data')
st.write(helper.get_match(match_id))