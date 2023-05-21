def get_portrait_data_type():
    """
    Returns the portrait data type given by the user
    :returns: portrait data type such as focus_stable, node_stable, saddle_unstable_x_axis, etc.
    """
    portrait_data_types = ["focus_stable", "focus_unstable", "node_stable", "node_unstable", "saddle_unstable_x_axis",
                           "saddle_unstable_y_axis"]
    prompt = "Possible portrait data types are below:" + "\n"
    for idx, data_type in enumerate(portrait_data_types):
        prompt += str(idx+1) + ": " + data_type + "\n"
    portrait_data_type = int(input(prompt + "Enter the id (integer) corresponding portrait data type: "))
    data_type_exists = (1 <= portrait_data_type <= 6)
    return portrait_data_type, data_type_exists
