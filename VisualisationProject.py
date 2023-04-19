import streamlit as st
import pandas as pd
import numpy as np
from FootballPitchVis import createPitch
from Helper import load_data, get_match, get_team_side, simple_pass_map
import plotly.graph_objects as go


# Create pitch plot
pitch_width = 120
pitch_height = 80
fig, ax = createPitch(pitch_width, pitch_height, "yards", "gray")

fig.set_size_inches(15, 10)
st.pyplot(fig)

hour_to_filter = st.slider("Amount of data", 0, 1000, 50)

hour_to_filter = 10000

# data_load_state = st.text("Loading data...")
data = load_data(hour_to_filter)

match = get_match(2057954)


ax = simple_pass_map(2057954, pitch_height, pitch_width, ax)
