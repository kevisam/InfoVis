import streamlit as st
import pandas as pd
import numpy as np
from utils.visual_functions import createPitch
from utils.helper_functions import load_data, get_match, get_team_side, simple_pass_map
import plotly.graph_objects as go



################################
# === Define page objects === #
################################

# Define football pitch
pitch_width = 100
pitch_height = 60
fig, ax = createPitch(pitch_width, pitch_height, "green")



#######################
# === Render page === #
#######################

# Render title
st.title('Football Game Statistics Visualized')

# Render introduction
st.markdown(
    """
    This software allows for the visualization of different actions and events that occurred during World Cup football matches.
    """
    )

# Render pitch
fig.set_size_inches(15, 10)
st.pyplot(fig)

# Render slider
st.slider(label="Amount of data", 
          min_value=0,
          max_value=1000,
          step=50)

# Display match data
match = get_match(2057954)
st.write(match)