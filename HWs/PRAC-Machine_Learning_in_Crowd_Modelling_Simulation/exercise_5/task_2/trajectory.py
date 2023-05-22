import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


class Trajectory:
    """
    Class for Trajectory tasks
    Attributes:
        A:  The matrix to transform
    """

    def __init__(self, A):
        """
        Initializer of the class Trajectory
        A:  The matrix to transform
        """
        self.A = A

    @staticmethod
    def solve_euler(f_ode, y0, time):
        """
        Solves the given ODE system in f_ode using forward Euler.
        :param f_ode: the right hand side of the ordinary differential equation d/dt x = f_ode(x(t)).
        :param y0: the initial condition to start the solution at.
        :param time: np.array of time values (equally spaced), where the solution must be obtained.
        :returns: (solution[time,values], time) tuple.
        """
        yt = np.zeros((len(time), len(y0)))
        yt[0, :] = y0
        step_size = time[1]-time[0]
        for k in range(1, len(time)):
            yt[k, :] = yt[k-1, :] + step_size * f_ode(yt[k-1, :])
        return yt

    def plot_phase_portrait(self, X, Y):
        """
        Plots a linear vector field in a streamplot, defined with X and Y coordinates and the matrix A.
        """
        UV = self.A @ np.row_stack([X.ravel(), Y.ravel()])
        U = UV[0,:].reshape(X.shape)
        V = UV[1,:].reshape(X.shape)

        fig = plt.figure(figsize=(25, 25))
        gs = gridspec.GridSpec(nrows=3, ncols=2, height_ratios=[1, 1, 2])

        #  Varying density along a streamline
        ax0 = fig.add_subplot(gs[0, 0])
        ax0.streamplot(X, Y, U, V, density=[0.5, 1])
        ax0.set_title('Streamplot for linear vector field A*x');
        ax0.set_aspect(1)
        return ax0

    def plot_trajectory(self):
        """
        Plots trajectories for an inital point
        """
        w = 11
        Y, X = np.mgrid[-w:w:100j, -w:w:100j]

        y0 = np.array([10,10])
        time = np.linspace(0, 100, 1000)
        yt = self.solve_euler(lambda y: self.A @ y, y0, time)

        ax0 = self.plot_phase_portrait(X, Y)
        ax0.plot(yt[:, 0], yt[:, 1], c='red')
        ax0.set_aspect(1)
