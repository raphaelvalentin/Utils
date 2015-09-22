from libarray import atan2, log10, array
from math import pi

dB = lambda x: 20.*log10(abs(x))
Angle = lambda x: atan2(x.imag, x.real)/pi*180.

__all__ = ['pi', 'dB', 'Angle', 'stoy', 'ytos', 'stoz', 'ytoz', 'ztoy']

def stoy(s11, s12, s21, s22, Z0=50.):
    d = (1.0+s11)*(1.0+s22)-s12*s21
    y11 = ((1.0-s11)*(1.0+s22)+s12*s21) / d / Z0
    y12 = -2.0*s12 / d / Z0
    y21 = -2.0*s21 / d / Z0
    y22 = ((1.0+s11)*(1.0-s22)+s12*s21) / d / Z0
    return (y11, y12, y21, y22)

def ytos(y11, y12, y21, y22, Z0=50.):
    y11, y12, y21, y22 = y11*Z0, y12*Z0, y21*Z0, y22*Z0
    d = (1.0+y11)*(1.0+y22)-y12*y21
    s11 =  ((1.0-y11)*(1.0+y22)+y12*y21) / d
    s12 = -2.0*y12 / d
    s21 = -2.0*y21 / d
    s22 =((1.0+y11)*(1.0-y22)+y12*y21) / d
    return (s11, s12, s21, s22)

def stoz(s11, s12, s21, s22, Z0=50.):
    d = (1.0-s11)*(1.0-s22)-s12*s21
    z11 = ((1.0+s11)*(1.0-s22)+s12*s21) / d * Z0
    z12 = 2.0*s12 / d * Z0
    z21 = 2.0*s21 / d * Z0
    z22 = ((1.0-s11)*(1.0+s22)+s12*s21) / d * Z0
    return (z11, z12, z21, z22)

def ytoz(y11, y12, y21, y22):
    det = y11*y22 - y12*y21
    z11 = y22/det
    z12 = -y12/det
    z21 = -y21/det
    z22 = y11/det
    return array([z11, z12, z21, z22])

def ztoy(z11, z12, z21, z22):
    det = z11*z22 - z12*z21
    y11 = z22/det
    y12 = -z12/det
    y21 = -z21/det
    y22 = z11/det
    return array([y11, y12, y21, y22])


