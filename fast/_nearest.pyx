cimport cython
import numpy as np
cimport numpy as np

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef nearest1(np.ndarray[double, ndim=1] array, double value):
    """ return the index of the nearest point of a numpy array of double
    """
    cdef int* cindex  = [0]
    cdef int n = array.shape[0]
    cdef float ci, ci1
    cdef int i
    assert n>0, 'size of array too short'
    cindex[0] = 0
    ci1 = array[0] - value
    if ci1 < 0.0:
        ci1 = -ci1
    for i in range(1, n, 1):
        ci = array[<unsigned int>(i)] - value
        if ci < 0.0:
            ci = -ci
        if ci < ci1:
            cindex[0] = i
            ci1 = ci
    return cindex[0]


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef nearest2(np.ndarray[double, ndim=1] array, double value):
    """ return the 2 indexes of the nearest point of a numpy array of double
    """
    cdef int* cindex  = [0, 1]
    cdef int n = array.shape[0]
    cdef float ci, ci1, ci2
    cdef int i
    assert n>1, 'size of array too short'
    ci1 = array[0] - value
    if ci1 < 0:   # abs
        ci1 = -ci1
    ci2 = array[1] - value
    if ci2 < 0:   # abs
        ci2 = -ci2
    if ci1 > ci2:
        cindex[0], cindex[1] = 1, 0
        ci1, ci2 = ci2, ci1
    for i in range(2, n, 1):
        ci = array[<unsigned int>(i)] - value
        if ci < 0:   # abs
            ci = -ci
        if ci < ci1:
            cindex[1] = cindex[0]
            cindex[0] = i
            ci2 = ci1
            ci1 = ci
        elif ci < ci2:
            cindex[1] = i
            ci2 = ci
    return cindex[0], cindex[1]


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef nearest3(np.ndarray[double, ndim=1] array, double value):
    """ return the 3 indexes of the nearest point of a numpy array of double
    """
    cdef int* cindex  = [0, 1, 2]
    cdef int n = array.shape[0]
    cdef float ci, ci0, ci1, ci2
    cdef int i
    # initialize
    cindex[0] = 0
    ci0 = array[0] - value
    if ci0 < 0:
        ci0 = -ci0
    cindex[1] = 1
    ci1 = array[1] - value
    if ci1 < 0:
        ci1 = -ci1
    cindex[2] = 2
    ci2 = array[2] - value
    if ci2 < 0:
        ci2 = -ci2
    # sort
    if ci2 < ci1:
        cindex[1], cindex[2] = cindex[2], cindex[1]
        ci1, ci2 = ci2, ci1
    if ci1 < ci0:
        cindex[0], cindex[1] = cindex[1], cindex[0]
        ci0, ci1 = ci1, ci0
    if ci2 < ci1:
        cindex[1], cindex[2] = cindex[2], cindex[1]
        ci1, ci2 = ci2, ci1
    for i in range(3, n, 1):
        ci = array[<unsigned int>(i)] - value
        if ci < 0:
            ci = -ci
        if ci < ci0:
            cindex[2] = cindex[1]
            cindex[1] = cindex[0]
            cindex[0] = i
            ci2 = ci1
            ci1 = ci0
            ci0 = ci
        elif ci < ci1:
            cindex[2] = cindex[1]
            cindex[1] = i
            ci2 = ci1
            ci1 = ci
        elif ci < ci2:
            cindex[2] = i
            ci2 = ci
    return cindex[0], cindex[1], cindex[2]


