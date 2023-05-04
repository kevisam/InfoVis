import json
from datetime import datetime


def event_render(
    event_name, pitch_length, pitch_width, match, game_time, color, fig, player_data, team_side
):
    """
    For a given match ID and game time, returns plot elements that
    visualize the simple passes in the form of arrows.
    """

    # get match data
    data = match[match["subEventName"] == event_name]
    data = data[data["eventSec"] >= game_time[0] * 60]
    data = data[data["eventSec"] <= game_time[1] * 60]

    # create plot elements
    for idx, event in data.iterrows():
        # get position coordinates
        start_point = [
            event["pos_orig_x"] / 100 * pitch_length,
            event["pos_orig_y"] / 100 * pitch_width,
        ]
        end_point = [
            event["pos_dest_x"] / 100 * pitch_length,
            event["pos_dest_y"] / 100 * pitch_width,
        ]
        # adjust positions based on team side
        if team_side == "right":
            start_point[0] = pitch_length - start_point[0]
            end_point[0] = pitch_length - end_point[0]

        # get player data
        player_id = event["playerId"]
        name = player_data[player_id]["shortName"].encode().decode("unicode-escape")
        role = json.loads(player_data[player_id]["role"].replace("'", '"'))["name"]
        foot = player_data[player_id]["foot"]
        height = player_data[player_id]["height"]
        weight = player_data[player_id]["weight"]
        country = json.loads(player_data[player_id]["passportArea"].replace("'", '"'))[
            "name"
        ]
        birthdate = player_data[player_id]["birthDate"]
        birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
        age = int((datetime.now() - birthdate).days / 365)

        xpos = event["pos_orig_x"] / 100 * pitch_length
        ypos = event["pos_orig_y"] / 100 * pitch_width

        # create arrow
        fig.add_annotation(
            axref="x",
            ayref="y",
            x=end_point[0],
            y=end_point[1],
            ax=start_point[0],
            ay=start_point[1],
            text="",
            arrowhead=1,
            showarrow=True,
            arrowcolor=color,
            arrowwidth=3,
            opacity=0.75,
        )

        # Add interactive point at start of the arrow
        fig.add_scatter(
            x=[start_point[0]],
            y=[start_point[1]],
            mode="markers",
            marker={"size": 7, "color": color},
            hovertemplate=f"Name: &nbsp; {name}<br>"
            + f"Role: &nbsp; {role}<br>"
            + f"Age: &nbsp; {age}<br>"
            + f"Height: &nbsp; {height}cm<br>"
            + f"Weight: &nbsp; {weight}kg<br>"
            + f"Foot: &nbsp; {foot}<br>"
            + f"Country: &nbsp; {country}<br>"
            + f"Xpos: &nbsp; {xpos:.2f}m<br>"
            + f"Ypos: &nbsp; {ypos:.2f}m<br>"
            + f"Event: &nbsp; {event_name}<br>"
            + f"<extra></extra>",  # Remove the trace number
        )
    return fig, data