from math import sqrt
from functions.science import sign

def minimize_scalar_bounded(func, bounds, args=(), xtol=1e-5, maxiter=500, disp=0):

    maxfun = maxiter
    # Test bounds are of correct form
    if len(bounds) != 2:
        raise ValueError('bounds must have two elements.')
    x1, x2 = min(bounds), max(bounds)

    flag = 0
    header = ' Func-count     x          f(x)          Procedure'
    step = '       initial'

    sqrt_eps = sqrt(2.2e-16)
    golden_mean = 0.5*(3.0 - sqrt(5.0))
    a, b = x1, x2
    fulc = a + golden_mean*(b - a)
    nfc, xf = fulc, fulc
    rat = e = 0.0
    x = xf
    fx = func(x, *args)
    num = 1
    fmin_data = (1, xf, fx)

    ffulc = fnfc = fx
    xm = 0.5*(a + b)
    tol1 = sqrt_eps*abs(xf) + xtol / 3.0
    tol2 = 2.0*tol1

    if disp > 2:
        print (" ")
        print (header)
        print "%5.0f   %12.6g %12.6g %s" % (fmin_data + (step,))


    while (abs(xf - xm) > (tol2 - 0.5*(b - a))):
        golden = 1
        # Check for parabolic fit
        if abs(e) > tol1:
            golden = 0
            r = (xf - nfc)*(fx - ffulc)
            q = (xf - fulc)*(fx - fnfc)
            p = (xf - fulc)*q - (xf - nfc)*r
            q = 2.0*(q - r)
            if q > 0.0: p = -p
            q = abs(q)
            r = e
            e = rat

            # Check for acceptability of parabola
            if ((abs(p) < abs(0.5*q*r)) and (p > q*(a - xf)) and \
                 (p < q*(b - xf))):
                rat = (p + 0.0) / q
                x = xf + rat
                step = '       parabolic'

                if ((x - a) < tol2) or ((b - x) < tol2):
                    si = sign(xm - xf) + ((xm - xf) == 0)
                    rat = tol1*si
            else:      # do a golden section step
                golden = 1

        if golden:  # Do a golden-section step
            if xf >= xm:
                e = a - xf
            else:
                e = b - xf
            rat = golden_mean*e
            step = '       golden'

        si = sign(rat) + (rat == 0)
        x = xf + si*max([abs(rat), tol1])
        fu = func(x, *args)
        num += 1
        fmin_data = (num, x, fu)
        if disp > 2:
            print "%5.0f   %12.6g %12.6g %s" % (fmin_data + (step,))

        if fu <= fx:
            if x >= xf:
                a = xf
            else:
                b = xf
            fulc, ffulc = nfc, fnfc
            nfc, fnfc = xf, fx
            xf, fx = x, fu
        else:
            if x < xf:
                a = x
            else:
                b = x
            if (fu <= fnfc) or (nfc == xf):
                fulc, ffulc = nfc, fnfc
                nfc, fnfc = x, fu
            elif (fu <= ffulc) or (fulc == xf) or (fulc == nfc):
                fulc, ffulc = x, fu

        xm = 0.5*(a + b)
        tol1 = sqrt_eps*abs(xf) + xtol / 3.0
        tol2 = 2.0*tol1

        if num >= maxfun:
            flag = 1
            break

    fval = fx
    if disp > 0:
        _endprint(x, flag, fval, maxfun, xtol, disp)

    result = (fval, flag, (flag == 0),
                    {0: 'Solution found.',
                     1: 'Maximum number of function calls '
                                'reached.'}.get(flag, ''),
                    xf, num)

    return result

def _endprint(x, flag, fval, maxfun, xtol, disp):
    if flag == 0:
        if disp > 1:
            print "\nOptimization terminated successfully;\n" \
                  "The returned value satisfies the termination criteria\n" \
                  "(using xtol = ", xtol, ")"
    if flag == 1:
        print "\nMaximum number of function evaluations exceeded --- " \
              "increase maxfun argument.\n"
    return


if __name__ == '__main__':
    def f(x):
        return (x-2.0)*(x+2.0)**2

    print minimize_scalar_bounded(f, bounds=(0, 10), args=(), xtol=1e-9, maxiter=500, disp=3)


