import json

from singleton import Singleton


@Singleton
class SimulationConfiguration:
    """
    Class representing simulation configuration. They are populated via file named `configuration.json`
    Attributes:
        OUTPUT_FOLDER_PATHS:        Path to output folders of the simulation software called vadere
        CSV_GROUP_ID_COLUMN_NAME:   Column name in the output csv file for group id of pedestrians
        FIGURE_PATH                 The path to save resulting plot of SIR groups
    """

    def __init__(self):
        """
        Populate attributes via a file
        """
        with open('configuration.json') as f:
            parameters = json.load(f)
        self.OUTPUT_FOLDER_PATHS = parameters["OUTPUT_FOLDER_PATHS"]
        self.CSV_GROUP_ID_COLUMN_NAME = parameters["CSV_GROUP_ID_COLUMN_NAME"]
        self.FIGURE_PATH = parameters["FIGURE_PATH"]