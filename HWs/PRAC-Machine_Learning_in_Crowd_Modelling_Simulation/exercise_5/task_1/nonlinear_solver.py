import numpy as np
import matplotlib.pyplot as plt

from solver import Solver


class NonlinearSolver(Solver):
    """
    Class for NonlinearSolver tasks
    Attributes:
        L:              The number of radial functions
        eps:            The epsilon value given in the calculation of radial functions
        file_name:      Input file storing coordinates of the points
        folder_path:    Directory of the folder where the input file is stored
        n:              The number of points in the dataset
    """

    def __init__(self, L, eps, file_name, folder_path=None):
        """
        Initializer of the class NonlinearSolver
        :param L:             The number of radial functions
        :param eps:           The epsilon value given in the calculation of radial functions
        :param file_name:     Input file storing coordinates of the points
        :param folder_path:   Directory of the folder where the input file is stored
        """
        super().__init__(file_name, folder_path)
        self.L = L
        self.eps = eps
        self.n = None

    @staticmethod
    def get_nonlinear_pred(A, coef):
        """
        Calculates y coordinates of the points
        :param A:       The radial function values of the points
        :param coef:    The matrix to transform radial functions to coordinates
        :returns:       The predicted y coordinates of the points
        """
        y_pred = np.dot(A, coef)
        return y_pred

    @staticmethod
    def plot_nonlinear_sol_data(x, y, y_pred):
        """
        Plots ground truth and predicted points
        :param x:         The x coordinates of the points
        :param y:         The y coordinates of the points
        :param y_pred:    The predicted y coordinates of the points
        """
        plt.scatter(x, y, color='b')
        plt.scatter(x, y_pred, color='r')
        plt.show()

    def plot_nonlinear_sol_func_partial(self, x, x_l, y, coef, x_left=-2.5, x_right=2.5, n_points=1000):
        """
        Plots ground truth and predicted function partially
        :param x:         The x coordinates of the points
        :param x_l:       The center points to calculate radial functions
        :param y:         The y coordinates of the points
        :param coef:      The matrix to transform radial functions to coordinates
        :param x_left:    Left boundary on the domain of function
        :param x_right:   Right boundary on the domain of function
        :param n_points:  The number of points to plot the function
        """
        plt.scatter(x, y, color='b')
        x_sample = np.linspace(x_left, x_right, n_points)
        y_sample = []
        for x_val in x_sample:
            sum = 0
            for k in range(self.L):
                x_prime = np.exp(-((x_l[k] - x_val) ** 2) / (self.eps ** 2))
                sum += x_prime * coef[k]
            y_sample.append(sum)
        y_sample = np.asarray(y_sample)
        plt.plot(x_sample, y_sample, color='r', linestyle='solid')
        plt.show()

    def plot_nonlinear_sol_func_entire(self, x, x_l, y, coef, expand=.01, n_points=1000):
        """
        Plots ground truth and predicted function
        :param x:         The x coordinates of the points
        :param x_l:       The center points to calculate radial functions
        :param y:         The y coordinates of the points
        :param coef:      The matrix to transform radial functions to coordinates
        :param expand:    Amount of expansion in left and right direction for x-axis to plot the function
        :param n_points:  The number of points to plot the function
        """
        plt.scatter(x, y, color='b')
        x_sample = np.linspace(np.min(x) - expand, np.max(x) + expand, n_points)
        y_sample = []
        for x_val in x_sample:
            sum = 0
            for k in range(self.L):
                x_prime = np.exp(-((x_l[k] - x_val) ** 2) / (self.eps ** 2))
                sum += x_prime * coef[k]
            y_sample.append(sum)
        y_sample = np.asarray(y_sample)
        plt.plot(x_sample, y_sample, color='r', linestyle='solid')
        plt.show()

    def get_basis(self, x, expand=.1):
        """
        Calculates radial function values of the given points
        :param x:         The coordinates of the points
        :param expand:    Amount of expansion in left and right direction for x-axis to get center points
        :returns:         The radial function values and chosen center points
        """
        x_l = np.linspace(np.min(x) - expand, np.max(x) + expand, self.L)
        x_basis = np.empty([self.n, self.L], dtype=np.float64)
        for i in range(self.n):
            for k in range(self.L):
                x_basis[i, k] = np.exp(-((x_l[k] - x[i]) ** 2) / (self.eps ** 2))
        return x_basis, x_l

    def solve_nonlinear(self):
        """
        Solve the prediction problem using the nonlinear method
        """
        x, y = self.read_data()
        x_basis, x_l = self.get_basis(x)
        A = np.vstack([x_basis.T, np.zeros(self.n)]).T
        # A = np.copy(x_basis)
        coef = np.linalg.lstsq(A, y, rcond=None)[0]
        y_pred = self.get_nonlinear_pred(A, coef)
        loss = self.get_loss(y, y_pred)
        print("loss:", loss)
        self.plot_nonlinear_sol_data(x, y, y_pred)
        print()
        self.plot_nonlinear_sol_func_partial(x, x_l, y, coef)
        print()
        self.plot_nonlinear_sol_func_entire(x, x_l, y, coef)
