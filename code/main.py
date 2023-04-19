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



#######################
# === Render page === #
#######################

# Render title
st.title('Football Game Statistics Visualized')

# Render introduction
st.markdown(
    """
    This app allows for the visualization of different actions and events that occurred during World Cup football matches. The visualizations can be controlled using a time slider.
    """
    )

# Render header
st.subheader('Event visualizer.')
st.markdown(
    """
    The visualization below shows the chosen event performed during a chosen match, team(s), and player(s), controlled by the time slider (in minutes) below.
    """
    )

# Render slider
game_time = st.slider(label=" ", 
                      min_value=0,
                      max_value=120,
                      step=1)

# Define arrows on pitch
if selected_event == "Simple pass":
    helper.simple_pass_render(pitch_height=pitch_height,
                            pitch_width=pitch_width,
                            match_id=2057954, 
                            game_time=game_time, 
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
st.write(helper.get_match(match_id))