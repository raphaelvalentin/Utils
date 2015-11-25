cimport cython
from libc.stdlib cimport malloc, free

# LOW LEVEL SEARCH FUNCTION
cdef _nearest1(float *cflist, int n, float value, int *index):
    cdef float ci, ci1
    index[0] = 0
    ci1 = cflist[0] - value
    if ci1 < 0:
        ci1 = -ci1
    for i in range(1, n, 1):
        ci = cflist[i] - value
        if ci < 0:
            ci = -ci
        if ci < ci1:
            index[0] = i
            ci1 = ci

cdef _nearest2(float *cflist, int n, float value, int *index):
    cdef float ci, ci1, ci2
    ci1 = cflist[0] - value
    if ci1 < 0:   # abs
        ci1 = -ci1
    ci2 = cflist[1] - value
    if ci2 < 0:   # abs
        ci2 = -ci2
    if ci1 < ci2:
        index[0] = 0
        index[1] = 1
    else:
        index[0] = 1
        index[1] = 0
        t = ci1
        ci1 = ci2
        ci2 = t
    for i in range(2, n, 1):
        ci = cflist[i] - value
        if ci < 0:   # abs
            ci = -ci
        if ci < ci1:
            index[1] = index[0]
            index[0] = i
            ci2 = ci1
            ci1 = ci
        elif ci < ci2:
            index[1] = i
            ci2 = ci

cdef _nearest3(float *cflist, int n, float value, int *index):
    cdef float ci, ci0, ci1, ci2
    # initialize
    index[0] = 0
    ci0 = cflist[0] - value
    if ci0 < 0:
        ci0 = -ci0
    index[1] = 1
    ci1 = cflist[1] - value
    if ci1 < 0:
        ci1 = -ci1
    index[2] = 2
    ci2 = cflist[2] - value
    if ci2 < 0:
        ci2 = -ci2
    # sort
    if ci2 < ci1:
        t = ci1
        ci1 = ci2
        ci2 = t
    if ci1 < ci0:
        t = ci0
        ci0 = ci1
        ci1 = t
    if ci2 < ci1:
        t = ci1
        ci1 = ci2
        ci2 = t
    for i in range(3, n, 1):
        ci = cflist[i] - value
        if ci < 0:
            ci = -ci
        if ci < ci0:
            index[2] = index[1]
            index[1] = index[0]
            index[0] = i
            ci2 = ci1
            ci1 = ci0
            ci0 = ci
        elif ci < ci1:
            index[2] = index[1]
            index[1] = i
            ci2 = ci1
            ci1 = ci
        elif ci < ci2:
            index[2] = i
            ci2 = ci



# WRAP
def nearest1(flist, value):

    # DECLARATION C VARIABLES
    cdef float* cflist
    cdef int* cindex 
    cdef int n
    n = len(flist)
    if n > 0:

        # DECLARATION C ARRAYS
        cindex  = <int *> malloc(1*cython.sizeof(int))
        if cindex is NULL:
            raise MemoryError()

        cflist = <float *> malloc(n*cython.sizeof(float))
        if cflist is NULL:
            raise MemoryError()

        # INIT ARRAY
        for i in range(n):
            cflist[i] = flist[i]

        # RUN ALGORITHM
        _nearest1(cflist, n, value, cindex)
        free(cflist)
        i0 = cindex[0]
        free(cindex)
        
        return i0
    else:
        raise Exception('Warning : list length is too short')

def nearest2(flist, value):

    # DECLARATION C VARIABLES
    cdef float* cflist
    cdef int* cindex 
    cdef int n
    n = len(flist)
    if n > 0:

        # DECLARATION C ARRAYS
        cindex  = <int *> malloc(2*cython.sizeof(int))
        if cindex is NULL:
            raise MemoryError()

        cflist = <float *> malloc(n*cython.sizeof(float))
        if cflist is NULL:
            raise MemoryError()

        # INIT ARRAY
        for i in range(n):
            cflist[i] = flist[i]

        # RUN ALGORITHM
        _nearest2(cflist, n, value, cindex)
        free(cflist)
        i0, i1 = cindex[0], cindex[1]
        free(cindex)
        
        return i0, i1
    else:
        raise Exception('Warning : list length is too short')

def nearest3(flist, value):

    # DECLARATION C VARIABLES
    cdef float* cflist
    cdef int* cindex 
    cdef int n
    n = len(flist)
    if n > 0:

        # DECLARATION C ARRAYS
        cindex  = <int *> malloc(3*cython.sizeof(int))
        if cindex is NULL:
            raise MemoryError()

        cflist = <float *> malloc(n*cython.sizeof(float))
        if cflist is NULL:
            raise MemoryError()

        # INIT ARRAY
        for i in range(n):
            cflist[i] = flist[i]

        # RUN ALGORITHM
        _nearest3(cflist, n, value, cindex)
        free(cflist)
        i0, i1, i2 = cindex[0], cindex[1], cindex[2]
        free(cindex)
        
        return i0, i1, i2
    else:
        raise Exception('Warning : list length is too short')


