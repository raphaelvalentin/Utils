import numpy as np
from _nearest import nearest1 as _nearest1, nearest2 as _nearest2, nearest3 as _nearest3

__all__ = ['nearest1', 'nearest2', 'nearest3', '_nearest1', '_nearest2', '_nearest3']

def nearest1(array, value):
    if isinstance(array, np.ndarray):
        if array.dtype == float:
            return _nearest1(array, value)
        else:
            return _nearest1(array.astype(float), value)
    elif isinstance(array, list):
        return _nearest1(np.array(array, float), value)
    else:
        raise ValueError('wrong arguments')
             
def nearest2(array, value):
    if isinstance(array, np.ndarray):
        if array.dtype == float:
            return _nearest2(array, value)
        else:
            return _nearest2(array.astype(float), value)
    elif isinstance(array, list):
        return _nearest2(np.array(array, float), value)
    else:
        raise ValueError('wrong arguments')
             
def nearest3(array, value):
    if isinstance(array, np.ndarray):
        if array.dtype == float:
            return _nearest3(array, value)
        else:
            return _nearest3(array.astype(float), value)
    elif isinstance(array, list):
        return _nearest3(np.array(array, float), value)
    else:
        raise ValueError('wrong arguments')
             

