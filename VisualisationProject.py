import streamlit as st
import pandas as pd
import numpy as np

from FootballPitchVis import createPitch


# Create pitch plot
pitch_width = 120
pitch_height = 80
fig, ax = createPitch(pitch_width, pitch_height, "yards", "gray")

st.title("Soccer game information")

# Create pitch plot
pitch_width = 120
pitch_height = 80
fig, ax = createPitch(pitch_width, pitch_height, "yards", "gray")


def load_data(nrows):
    data = pd.read_csv("Database/events_World_Cup.csv", nrows=nrows)

    return data


hour_to_filter = st.slider("Amount of data", 0, 100, 50)

data_load_state = st.text("Loading data...")
data = load_data(hour_to_filter)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)
