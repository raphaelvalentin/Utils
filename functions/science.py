from math import *
import numpy as np

__all__ = ['nan', 'inf', 'rms', 'mae', 'average', 'sign', 'linspace', 'logspace', 'derivative', 'flatten', 'integ', 'polyval']


rms = lambda X : sqrt(sum(x*x for x in X)/len(X)) # root mean square
mae = lambda X : sum(abs(x) for x in X)/len(X) # mean absolute error
average = lambda X: sum(X)/len(X)

nan = float('nan')
inf = float('inf')

def sign(x):
    if x>=0: return 1
    return -1

def linspace(start, stop, num=0, step=None):
    start = float(start)
    stop = float(stop)
    if step == None:
        if num == 1:
	     step = stop-start
	else:
    	     step = (stop-start)/(float(num)-1.0)
    else:
        step = float(step)
	if step == 0.0:
	    num = 0.0
	else:
	    num = (stop-start)/step+1.0
    return np.arange(num)*step + start



def logspace(start, stop, num=1, step=None, prec=10):
    if start<=0.0 or stop<=0.0:
        return []
    if step == None:
        return 10**(linspace(log10(start), log10(stop), num=num))
    else:
        if step<=0:
	    return []
        return 10**(linspace(log10(start), log10(stop), step=log10(step)))


def derivative(x, y, n=1):
    def __derivative__(x, y):
        xr = np.empty(len(x)-1)
        yr = np.empty(len(x)-1)
        for i in xrange(len(x)-1):
            xr[i] = (x[i]+x[i+1])*0.5
            yr[i] = (y[i]-y[i+1])/(x[i]-x[i+1])
        return (xr,yr)
    if len(x)<n+1:
        raise Exception('Warning : not enough points for applying the derivative.')
    for i in xrange(n):
        (x, y) = __derivative__(x, y)
    return (x, y)


def flatten(sequence):
    """ yield each element of an irregular list (or tuple, dict...->__instance)"""
    for el in sequence:
        if isinstance(el, list):
            for sub in flatten(el):
                yield sub
        else:
            yield el

def integ(f,X0,X1,n):
#integration numerique a partir d une fonction
    H=X1-X0
    p=H/n
    I=0.
    h=p/4.
    x0=X0
    while (x0+p)<X1:
        x1=x0+h
        x2=x1+h
        x3=x2+h
        x4=x3+h
        I+=14.*f(x0)+64.*f(x1)+24.*f(x2)+64.*f(x3)+14.*f(x4)
        x0=x4
    return I*h/45.


def polyval(p, x):
    y = 0.0
    l=len(p)
    for i, v in enumerate(p):
        y += v*x**(l-i-1)
    return y
