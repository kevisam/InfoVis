import pandas as pd

# remove unnecessary columns
df = pd.read_csv("./code/dataset/events_World_Cup.csv")
df.drop('eventId', axis=1, inplace=True)
df.drop('eventName', axis=1, inplace=True)
df.drop('subEventId', axis=1, inplace=True)
df.drop('tags', axis=1, inplace=True)
df.drop('tagsList', axis=1, inplace=True)
df.drop('positions', axis=1, inplace=True)

df.to_csv("./code/dataset/cleaned_data.csv", index=False)