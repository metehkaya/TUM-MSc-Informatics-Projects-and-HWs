import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


class Trajectory:
    """
    Class for Trajectory tasks
    Attributes:
        x_0:    The coordinates of initial points
        x_l:    The chosen center points
        coef:   The matrix to transform radial functions to coordinates
        L:      The number of radial functions
        eps:    The epsilon value given in the calculation of radial functions
    """

    def __init__(self, x_0, x_l, coef, L, eps):
        """
        Initializer of the class Trajectory
        x_0:    The coordinates of initial points
        x_l:    The chosen center points
        coef:   The matrix to transform radial functions to coordinates
        L:      The number of radial functions
        eps:    The epsilon value given in the calculation of radial functions
        """
        self.x_0 = x_0
        self.x_l = x_l
        self.coef = coef
        self.L = L
        self.eps = eps

    def get_euc_dist(self, y0, y1):
        """
        Calculates the euclidean distance between given points
        :param y0:  The first point of the pair to calculate euclidean distance
        :param y1:  The second point of the pair to calculate euclidean distance
        :returns:   The euclidean distance between given points
        """
        diff = y0 - y1
        sum = np.sum(diff ** 2)
        euc_dist = np.sqrt(sum)
        return euc_dist

    def solve_euler(self, y0, time):
        """
        Solves the given ODE system using radial functions.
        :param y0:      the initial condition to start the solution at.
        :param time:    np.array of time values (equally spaced), where the solution must be obtained.
        :returns:       All points in the trajectory by order and pair of close points
        """
        close_points = []
        yt = np.zeros((len(time), len(y0)))
        yt[0, :] = y0
        step_size = time[1] - time[0]
        for i in range(1, len(time)):
            x = yt[i - 1, :]
            x_basis = np.empty([self.L * 2], dtype=np.float64)
            x_basis = self.x_l - x[:, None].T
            x_basis = x_basis ** 2
            x_basis = -x_basis / (self.eps ** 2)
            x_basis = np.exp(x_basis)
            x_basis = np.ravel(x_basis)
            pred_v = np.dot(x_basis, self.coef[:-1])
            yt[i, :] = yt[i - 1, :] + step_size * pred_v
            euc_dist = self.get_euc_dist(yt[i - 1, :], yt[i, :])
            if euc_dist < 1e-7:
                close_points.append((yt[i - 1, :], yt[i, :], euc_dist))
        return yt, close_points

    @staticmethod
    def plot_phase_portrait():
        """
        Plots phase portrait
        :returns: Subplot to plot trajectory
        """
        fig = plt.figure(figsize=(25, 25))
        gs = gridspec.GridSpec(nrows=3, ncols=2, height_ratios=[1, 1, 2])
        ax0 = fig.add_subplot(gs[0, 0])
        ax0.set_aspect(1)
        return ax0

    def plot_trajectory(self, periodic_print=True):
        """
        Plots trajectories for the given inital points
        :param periodic_print:  A debugging boolean value to see if plotting works fast
        :returns:               All pair of close points
        """
        n = self.x_0.shape[0]
        w = 4.5
        Y, X = np.mgrid[-w:w:100j, -w:w:100j]

        ax0 = self.plot_phase_portrait()

        period = 100
        yts = []
        close_points = []
        for i in range(n):
            if periodic_print and i % period == 0:
                print("Plotting for initial point:", i)
            y0 = self.x_0[i, :]
            time = np.linspace(0, 100, 1000)
            yt, new_close_points = self.solve_euler(y0, time)
            close_points.extend(new_close_points)
            yts.append(yt)
            ax0.plot(yt[:, 0], yt[:, 1], c='red')

        ax0.set_aspect(1)

        return close_points
