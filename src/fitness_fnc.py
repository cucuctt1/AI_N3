#sphere function
import numpy as np


def sphere(x):
    return np.sum(x**2)


# (muc 5 added)
def rastrigin(x):
    x = np.asarray(x)
    n = x.size
    return 10 * n + np.sum(x**2 - 10 * np.cos(2 * np.pi * x))


def rosenbrock(x):
    x = np.asarray(x)
    if x.size < 2:
        return 0.0
    return np.sum(100.0 * (x[1:] - x[:-1] ** 2) ** 2 + (x[:-1] - 1.0) ** 2)


def ackley(x):
    x = np.asarray(x)
    n = x.size
    if n == 0:
        return 0.0
    sum_sq = np.sum(x**2)
    sum_cos = np.sum(np.cos(2 * np.pi * x))
    term1 = -20.0 * np.exp(-0.2 * np.sqrt(sum_sq / n))
    term2 = -np.exp(sum_cos / n)
    return term1 + term2 + 20.0 + np.e


def griewank(x):
    x = np.asarray(x)
    i = np.arange(1, x.size + 1)
    sum_term = np.sum(x**2) / 4000.0
    prod_term = np.prod(np.cos(x / np.sqrt(i)))
    return sum_term - prod_term + 1.0