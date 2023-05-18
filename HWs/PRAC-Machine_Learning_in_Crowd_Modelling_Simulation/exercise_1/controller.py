from queue import PriorityQueue

from grid import Grid
from path_calculator import PathCalculator
from pygame_conf import PygameConfiguration
from state import State


class Controller:
    """
    Object representing the grid controller — the one that makes the moves on the grid

    Attributes:
        grid:               Grid to be controlled
        heap:               Priority queue that stores moves according to their priority
    """

    def __init__(self, grid: Grid, path_calculator: PathCalculator):
        self.grid = grid
        self.path_calculator = path_calculator
        self.heap = PriorityQueue()
        self.occupied_positions = set()

        for pedestrian in grid.pedestrians:
            pedestrian_id = pedestrian.ID
            # add pedestrian coordinates (position) to the occupied positions list
            self.occupied_positions.add(pedestrian.position)
            # put the id and the position of pedestrian to the heap with initial timestamp - it will be used
            # while computing move priority
            self.heap.put((.0, pedestrian_id, pedestrian.position))

    def make_move(self, current_timestamp: float):
        """
        Makes the most prior move
        :return: None
        """
        pygame_conf = PygameConfiguration.instance()
        delta_timestamp = pygame_conf.DISPLAY_DELTA_TIMESTAMP
        cells = self.grid.cells

        while not self.heap.empty():
            # fetch the most prior move
            event_time, pedestrian_id, next_pedestrian_position = self.heap.queue[0]

            # the next event occurs after the current timestamp t
            if event_time > current_timestamp:
                break

            self.heap.get()
            pedestrian = self.grid.pedestrians[pedestrian_id]
            pedestrian_x, pedestrian_y = pedestrian.position

            # if the pedestrian is planning to move a different position instead of waiting in his cell
            if pedestrian.position is not next_pedestrian_position:
                # set the current cell as visited, remove it from occupied positions and move the pedestrian
                cells[pedestrian_x][pedestrian_y].set_state(State.VISITED, pedestrian.TRACK_COLOR)
                self.occupied_positions.remove(pedestrian.position)
                pedestrian.position = next_pedestrian_position
                pedestrian_x, pedestrian_y = pedestrian.position
                # check if the pedestrian reached the target or not
                if cells[pedestrian_x][pedestrian_y].state is State.TARGET:
                    pedestrian.has_arrived = True
                    self.grid.TARGET_CELL.pedestrians_on_target.append(pedestrian.ID + 1)
                    print('Pedestrian {} has arrived to the target at {}.'.format(pedestrian.ID + 1, event_time))
                    continue
                else:
                    cells[pedestrian_x][pedestrian_y].set_state(State.PEDESTRIAN)

            pedestrian_found_adjacent_cell = False
            best_paths = self.path_calculator.all_best_paths[pedestrian_x][pedestrian_y]

            # decide the next cell to visit for the pedestrian considering currently occupied cells and obstacles
            for path in best_paths:
                direction = path.DIRECTION
                pedestrian_new_x = pedestrian_x + direction.DIR_X
                pedestrian_new_y = pedestrian_y + direction.DIR_Y
                pedestrian_new_position = (pedestrian_new_x, pedestrian_new_y)
                # if the best cell to visit is an obstacle, then the pedestrian gets stuck
                if cells[pedestrian_new_x][pedestrian_new_y].state is State.OBSTACLE:
                    pedestrian.has_stuck = True
                    print('Pedestrian {} has stuck at the cell({},{}) at timestamp {}.'.format(pedestrian.ID + 1,
                                                                                               pedestrian_x,
                                                                                               pedestrian_y,
                                                                                               event_time))
                    break
                # if the cell that currently is checked is not occupied by another pedestrian, he can visit the cell
                elif pedestrian_new_position not in self.occupied_positions:
                    # making the absorbing target cell occupied would lead pedestrians arriving at different times
                    if cells[pedestrian_new_x][pedestrian_new_y].state is not State.TARGET:
                        self.occupied_positions.add(pedestrian_new_position)
                    new_event_time = event_time + direction.DIR_COST / pedestrian.SPEED
                    self.heap.put((new_event_time, pedestrian_id, pedestrian_new_position))
                    pedestrian_found_adjacent_cell = True
                    break

            # if the pedestrian is not stuck, and he has no cell to visit, let him wait for delta_timestamp
            if not pedestrian.has_stuck and not pedestrian_found_adjacent_cell:
                self.heap.put((current_timestamp + delta_timestamp, pedestrian_id, pedestrian.position))
