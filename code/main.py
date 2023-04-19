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
st.subheader('Simple pass visualizer.')
st.markdown(
    """
    For demonstrative purposes, the visualization below shows passes performed on a given match, controlled by the time slider below.
    """
    )

# Render slider
game_time = st.slider(label=" ", 
                      min_value=0,
                      max_value=120,
                      step=1)

# Define arrows on pitch
helper.simple_pass_render(pitch_height=pitch_height,
                          pitch_width=pitch_width,
                          match_id=2057954, 
                          game_time=game_time, 
                          ax=ax)

# Render pitch
fig.set_size_inches(15, 10)
st.pyplot(fig)