import numpy as np
from utils import lorenz
from matplotlib import pyplot as plt

# Need one more for the initial values
dt = 0.001
TIME_LIMIT = 1000

def get_trajectory(x_0=10., r=28.0, plot=False):
    """
    Given:
       x_0: initial point of the trajectory
       r: parameter rho of Lorenz system
       plot: flag to plot the trajectory
    Returns:
       x: points of trajectory for the given initial point and parameters - axis x
       y: points of trajectory for the given initial point and parameters - axis y
       z: points of trajectory for the given initial point and parameters - axis z
    """

    # Set initial values
    curr_x, curr_y, curr_z = (x_0, 10., 10.)
    x = [curr_x]
    y = [curr_y]
    z = [curr_z]
    curr_idx = 0

    # Step through "time", calculating the partial derivatives at the current point
    # and using them to estimate the next point
    while curr_idx * dt < TIME_LIMIT:
        change_x, change_y, change_z = lorenz(x=curr_x, y=curr_y, z=curr_z, r=r)
        curr_x += change_x * dt
        curr_y += change_y * dt
        curr_z += change_z * dt
        x.append(curr_x)
        y.append(curr_y)
        z.append(curr_z)
        curr_idx += 1

    # plot trajectory for the given initial point and params
    if plot:
        ax = plt.figure(figsize=(8,6)).add_subplot(projection='3d')
        ax.plot(x, y, z, lw=0.6)
        ax.set_xlabel("X Axis")
        ax.set_ylabel("Y Axis")
        ax.set_zlabel("Z Axis")
        ax.set_title("Lorenz Attractor")

    return x, y, z
