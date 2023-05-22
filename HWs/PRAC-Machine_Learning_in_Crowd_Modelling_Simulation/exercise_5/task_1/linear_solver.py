import numpy as np
import matplotlib.pyplot as plt

from solver import Solver


class LinearSolver(Solver):
    """
    Class for LinearSolver tasks
    Attributes:
        file_name:      Input file storing coordinates of the points
        folder_path:    Directory of the folder where the input file is stored
        n:              The number of points in the dataset
    """

    def __init__(self, file_name, folder_path=None):
        """
        Initializer of the class LinearSolver
        :param file_name:     Input file storing coordinates of the points
        :param folder_path:   Directory of the folder where the input file is stored
        """
        super().__init__(file_name, folder_path)
        self.n = None

    @staticmethod
    def get_linear_pred(x, m):
        """
        Calculates y coordinates of the given points
        :param x:   The x coordinates of the points
        :param m:   The slope m used to predict y coordinates
        :returns:   The predicted y coordinates of the given points
        """
        y_pred = m * x
        return y_pred

    @staticmethod
    def plot_linear_sol(x, y, m, expand=.5, n_points=1000):
        """
        Plots the function
        :param x:         The x coordinates of the points
        :param y:         The y coordinates of the points
        :param m:         The slope m used to predict y coordinates
        :param expand:    Amount of expansion in left and right direction for x-axis to plot the function
        :param n_points:  The number of points to plot the function
        """
        plt.scatter(x, y, color='b')
        x_sample = np.linspace(np.min(x) - expand, np.max(x) + expand, n_points)
        y_sample = m * x_sample
        plt.plot(x_sample, y_sample, color='r', linestyle='solid')
        plt.show()

    def solve_linear(self):
        """
        Solve the prediction problem using the linear method
        """
        x, y = self.read_data()
        A = np.vstack([x, np.zeros(self.n)]).T
        m, c = np.linalg.lstsq(A, y, rcond=None)[0]
        print("m: {} and c: {}".format(m, c))
        y_pred = self.get_linear_pred(x, m)
        loss = self.get_loss(y, y_pred)
        print("loss:", loss)
        self.plot_linear_sol(x, y, m)
