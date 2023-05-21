import numpy as np


def lorenz(x, y, z, s=10, r=28, b=2.667):
    """
    Given:
       x, y, z: a point of interest in three dimensional space
       s, r, b: parameters defining the lorenz attractor
    Returns:
       x_dot, y_dot, z_dot: values of the lorenz attractor's partial
           derivatives at the point x, y, z
    """
    x_dot = s*(y - x)
    y_dot = r*x - y - x*z
    z_dot = x*y - b*z
    return x_dot, y_dot, z_dot


def euc(p1, p2):
    """
    Given:
       p1: first point of the given pair
       p2: second point of the given pair
    Returns:
       euc_dist: euclidean distance between given 2 points
    """
    euc_dist = np.sqrt(np.sum((p1-p2)**2))
    return euc_dist


def get_dist(all_points, all_points_hat, dt):
    """
    Given:
       all_points: all points of the first trajectory
       all_points_hat: all points of the second trajectory
       dt: change in time between two points of the same trajectory
    Returns:
       dist: array of euclidean distance between corresponding points of given two trajectories
    """
    dist = []
    ix = 0
    time_happened = None
    for p1, p2 in zip(all_points, all_points_hat):
        d = euc(p1, p2)
        if time_happened is None and d > 1:
            time_happened = ix * dt
        dist.append(d)
        ix += 1

    dist = np.array(dist)
    max_dist = np.max(dist)

    if time_happened is not None:
        print('The exact time when the distance is larger than 1 is:', time_happened, 'seconds', sep=' ')
    else:
        print('The distance never exceeded 1.')
    print('Maximum distance between two trajectories is:', max_dist, sep=' ')

    return dist
