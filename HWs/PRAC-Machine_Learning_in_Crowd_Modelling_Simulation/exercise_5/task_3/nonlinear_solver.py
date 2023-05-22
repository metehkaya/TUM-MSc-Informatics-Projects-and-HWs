import numpy as np

from solver import Solver


class NonlinearSolver(Solver):
    """
    Class for NonlinearSolver tasks
    Attributes:
        L:              The number of radial functions
        eps:            The epsilon value given in the calculation of radial functions
        file_name_x0:   Input file storing coordinates of the first points of trajectories
        file_name_x1:   Input file storing coordinates of the second points of trajectories
        folder_path:    Directory of the folder where input files are stored
        n:              The number of points in the dataset
    """

    def __init__(self, L, eps, file_name_x0, file_name_x1, folder_path=None):
        """
        Initializer of the class NonlinearSolver
        L:              The number of radial functions
        eps:            The epsilon value given in the calculation of radial functions
        file_name_x0:   Input file storing coordinates of the first points of trajectories
        file_name_x1:   Input file storing coordinates of the second points of trajectories
        folder_path:    Directory of the folder where input files are stored
        """
        super().__init__(file_name_x0, file_name_x1, folder_path)
        self.L = L
        self.eps = eps

    @staticmethod
    def get_nonlinear_pred(x_0, A, coef, delta_t):
        """
        Calculates coordinates of the next points in the trajectory
        :param x_0:         The coordinates of the initial points
        :param A:           The radial function values of the points
        :param coef:        The matrix to transform radial functions to coordinates
        :param delta_t:     Time difference between steps of the trajectory
        :returns:           The coordinates of the next point
        """
        pred_v = np.dot(A, coef)
        displacement = pred_v * delta_t
        pred_x_1 = x_0 + displacement
        return pred_x_1

    def get_basis(self, x):
        """
        Calculates radial function values of the given points
        :param x:     The coordinates of the points
        :returns:     The radial function values and chosen center points
        """
        x_l = 9*np.random.rand(self.L,2)-4.5
        x_basis = np.empty([self.n, self.L*2], dtype=np.float64)
        for i in range(self.n):
            x_i = x[i,:]
            x_i_basis = x_l - x_i[:,None].T
            x_i_basis = x_i_basis**2
            x_i_basis = -x_i_basis / (self.eps**2)
            x_i_basis = np.exp(x_i_basis)
            x_basis[i,:] = np.ravel(x_i_basis)
        return x_basis, x_l

    def solve_nonlinear(self, delta_t = 0.1):
        """
        Solve the trajectory prediction problem using the nonlinear method
        :param delta_t:   Time difference between steps of the trajectory
        :returns:         The initial points, center points and the transition matrix
        """
        x_0, x_1, v = self.get_data(delta_t)
        x_basis, x_l = self.get_basis(x_0)
        A = np.vstack([x_basis.T, np.zeros(x_0.shape[0])]).T
        coef = np.linalg.lstsq(A, v, rcond=None)[0]
        pred_x_1 = self.get_nonlinear_pred(x_0, A, coef, delta_t)
        loss = self.get_loss(x_1, pred_x_1)
        print("L: {}, eps: {} => loss: {}".format(self.L, self.eps, loss))
        return x_0, x_l, coef
