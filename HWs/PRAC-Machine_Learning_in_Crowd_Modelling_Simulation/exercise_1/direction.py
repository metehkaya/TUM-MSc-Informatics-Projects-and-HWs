from typing import Tuple


class Direction:
    """
    Class representing the directions and their distance costs for pedestrians

    Attributes:
        DIR_X:              Change in the row id of the given direction
        DIR_Y:              Change in the column id of the given direction
        DIR_COST:           Cost of going to the adjacent cell in the given direction
    """

    def __init__(self, direction: Tuple[int, int], dir_cost: float):
        self.DIR_X = direction[0]
        self.DIR_Y = direction[1]
        self.DIR_COST = dir_cost
