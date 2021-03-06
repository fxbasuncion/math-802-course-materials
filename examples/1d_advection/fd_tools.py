"""
Tools for creating finite difference stencils.
"""

import numpy as np

def fd_coeff(k, x_bar, x):
    """
    Computes the coefficients fo the kth order derivative using Fornberg's
    algorithm.

      B. Fornberg, "Calculation of weights in finite difference formulas",
      SIAM Review 40 (1998), pp. 685-691.

    Fornberg's original algorithm computes all derivative weights up to k,
    this implementation (like LeVeque's) only returns the kth derivative
    weights.

    Parameters
    ----------
    k : int
        The order of derivative to approximate.
    x_bar : float
        The location of derivative approximation.
    x : array_like :
        The sample locations.

    Returns
    -------
        An array of finite difference coefficients.
    """

    import numpy as np

    # translate variable names to Fornberg's language
    m = k
    z = x_bar

    n = len(x) - 1    # "one less than the total number of grid points"

    # create the coefficient matrix
    c = np.zeros((n+1,m+1))

    c1 = 1
    c4 = x[0] - z
    c[0,0] = 1
    for i in range(1,n+1):
        mn = min(i,m)
        c2 = 1
        c5 = c4
        c4 = x[i] - z
        for j in range(i):
            c3 = x[i] - x[j]
            c2 = c2*c3
            if j == i-1:
                for k in range(mn,0,-1):
                    c[i,k] = c1*(k*c[i-1,k-1] - c5*c[i-1,k])/c2
                c[i,0] = -c1*c5*c[i-1,0]/c2
            for k in range(mn,0,-1):
                c[j,k] = (c4*c[j,k] - k*c[j,k-1])/c3
            c[j,0] = c4*c[j,0]/c3
        c1 = c2

    return c[:,-1]
