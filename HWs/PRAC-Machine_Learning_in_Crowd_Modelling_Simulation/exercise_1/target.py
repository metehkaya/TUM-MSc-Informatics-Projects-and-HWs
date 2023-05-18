from typing import Tuple


class Target:
    """
    Class representing the target object

    Attributes:
        position:               Current coordinates of the pedestrian
        pedestrians_on_target:  List of pedestrians waiting on the target until the limit is exceeded
    """

    def __init__(self, position: Tuple[int, int]):
        self.INIT_POINTS = position
        self.pedestrians_on_target = []
