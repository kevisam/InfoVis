def simple_pass_render(pitch_height, pitch_width, match, game_time, time_window, color, ax):
    """ For a given match ID and game time, returns plot elements that visualize the simple passes in the form of arrows """
    # get match data
    data = match[match["subEventName"] == "Simple pass"]
    data = data[data["eventSec"] >= game_time*60]
    data = data[data["eventSec"] <= game_time*60 + time_window*60]

    # create plot elements
    for idx, event in data.iterrows():
        start_point = (event["pos_orig_x"]/100*pitch_width, event["pos_orig_y"]/100*pitch_height)
        end_point = (event["pos_dest_x"]/100*pitch_width, event["pos_dest_y"]/100*pitch_height)
        ax.annotate('', xy=end_point, xytext=start_point,
            arrowprops=dict(facecolor=color, edgecolor=color, arrowstyle='->'))
    return ax


def high_pass_render(pitch_height, pitch_width, match, game_time, time_window, color, ax):
    """ For a given match ID and game time, returns plot elements that visualize the simple passes in the form of arrows """
    # get match data
    data = match[match["subEventName"] == "High pass"]
    data = data[data["eventSec"] >= game_time*60]
    data = data[data["eventSec"] <= game_time*60 + time_window*60]

    # create plot elements
    for idx, event in data.iterrows():
        start_point = (event["pos_orig_x"]/100*pitch_width, event["pos_orig_y"]/100*pitch_height)
        end_point = (event["pos_dest_x"]/100*pitch_width, event["pos_dest_y"]/100*pitch_height)
        ax.annotate('', xy=end_point, xytext=start_point,
            arrowprops=dict(facecolor=color, edgecolor=color, arrowstyle='->'))
    return ax