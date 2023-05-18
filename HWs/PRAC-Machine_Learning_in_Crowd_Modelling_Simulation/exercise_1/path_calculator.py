from grid import Grid
from state import State
from path import Path
from direction import Direction
from queue import PriorityQueue
from pygame_conf import PygameConfiguration


class PathCalculator:
    """
    Class for calculation of shortest path

    Attributes:
        grid:           Grid to be controlled
        visited:        2D array to store the information that indicates if a cell is visited previously
        dist_to_target: 2D array storing distance of cells to the target cell
        all_best_paths: The best paths (adjacent cells) to follow to reach the target for all cells
        DIRECTIONS:     2D array storing 8 possible directions (4 by row, 4 by column)
    """

    def __init__(self, grid: Grid):
        self.grid = grid
        self.visited = None
        self.dist_to_target = None
        self.all_best_paths = None
        pygame_conf = PygameConfiguration.instance()
        self.DIRECTIONS = [Direction((1, 0), pygame_conf.DISTANCE_BY_ROW),
                           Direction((-1, 0), pygame_conf.DISTANCE_BY_ROW),
                           Direction((0, 1), pygame_conf.DISTANCE_BY_COL),
                           Direction((0, -1), pygame_conf.DISTANCE_BY_COL),
                           Direction((1, 1), pygame_conf.DISTANCE_BY_DIAG),
                           Direction((1, -1), pygame_conf.DISTANCE_BY_DIAG),
                           Direction((-1, 1), pygame_conf.DISTANCE_BY_DIAG),
                           Direction((-1, -1), pygame_conf.DISTANCE_BY_DIAG)]

    def dijkstra(self):
        """
        The dijkstra algorithm to find the distance between the target cell and all cells
        :return: None
        """
        pygame_conf = PygameConfiguration.instance()
        n_row, n_col = pygame_conf.N_ROW, pygame_conf.N_COL
        obstacle_avoidance_flag = pygame_conf.OBSTACLE_AVOIDANCE_FLAG
        obstacle_extra_cost = pygame_conf.OBSTACLE_EXTRA_COST
        target_x, target_y = self.grid.TARGET_CELL.INIT_POINTS
        heap = PriorityQueue()
        heap.put((.0, target_x, target_y))

        # initializations
        self.visited = [[False for _ in range(n_col)] for _ in range(n_row)]
        self.dist_to_target = [[float("inf") for _ in range(n_col)] for _ in range(n_row)]
        self.dist_to_target[target_x][target_y] = .0

        # dijkstra's implementation with priority queue
        while not heap.empty():
            dist, x, y = heap.get()
            if self.visited[x][y]:
                continue
            self.visited[x][y] = True
            for direction in self.DIRECTIONS:
                new_x = x + direction.DIR_X
                new_y = y + direction.DIR_Y
                # check out of boundary case
                if new_x < 0 or new_x >= n_row or new_y < 0 or new_y >= n_col:
                    continue
                # if a shortest path to the adjacent cell is already found, skip it
                if self.visited[new_x][new_y]:
                    continue
                # if obstacle_avoidance flag is enabled and there is an obstacle at the adjacent cell, skip it
                if obstacle_avoidance_flag and self.grid.cells[new_x][new_y].state == State.OBSTACLE:
                    continue
                new_dist = dist + direction.DIR_COST
                # if obstacle_avoidance flag is disabled and there is an obstacle at the adjacent cell, add extra cost
                if not obstacle_avoidance_flag and self.grid.cells[new_x][new_y].state == State.OBSTACLE:
                    new_dist += obstacle_extra_cost
                # if the path going through the current cell is not smaller than all the possible paths found, skip it
                if new_dist >= self.dist_to_target[new_x][new_y]:
                    continue
                self.dist_to_target[new_x][new_y] = new_dist
                heap.put((new_dist, new_x, new_y))

    def find_best_adjacent_cells(self):
        """
        Finds the best adjacent cells to follow to reach the target in the shortest time for all cells
        :return: None
        """
        pygame_conf = PygameConfiguration.instance()
        n_row, n_col = pygame_conf.N_ROW, pygame_conf.N_COL
        self.all_best_paths = []
        for x in range(n_row):
            row_best_paths = []
            for y in range(n_col):
                best_paths = []
                if self.visited[x][y]:
                    for direction in self.DIRECTIONS:
                        new_x = x + direction.DIR_X
                        new_y = y + direction.DIR_Y
                        # check out of boundary case
                        if new_x < 0 or new_x >= n_row or new_y < 0 or new_y >= n_col:
                            continue
                        # if there is no path from the adjacent cell to the target cell, do not consider it
                        if not self.visited[new_x][new_y]:
                            continue
                        path_dist = self.dist_to_target[new_x][new_y] + direction.DIR_COST
                        new_path = Path(path_dist, direction)
                        best_paths.append(new_path)
                    # sort the directions to go (the adjacents to visit) based on the distance to the target cell
                    best_paths.sort(key=lambda x: x.PATH_DIST)
                row_best_paths.append(best_paths)
            self.all_best_paths.append(row_best_paths)
