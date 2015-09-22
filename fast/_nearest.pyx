cimport cython
from libc.stdlib cimport malloc, free

# LOW LEVEL SEARCH FUNCTION (FASTEST)
cdef _nearest1(float *cflist, int n, float value, int *index):
    cdef float result0
    cdef int index0
    cdef float ci1, ci2
    result0 = cflist[0]
    index0 = 0
    for i in range(1, n, 1):
        ci1 = cflist[i] - value
        ci2 = result0 - value
        if ci1*ci1 < ci2*ci2:
            result0 = cflist[i]
            index0 = i
    index[0] = index0

cdef _nearest2(float *cflist, int n, float value, int *index):
    cdef float result0, result1
    cdef int index0, index1
    cdef float ci1, ci2, ci3
    result0 = cflist[0]
    result1 = cflist[1]
    index0 = 0
    index1 = 1
    for i in range(2, n, 1):
        ci1 = cflist[i] - value
        ci2 = result0 - value
        ci3 = result1 - value
        if value!=result1 and ci1*ci1 < ci2*ci2:
            result0 = cflist[i]
            index0 = i
        elif value!=result0 and ci1*ci1 < ci3*ci3:
            result1 = cflist[i]
            index1 = i
    index[0] = index0
    index[1] = index1

cdef _nearest3(float *cflist, int n, float value, int *index):
    cdef float result0, result1, result2
    cdef int index0, index1, index2
    cdef float ci1, ci2, ci3, ci4
    result0 = cflist[0]
    result1 = cflist[1]
    result2 = cflist[2]
    index0 = 0
    index1 = 1
    index2 = 2
    for i in range(3, n, 1):
        ci1 = cflist[i] - value
        ci2 = result0 - value
        ci3 = result1 - value
        ci4 = result2 - value
        if value!=result1 and value!=result2 and ci1*ci1 < ci2*ci2:
            result0 = cflist[i]
        elif value!=result0 and value!=result2 and ci1*ci1 < ci3*ci3:
            result1 = cflist[i]
        elif value!=result0 and value!=result1 and ci1*ci1 < ci4*ci4:
            result2 = cflist[i]
    index[0] = index0
    index[1] = index1
    index[2] = index2

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


