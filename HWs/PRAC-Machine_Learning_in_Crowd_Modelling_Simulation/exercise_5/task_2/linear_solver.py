import os
import numpy as np


class LinearSolver:
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
        self.file_name_x0 = file_name_x0
        self.file_name_x1 = file_name_x1
        self.folder_path = folder_path
        self.n = None

    def read_data(self, file_name):
        """
        Reads coordinates of the points
        :param file_name:    Input file storing coordinates of the points
        :returns:            Coordinates of the points given in the file
        """
        data = []
        if self.folder_path is None:
            file_path = file_name
        else:
            file_path = os.path.join(self.folder_path, file_name)
        with open(file_path) as f:
            lines = f.readlines()
            for line in lines:
                row_data = []
                x, y = map(float, line.split())
                row_data.append(x)
                row_data.append(y)
                row_data = np.asarray(row_data)
                data.append(row_data)
        data = np.asarray(data)
        self.n = data.shape[0]
        return data

    def get_data(self, delta_t):
        """
        Retrieves coordinates of the points and velocity
        :param delta_t:     Time difference between steps of the trajectory
        :returns:           Coordinates of the points given in the file and velocity
        """
        x_0 = self.read_data(self.file_name_x0)
        x_1 = self.read_data(self.file_name_x1)
        v = (x_1 - x_0) / delta_t
        return x_0, x_1, v

    def get_loss(self, x_1, pred_x_1):
        """
        Retrieves loss
        :param x_1:         Ground truth for coordinates of the points
        :param pred_x_1:    Predicted coordinates of the points
        :returns:           Loss value
        """
        sum = 0
        for i in range(self.n):
            diff = np.sum((x_1[i] - pred_x_1[i]) ** 2)
            sum += np.sqrt(diff)
        loss = sum / self.n
        return loss

    @staticmethod
    def get_pred(x_0, A, delta_t):
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

    def solve_linear(self, delta_t=0.1):
        """
        Solve the trajectory prediction problem using the linear method
        :param delta_t:     Time difference between steps of the trajectory
        """
        x_0, x_1, v = self.get_data(delta_t)
        X = np.vstack([x_0.T, np.zeros(x_0.shape[0])]).T
        A = np.linalg.lstsq(X, v, rcond=None)[0]
        A = A[:-1]
        pred_x_1 = self.get_pred(x_0, A, delta_t)
        loss = self.get_loss(x_1, pred_x_1)
        print("loss:", loss)
        return A
