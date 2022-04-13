def rsquared(x, y):
    """ Return R^2 where x and y are array-like."""
    import scipy.stats
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
    return r_value**2

