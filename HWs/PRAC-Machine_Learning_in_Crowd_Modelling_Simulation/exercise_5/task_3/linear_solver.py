import numpy as np

from solver import Solver


class LinearSolver(Solver):
    """
    Class for LinearSolver tasks
    Attributes:
        file_name_x0:   Input file storing coordinates of the first points of trajectories
        file_name_x1:   Input file storing coordinates of the second points of trajectories
        folder_path:    Directory of the folder where input files are stored
        n:              The number of points in the dataset
    """

    def __init__(self, file_name_x0, file_name_x1, folder_path=None):
        """
        Initializer of the class LinearSolver
        :param file_name_x0:    Input file storing coordinates of the first points of trajectories
        :param file_name_x1:    Input file storing coordinates of the second points of trajectories
        :param folder_path:     Directory of the folder where input files are stored
        """
        super().__init__(file_name_x0, file_name_x1, folder_path)

    @staticmethod
    def get_linear_pred(x_0, A, delta_t):
        """
        Calculates coordinates of the next points in the trajectory
        :param x_0:         The coordinates of the initial points
        :param A:           The transition matrix used to calculate coordinates of the next point
        :param delta_t:     Time difference between steps of the trajectory
        :returns:           The coordinates of the next point
        """
        pred_v = np.dot(x_0, A)
        displacement = pred_v * delta_t
        pred_x_1 = x_0 + displacement
        return pred_x_1

    def solve_linear(self, delta_t = 0.1):
        """
        Solve the trajectory prediction problem using the linear method
        :param delta_t:     Time difference between steps of the trajectory
        """
        x_0, x_1, v = self.get_data(delta_t)
        X = np.vstack([x_0.T, np.zeros(x_0.shape[0])]).T
        A = np.linalg.lstsq(X, v, rcond=None)[0]
        A = A[:-1]
        pred_x_1 = self.get_linear_pred(x_0, A, delta_t)
        loss = self.get_loss(x_1, pred_x_1)
        print("loss:", loss)
