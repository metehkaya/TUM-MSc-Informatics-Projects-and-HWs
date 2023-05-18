import json

import pygame
import random
import os
import shutil

from cell import Cell
from pedestrian import Pedestrian
from target import Target
from pygame_conf import PygameConfiguration
from state import State


class Grid:
    """
    Class representing the grid object
    Attributes:
        n_screenshot:   Number of screenshots taken of the simulation
        pedestrians:    Stores pedestrians with their positions
        cells:          List where the Cell objects are stored
        TARGET_CELL:    The (only) target cell object
    """

    def __init__(self):

        # fetch singleton object
        pygame_conf = PygameConfiguration.instance()
        grid_configuration = pygame_conf.GRID
        self.n_screenshot = 0

        self.cells = []
        for row in range(pygame_conf.N_ROW):
            row_cells = []
            for col in range(pygame_conf.N_COL):
                new_cell = Cell((row * pygame_conf.CELL_SIZE_BY_ROW, col * pygame_conf.CELL_SIZE_BY_COL))
                row_cells.append(new_cell)
            self.cells.append(row_cells)

        self.pedestrians = []
        # read the pedestrian attributes from config then process them
        for pedestrian_id, pedestrian_position in enumerate(grid_configuration['PEDESTRIANS']):
            pedestrian_x, pedestrian_y, pedestrian_speed = tuple(pedestrian_position)
            # set a random color for the track which pedestrian is going to form
            color = tuple(random.randint(0, 255) for _ in range(3))
            new_pedestrian = Pedestrian((pedestrian_x, pedestrian_y), pedestrian_id, color, float(pedestrian_speed))
            self.pedestrians.append(new_pedestrian)
            self.cells[pedestrian_x][pedestrian_y].set_state(State.PEDESTRIAN)

        if 'OBSTACLES' in grid_configuration:
            # read the obstacle attributes from config then process them
            obstacles = grid_configuration['OBSTACLES']
            for obstacle_position in obstacles:
                rect_top_left_x, rect_top_left_y, rect_bottom_right_x, rect_bottom_right_y = tuple(obstacle_position)
                for obstacle_x in range(rect_top_left_x, rect_bottom_right_x+1):
                    for obstacle_y in range(rect_top_left_y, rect_bottom_right_y+1):
                        self.cells[obstacle_x][obstacle_y].set_state(State.OBSTACLE)

        # specify target cell in the grid
        target_x, target_y = tuple(grid_configuration['TARGET'])
        self.cells[target_x][target_y].set_state(State.TARGET)
        self.TARGET_CELL = Target((target_x, target_y))

    def draw_grid(self, screenshot: bool = False):
        """
        Initiates pygame then displays the grid on the screen using pygame
        :param screenshot:  The flag used to take a screenshot of the grid or not
        :return:            None
        """
        pygame_conf = PygameConfiguration.instance()
        for row in range(pygame_conf.N_ROW):
            for col in range(pygame_conf.N_COL):
                cur_cell = self.cells[row][col]
                x, y = cur_cell.INIT_POINTS
                rect = pygame.Rect(y, x, pygame_conf.CELL_SIZE_BY_ROW, pygame_conf.CELL_SIZE_BY_COL)
                if cur_cell.state is State.VISITED:
                    pygame.draw.rect(pygame_conf.SCREEN, cur_cell.color, rect)
                else:
                    pygame.draw.rect(pygame_conf.SCREEN, cur_cell.color.value, rect)
        pygame.display.update()
        if screenshot:
            self.take_screenshot()

    def take_screenshot(self):
        """
        Takes the screenshot of the grid
        :return:    None
        """
        pygame_conf = PygameConfiguration.instance()
        cwd = os.getcwd()
        dir_path = os.path.join(cwd, "img", pygame_conf.SS_FOLDER_NAME)
        if self.n_screenshot == 0:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
            os.makedirs(dir_path)
        self.n_screenshot += 1
        img_name = "img_" + str(self.n_screenshot) + ".jpg"
        img_path = os.path.join(dir_path, img_name)
        pygame.image.save(pygame_conf.SCREEN, img_path)
