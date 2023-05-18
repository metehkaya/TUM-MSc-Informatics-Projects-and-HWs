from enum import Enum


class State(Enum):
    """
    Class representing the types of a Cell
    """
    EMPTY = 'E'
    PEDESTRIAN = 'P'
    OBSTACLE = 'O'
    TARGET = 'T'
    VISITED = 'V'
