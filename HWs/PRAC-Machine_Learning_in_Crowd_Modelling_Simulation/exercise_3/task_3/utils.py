import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


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
    return yt, time


def plot_phase_portrait(calc, X, Y):
    """
    Plots a linear vector field in a streamplot, defined with X and Y coordinates and the method calc.
    """
    x = X.ravel()
    y = Y.ravel()
    UV = [[],[]]
    for i in range(len(x)):
        for k,l in enumerate(calc([x[i],y[i]])):
            UV[k].append(l)
    # all values of vector space is calculated and assigned to UV matrix
    UV = np.array(UV)
    print(UV)
    U = UV[0,:].reshape(X.shape)
    V = UV[1,:].reshape(X.shape)
    # from UV values are taken and assigned to U and V for plotting purpose

    fig = plt.figure(figsize=(15, 15))
    gs = gridspec.GridSpec(nrows=3, ncols=2, height_ratios=[1, 1, 2])

    #  Varying density along a streamline
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.streamplot(X, Y, U, V, density=[0.5, 1])
    ax0.set_title('Alpha = +1, Start point = (0.5,0)');
    ax0.set_aspect(1)
    return ax0

def calc(x):
    """
    takes the previous positions or initial positions and returns updated one for a spesific alpha value
    """
    alp = +1
    x1,x2 = x
    tempx1 = x1
    x1= alp*x1 - x2 -x1*(x1**2 + x2**2)
    x2= tempx1 + alp*x2 - x2*(tempx1**2 + x2**2)
    return np.array([x1,x2])
