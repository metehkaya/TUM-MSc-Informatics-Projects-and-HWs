import numpy as np


class PortraitDataset:
    """
    Class for retrieving portrait data

    Attributes:
        portrait_data_type:     type of portrait data such as focus_stable, node_stable, saddle_unstable_x_axis, etc.
    """

    def __init__(self, portrait_data_type: int):
        self.portrait_data_type = portrait_data_type
        self.functions = [self.get_focus_stable, self.get_focus_unstable, self.get_node_stable, self.get_node_unstable,
                          self.get_saddle_unstable_x_axis, self.get_saddle_unstable_y_axis]

    def get_portrait_data(self):
        """
        Returns the portrait data
        :returns: portrait data such as focus_stable, node_stable, saddle_unstable_x_axis, etc.
        """
        return self.functions[self.portrait_data_type-1]()

    @staticmethod
    def get_focus_stable():
        """
        :returns: portrait data with a type of focus stable
        """
        alpha = .1
        a_matrix = -np.array([[alpha, alpha], [-.25, 0]])
        timespan_time = 100
        timespan_freq = 100
        trajectories = []
        trajectories.append({"y0": np.array([1, -1]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 1"}})
        data = {"A": a_matrix, "trajectories": trajectories}
        return data

    @staticmethod
    def get_focus_unstable():
        """
        :returns: portrait data with a type of focus unstable
        """
        alpha = .1
        a_matrix = np.array([[alpha, alpha], [-.25, 0]])
        timespan_time = 99.5
        timespan_freq = 100
        trajectories = []
        trajectories.append({"y0": np.array([-.003, .011]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 1"}})
        data = {"A": a_matrix, "trajectories": trajectories}
        return data

    @staticmethod
    def get_node_stable():
        """
        :returns: portrait data with a type of node stable
        """
        a_matrix = np.array([[-0.1, 0], [0, -0.2]])
        timespan_time = 50
        timespan_freq = 100
        trajectories = []
        trajectories.append({"y0": np.array([1, 0]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 1"}})
        trajectories.append({"y0": np.array([-1, 0]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 2"}})
        trajectories.append({"y0": np.array([0, 1]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 3"}})
        trajectories.append({"y0": np.array([0, -1]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 4"}})
        trajectories.append({"y0": np.array([1, 1]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 5"}})
        trajectories.append({"y0": np.array([1, -1]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 6"}})
        trajectories.append({"y0": np.array([-1, 1]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 7"}})
        trajectories.append({"y0": np.array([-1, -1]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 8"}})
        data = {"A": a_matrix, "trajectories": trajectories}
        return data

    @staticmethod
    def get_node_unstable():
        """
        :returns: portrait data with a type of node unstable
        """
        a_matrix = np.array([[0.1, 0], [0, 0.2]])
        timespan_time_fast = 23
        timespan_time_slow = 46
        timespan_freq = 100
        trajectories = []
        trajectories.append({"y0": np.array([.01, 0]), "timespan": {"time": timespan_time_slow, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 1"}})
        trajectories.append({"y0": np.array([-.01, 0]), "timespan": {"time": timespan_time_slow, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 2"}})
        trajectories.append({"y0": np.array([0, .01]), "timespan": {"time": timespan_time_fast, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 3"}})
        trajectories.append({"y0": np.array([0, -.01]), "timespan": {"time": timespan_time_fast, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 4"}})
        trajectories.append({"y0": np.array([.1, .01]), "timespan": {"time": timespan_time_fast, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 5"}})
        trajectories.append({"y0": np.array([.1, -.01]), "timespan": {"time": timespan_time_fast, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 6"}})
        trajectories.append({"y0": np.array([-.1, .01]), "timespan": {"time": timespan_time_fast, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 7"}})
        trajectories.append({"y0": np.array([-.1, -.01]), "timespan": {"time": timespan_time_fast, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 8"}})
        data = {"A": a_matrix, "trajectories": trajectories}
        return data

    @staticmethod
    def get_saddle_unstable_x_axis():
        """
        :returns: portrait data with a type of saddle unstable (x-axis)
        """
        a_matrix = np.array([[0.1, 0], [0, -0.1]])
        timespan_time = 46
        timespan_freq = 100
        trajectories = []
        trajectories.append({"y0": np.array([.01, 0]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 1"}})
        trajectories.append({"y0": np.array([-.01, 0]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 2"}})
        trajectories.append({"y0": np.array([0, 1]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 4"}})
        trajectories.append({"y0": np.array([0, -1]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 4"}})
        trajectories.append({"y0": np.array([.01, .99]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 5"}})
        trajectories.append({"y0": np.array([.01, -.99]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 6"}})
        trajectories.append({"y0": np.array([-.01, .99]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 7"}})
        trajectories.append({"y0": np.array([-.01, -.99]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 8"}})
        data = {"A": a_matrix, "trajectories": trajectories}
        return data

    @staticmethod
    def get_saddle_unstable_y_axis():
        """
        :returns: portrait data with a type of saddle unstable (y-axis)
        """
        a_matrix = np.array([[-0.1, 0], [0, 0.1]])
        timespan_time = 46
        timespan_freq = 100
        trajectories = []
        trajectories.append({"y0": np.array([1, 0]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 1"}})
        trajectories.append({"y0": np.array([-1, 0]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 2"}})
        trajectories.append({"y0": np.array([0, .01]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 4"}})
        trajectories.append({"y0": np.array([0, -.01]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 4"}})
        trajectories.append({"y0": np.array([.99, .01]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 5"}})
        trajectories.append({"y0": np.array([.99, -.01]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 6"}})
        trajectories.append({"y0": np.array([-.99, .01]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 7"}})
        trajectories.append({"y0": np.array([-.99, -.01]), "timespan": {"time": timespan_time, "freq": timespan_freq},
                             "plot": {"color": "red", "label": "Trajectory 8"}})
        data = {"A": a_matrix, "trajectories": trajectories}
        return data
