import numpy as np


def Brownian(volatility, steps, num, p_start):
    mu = 0.385
    T = 1
    dt = T / steps
    S0 = p_start
    sigma = volatility

    random_component = np.random.normal(0, np.sqrt(dt), size=(num, steps)).T
    St = np.exp((mu - sigma**2 / 2) * dt + sigma * random_component)

    St = np.vstack([np.ones(num), St])
    St = S0 * St.cumprod(axis=0)

    return St.T