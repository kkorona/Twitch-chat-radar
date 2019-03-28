def squareSpread(x):
    ret = 0
    if x >= 0:
        ret = x*x
    else:
        ret = -(x*x)
    return ret