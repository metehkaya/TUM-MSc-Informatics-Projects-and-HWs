from direction import Direction


class Path:
    """
    Class representing the path for a pedestrian going through an adjacent cell

    Attributes:
        PATH_DIST:      distance of current cell to the target going through the given adjacent cell
        DIRECTION:      direction of the first step of the path to the target going through the given adjacent cell
    """

    def __init__(self, path_dist: float, direction: Direction):
        self.PATH_DIST = path_dist
        self.DIRECTION = direction
