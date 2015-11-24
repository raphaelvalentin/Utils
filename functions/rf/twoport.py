from libarray import atan2, log10, array
from numpy import array
from math import pi, sqrt

dB = lambda x: 20.*log10(abs(x))
Angle = lambda x: atan2(x.imag, x.real)/pi*180.

__all__ = ['pi', 'dB', 'Angle', 'stoy', 'ytos', 'stoz', 'ytoz', 'ztoy', 'ztos', 'ztoa', 'atos']

def stoy(s11, s12, s21, s22, Z0=50.):
    d = (1.0+s11)*(1.0+s22)-s12*s21
    y11 = ((1.0-s11)*(1.0+s22)+s12*s21) / d / Z0
    y12 = -2.0*s12 / d / Z0
    y21 = -2.0*s21 / d / Z0
    y22 = ((1.0+s11)*(1.0-s22)+s12*s21) / d / Z0
    return array([y11, y12, y21, y22])

def ytos(y11, y12, y21, y22, Z0=50.):
    y11, y12, y21, y22 = y11*Z0, y12*Z0, y21*Z0, y22*Z0
    d = (1.0+y11)*(1.0+y22)-y12*y21
    s11 =  ((1.0-y11)*(1.0+y22)+y12*y21) / d
    s12 = -2.0*y12 / d
    s21 = -2.0*y21 / d
    s22 =((1.0+y11)*(1.0-y22)+y12*y21) / d
    return array([s11, s12, s21, s22])

def stoz(s11, s12, s21, s22, Z0=50.):
    d = (1.0-s11)*(1.0-s22)-s12*s21
    z11 = ((1.0+s11)*(1.0-s22)+s12*s21) / d * Z0
    z12 = 2.0*s12 / d * Z0
    z21 = 2.0*s21 / d * Z0
    z22 = ((1.0-s11)*(1.0+s22)+s12*s21) / d * Z0
    return array([z11, z12, z21, z22])

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

def ztos(z11, z12, z21, z22):
    z11, z12, z21, z22 = z11/Z0, z12/Z0, z21/Z0, z22/Z0
    d = (z11+1.0)*(z22+1.0)-z12*z21
    s11 = ((z11-1.0)*(z22+1.0)-z12*z21)/d
    s12 = 2*z12/d
    s21 = 2*z21/d
    s22 = ((z11+1.0)*(z22-1.0)-z12*z21)/d
    return array([s11, s12, s21, s22])

#http://qucs.sourceforge.net/tech/node98.html
def ztos(z11, z12, z21, z22, z1=50., z2=50.):
    d = (z11+z1)*(z22+z2)-z12*z21
    s11 = ((z11-z1)*(z22+z2)-z12*z21)/d
    s12 = sqrt(z2/z1)*2.0*z12*z1/d
    s21 = sqrt(z1/z2)*2.0*z21*z2/d
    s22 = ((z11+z1)*(z22-z2)-z12*z21)/d
    return array([s11, s12, s21, s22])

def ztoa(z11, z12, z21, z22):
    a11 = z11/z21
    a12 = (z11*z22-z12*z21)/z21
    a21 = 1.0/z21
    a22 = z22/z21
    return array([a11, a12, a21, a22])

def atos(a11, a12, a21, a22):
    d = a11 + a12 + a21 + a22
    s11 = (a11 + a12 - a21 - a22)/d
    s12 = 2.0*(a11*a22 - a12*a21)/d
    s21 = 2.0/d
    s22 = (-a11 + a12 - a21 + a22)/d
    return array([s11, s12, s21, s22])



