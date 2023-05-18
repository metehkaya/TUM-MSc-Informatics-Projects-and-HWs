from typing import Tuple

from color import Color
from state import State

# dictionary to ease color assignments to the cells using state
state_color_dict = {
    'E': Color.WHITE,
    'P': Color.RED,
    'O': Color.BLACK,
    'T': Color.YELLOW
}


class Cell:
    """
    Class representing a cell in the grid
    Attributes:
        INIT_POINTS:    Initial 2-D coordinates of the cell in the format of (x, y)
        state:          The state of a cell, might be Empty, Pedestrian etc.
        color:          The color of a cell - dependent on state
        is_accessible:  Indicates if the cell is accessible i.e. either it's a part of an obstacle or not
    """

    def __init__(self, init_points: Tuple[int, int]):
        self.INIT_POINTS = init_points
        self.state = State.EMPTY
        self.color = Color.WHITE
        self.is_accessible = True

    def set_state(self, new_state: State, color: Tuple[int, int, int] = None):
        """
        Function to set the new state of the cell. Updates state, color and changes accessibility if required
        :param new_state: New state of the cell
        :param color:     New color of the cell. Might be a random path color or the predefined colors
        :return:          None
        """
        self.state = new_state
        if new_state is State.VISITED:
            self.color = color
        else:
            self.color = state_color_dict[self.state.value]
            if new_state is State.OBSTACLE:
                self.is_accessible = False
