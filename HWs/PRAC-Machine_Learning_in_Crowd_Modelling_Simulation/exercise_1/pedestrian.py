from typing import Tuple


class Pedestrian:
    """
    Class representing the pedestrian object

    Attributes:
        position:               Current coordinates of the pedestrian
        ID:                     Identity number of the pedestrian
        SPEED:                  Move speed of the pedestrian within the grid
        TRACK_COLOR:            Color of the pedestrian's track
        has_arrived:            True if pedestrian has arrived to the target
        has_stuck:              True if pedestrian has stuck in the grid
    """

    def __init__(self, position: Tuple[int, int], idx: int, color: Tuple[int, int, int], speed: float = 1.0):
        self.position = position
        self.ID = idx
        self.SPEED = speed
        self.TRACK_COLOR = color
        self.has_arrived = False
        self.has_stuck = False

    def arrived(self):
        self.has_arrived = True

    def stuck(self):
        self.has_stuck = True
