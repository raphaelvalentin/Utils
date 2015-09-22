# nports
import numpy as np
from numpy import transpose, array
from numpy.linalg import inv
from math import sqrt

__all__ = ['stoz', 'stoy', 'ztoy', 'ytoz']

def stoz(*s, **kwargs):
    Z0 = kwargs.get('Z0', 50.)
    n = int(sqrt(len(s)))
    if n*n != len(s):
        raise Exception('not correct number of arguments')
    if n==1:
        s11 = array(s)
        z11 = Z0*(1.0+s11)/(1.0-s11)
	return z11
    elif n==2:
        s11, s12, s21, s22 = array(s)
        d = (1.0-s11)*(1.0-s22)-s12*s21
        z11 = ((1.0+s11)*(1.0-s22)+s12*s21) / d * Z0
        z12 = 2.0*s12 / d * Z0
        z21 = 2.0*s21 / d * Z0
        z22 = ((1.0-s11)*(1.0+s22)+s12*s21) / d * Z0
        return (z11, z12, z21, z22)
    else:
        E = np.identity(n)
        if hasattr(s[0], '__iter__'):
            m = len(s[0])
            s = np.transpose(s)
            s = np.reshape(s, (m,n,n))
            z = np.empty((m,n,n))
            for i, S in enumerate(s):
                z[i] = inv(E-S).dot(E+S)*Z0
            z = np.reshape(z, (m,n*n))
            return transpose(z)
        else:
            S = np.reshape(s, (n,n))
            Z = inv(E-S).dot(E+S)*Z0
            return np.reshape(Z, n*n)



def stoy(*s, **kwargs):
    Z0 = kwargs.get('Z0', 50.)
    n = int(sqrt(len(s)))
    if n*n != len(s):
        raise Exception('not correct number of arguments')
    if n==1:
        s11 = array(s)
        y11 = (1.0-s11)/(1.0+s11)/Z0
	return y11
    elif n==2:
        s11, s12, s21, s22 = array(s)
        d = (1.0+s11)*(1.0+s22)-s12*s21
        y11 = ((1.0-s11)*(1.0+s22)+s12*s21) / d / Z0
        y12 = -2.0*s12 / d / Z0
        y21 = -2.0*s21 / d / Z0
        y22 = ((1.0+s11)*(1.0-s22)+s12*s21) / d / Z0
        return (y11, y12, y21, y22)
    else:
        E = np.identity(n)
        if hasattr(s[0], '__iter__'):
            m = len(s[0])
            s = np.transpose(s)
            s = np.reshape(s, (m,n,n))
            y = np.empty((m,n,n))
            for i, S in enumerate(s):
                y[i] = inv(E+S).dot(E-S)*(1./Z0)
            y = np.reshape(y, (m,n*n))
            return transpose(y)
        else:
            S = np.reshape(s, (n,n))
            Y = inv(E+S).dot(E-S)*(1./Z0)
            return np.reshape(Y, n*n)



def ztoy(*z, **kwargs):
    n = int(sqrt(len(z)))
    if n*n != len(z):
        raise Exception('not correct number of arguments')
    if n==1:
        z11 = array(z)
        y11 = 1.0/z11
	return y11
    elif n==2:
        z11, z12, z21, z22 = array(z)
        det = z11*z22 - z12*z21
        y11 = z22/det
        y12 = -z12/det
        y21 = -z21/det
        y22 = z11/det
        return y11, y12, y21, y22
    else:
        if hasattr(z[0], '__iter__'):
            m = len(z[0])
            z = np.transpose(z)
            z = np.reshape(z, (m,n,n))
            y = np.empty((m,n,n))
            for i, Z in enumerate(z):
                y[i] = inv(Z)
            y = np.reshape(y, (m,n*n))
            return transpose(y)
        else:
            Z = np.reshape(z, (n,n))
            Y = inv(Z)
            return np.reshape(Y, n*n)


def ytoz(*y, **kwargs):
    n = int(sqrt(len(y)))
    if n*n != len(y):
        raise Exception('not correct number of arguments')
    if n==1:
        y11 = array(y)
        z11 = 1.0/y11
	return z11
    elif n==2:
        y11, y12, y21, y22 = array(y)
        det = y11*y22 - y12*y21
        z11 = y22/det
        z12 = -y12/det
        z21 = -y21/det
        z22 = y11/det
        return z11, z12, z21, z22
    else:
        if hasattr(y[0], '__iter__'):
            m = len(y[0])
            y = np.transpose(y)
            y = np.reshape(y, (m,n,n))
            z = np.empty((m,n,n))
            for i, Y in enumerate(y):
                z[i] = inv(Y)
            z = np.reshape(z, (m,n*n))
            return transpose(z)
        else:
            Y = np.reshape(y, (n,n))
            Z = inv(Y)
            return np.reshape(Z, n*n)



