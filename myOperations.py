def absoluteSquare(x,y):
    ret = 0
    if x >= 0:
        ret = x**y
    else:
        ret = -((-x)**y)
    return ret