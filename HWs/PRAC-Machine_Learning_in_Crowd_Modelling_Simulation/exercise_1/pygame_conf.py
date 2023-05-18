import json
import math

import pygame

from color import Color
from singleton import Singleton


@Singleton
class PygameConfiguration:
    """
    Class representing `pygame` configuration. They are populated via file named `pygame_configuration.json`
    Attributes:
        WINDOW_WIDTH:               Pixel-based width of the window for pygame
        WINDOW_HEIGHT:              Pixel-based height of the window for pygame
        N_ROW:                      Number of rows in the grid
        N_COL:                      Number of columns in the grid
        CELL_SIZE_BY_ROW:           Pixel-based height of the cell
        CELL_SIZE_BY_COL:           Pixel-based width of the cell
        DISTANCE_BY_ROW:            Distance between two not-diagonally adjacent rows
        DISTANCE_BY_COL:            Distance between two not-diagonally adjacent columns
        DISTANCE_BY_DIAG:           Distance between two diagonally adjacent rows
        OBSTACLE_AVOIDANCE_FLAG:    The flag that indicates the pedestrian behavior. Obstacle will be avoided if set as 1
        OBSTACLE_EXTRA_COST:        Cost to be used during computation of the best paths
        STOP_DISPLAY_AFTER_STUCK:   The flag that finishes the display for the pedestrians who got stuck
        DISPLAY_DELTA_TIMESTAMP:    The time difference between consecutive displays
        END_FREEZE:                 The number of seconds to wait at the end of the simulation
        SS_FOLDER_NAME:             The folder name under img directory to save the screenshots of the simulation
        SS_START:                   The flag used to take a screenshot of the initial grid
        SS_FINAL:                   The flag used to take a screenshot of the final grid
        SS_PERIOD:                  The period used to take screenshots of the grid periodically, put 0 otherwise
        GRID:                       Field containing pedestrian, obstacle (optional) and target coordinates.
        STEP_LIMIT:                 Upper bound to limit move count
        SCREEN:                     Screen to be coupled with pygame
    """

    def __init__(self):
        """
        Populate attributes via a file
        """
        with open('pygame_configuration.json') as f:
            parameters = json.load(f)
        pygame.init()
        window_size = parameters["WINDOW_SIZE"]
        self.WINDOW_WIDTH = window_size['WINDOW_WIDTH']
        self.WINDOW_HEIGHT = window_size['WINDOW_HEIGHT']
        grid_size = parameters["GRID_SIZE"]
        self.N_ROW = grid_size['N_ROW']
        self.N_COL = grid_size['N_COL']
        self.CELL_SIZE_BY_ROW = self.WINDOW_HEIGHT // self.N_ROW
        self.CELL_SIZE_BY_COL = self.WINDOW_WIDTH // self.N_COL
        cell_distance = parameters["CELL_DISTANCE"]
        self.DISTANCE_BY_ROW = float(cell_distance['DISTANCE_BY_ROW'])
        self.DISTANCE_BY_COL = float(cell_distance['DISTANCE_BY_COL'])
        self.DISTANCE_BY_DIAG = math.sqrt(self.DISTANCE_BY_ROW ** 2 + self.DISTANCE_BY_COL ** 2)
        obstacle_flags = parameters["OBSTACLE_FLAGS"]
        self.OBSTACLE_AVOIDANCE_FLAG = obstacle_flags['OBSTACLE_AVOIDANCE_FLAG']
        self.OBSTACLE_EXTRA_COST = float(obstacle_flags['OBSTACLE_EXTRA_COST'])
        display = parameters["DISPLAY"]
        self.STOP_DISPLAY_AFTER_STUCK = display['STOP_DISPLAY_AFTER_STUCK']
        self.DISPLAY_DELTA_TIMESTAMP = float(display['DISPLAY_DELTA_TIMESTAMP'])
        self.END_FREEZE = float(display['END_FREEZE'])
        screenshot = parameters['SCREENSHOT']
        self.SS_FOLDER_NAME = screenshot['SS_FOLDER_NAME']
        self.SS_START = screenshot['SS_START']
        self.SS_FINAL = screenshot['SS_FINAL']
        self.SS_PERIOD = screenshot['SS_PERIOD']
        self.GRID = parameters['GRID']
        self.STEP_LIMIT = None

        if parameters['STEP_LIMIT']['ACTIVE']:
            self.STEP_LIMIT = parameters['STEP_LIMIT']['VALUE']

        pygame.display.set_caption('Crowd modeling')
        self.SCREEN = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.SCREEN.fill(Color.BLACK.value)
