import numpy as np
import matplotlib.pyplot as plt


def Brownian(volatility,steps):

    # drift coefficient
    mu = 0.1
    # number of steps
    n = steps
    # time in years
    T = 1
    # number of sims
    M = 100
    # initial stock price
    S0 = 100
    # volatility
    sigma = volatility

    # calc each time step
    dt = T/n

    # simulation using numpy arrays
    St = np.exp(
        (mu - sigma**2/2) * dt
        +sigma * np.random.normal(0,np.sqrt(dt),size=(M,n)).T
    )

    # include array of 1's
    St = np.vstack([np.ones(M), St])

    # multiply through by S0 and return the cumulative product of elements along a given simulation path(axis = 0)
    St = S0 * St.cumprod(axis=0)

    return St.T