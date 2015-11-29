
def interp1d(x, y, kind='linear'):
    def nearest(x0):
        distance = [((xi-x0)*(xi-x0), indx) for indx, xi in enumerate(x)]
	i0 = min(distance)[1]
	return y[i0]
    def linear(x0):
        distance = [((xi-x0)*(xi-x0), indx) for indx, xi in enumerate(x)]
	distance.sort()
        i0 = distance[0][1]; i1 = distance[1][1]
        slope = (y[i1]-y[i0]) / (x[i1]-x[i0])
        return slope*x0 + y[i0] - slope*x[i0]
    def cubic(x0):
        distance = [((xi-x0)*(xi-x0), indx) for indx, xi in enumerate(x)]
	distance.sort()
	i0, i1, i2 = distance[0][1], distance[1][1], distance[2][1]
        [x1, x2, x3] = [x[i0], x[i1], x[i2]]
        [y1, y2, y3] = [y[i0], y[i1], y[i2]]
        det = x1**2*x2 - x1**2*x3 - x1*x2**2 + x1*x3**2 + x2**2*x3 - x2*x3**2
        k1 = (y1*(x2 - x3) - y2*(x1 - x3) + y3*(x1 - x2))                    / det
        k2 = (-y1*(x2**2 - x3**2) + y2*(x1**2 - x3**2) - y3*(x1**2 - x2**2)) / det
        k3 = (x1*x2*y3*(x1 - x2) - x1*x3*y2*(x1 - x3) + x2*x3*y1*(x2 - x3))  / det
        return k1*x0**2 + k2*x0 + k3
    if kind=='nearest':
        return nearest
    elif kind=='linear':
        return linear
    elif kind=='cubic':
        return cubic


try:
    from fast import _nearest1, _nearest2, _nearest3
    def interp1d(x, y, kind='linear'):
        x = array(x, dtype=float)
        y = array(y, dtype=float)
        def nearest(x0):
            i0 = _nearest1(x, x0)
	    return y[i0]
        def linear(x0):
            i0, i1 = _nearest2(x, x0)
            slope = (y[i1]-y[i0]) / (x[i1]-x[i0])
            return slope*x0 + y[i0] - slope*x[i0]
        def cubic(x0):
	    i0, i1, i2 = _nearest3(x, x0)
            [x1, x2, x3] = [x[i0], x[i1], x[i2]]
            [y1, y2, y3] = [y[i0], y[i1], y[i2]]
            det = x1**2*x2 - x1**2*x3 - x1*x2**2 + x1*x3**2 + x2**2*x3 - x2*x3**2
            k1 = (y1*(x2 - x3) - y2*(x1 - x3) + y3*(x1 - x2))                    / det
            k2 = (-y1*(x2**2 - x3**2) + y2*(x1**2 - x3**2) - y3*(x1**2 - x2**2)) / det
            k3 = (x1*x2*y3*(x1 - x2) - x1*x3*y2*(x1 - x3) + x2*x3*y1*(x2 - x3))  / det
            return k1*x0**2 + k2*x0 + k3
        if kind=='nearest':
            return nearest
        elif kind=='linear':
           return linear
        elif kind=='cubic':
            return cubic
except ImportError:
    print 'Warning: use slow version of interp1d'


if __name__=='__main__':
    from function import linspace
    from libarray import *
    x = linspace(1,5, 20)
    y = sin(x)
    x0 = 2.5
    print interp1d(x, y, 'linear')(x0)
    print sin(x0)
