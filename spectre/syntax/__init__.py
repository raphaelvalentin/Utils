""" primitives
"""
from exception import *
from spectre import simulator
from function import flatten
import os
from spectre.syntax import *
from spectre.modelParameter import modelParameter

nan = float('nan')

class Netlist(list):
    __name__ = 'netlist'
    __indent__ = ""
    def __init__(self, *kwargs):
        list.__init__(self, kwargs)
	self.raw = {}
    def __str__(self):
        _indent = ""
        s = []
        isverbose = False
        for dev in self:
	    dev.__indent__ = self.__indent__
	    try:
	        if dev.__name__ is 'verbose':
	            isverbose = True
	    except:
	        pass
            s.append(dev.__str__())
	if not self.__class__.__name__ in ('Verbose', 'Info'):
	    if not isverbose:
	        if hasattr(self,'__verbose__') and self.__verbose__:
	            s.append(Verbose().__str__())
        return "\n".join(s)
    def getitem(self, name):
        for i in xrange(len(self)):
            if 'name' in dir(self[i]):
                if self[i].name==name:
                    return self[i]
    def setitem(self, name, dev):
        for i in xrange(len(self)):
            if 'name' in dir(self[i]):
                if self[i].name==name:
                    self[i] = dev
    def index(self, name):
        for i in xrange(len(self)):
            if list.__getitem__(self, i).name==name:
                return i
        list.index(self, name)
    def keys(self):
        return [dev.name for dev in self]
    def set(self, key, value):
        try:
	    setattr(self, key, value)
	except:
	    pass
    def get(self, key, default=None):
        return getattr(self, key, default)
    def getRawFiles(self):
        r = []
	for el in flatten(self):
	    if hasattr(el, "__type__") and el.__type__ is 'analyse':
	        if hasattr(el, "getRawFiles"):
	            r.extend(el.getRawFiles())
	return r
    def simulate(self, **parameters):
        s = simulator.spectre(netlist=self, **parameters)
	s.run()
	self.raw = s.raw
        self.modelParameter = {}
	try:
    	    path = s.__parameters__['path']
	    if os.path.isfile(path+'modelParameter.info'):
	        self.modelParameter = modelParameter(filename=path+'modelParameter.info').read()
	except:
	    print 'Warning: The extraction of the modelParameter has generated an Exception.'
        return self
    def __eq__(self, obj):
        if isinstance(obj, Netlist):
	    return self.__str__() == obj.__str__() and dir(self) == dir(obj)
	return False
 

@deprecated
class common(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            if k in self.__dict__:
                setattr(self, k, v)
    def __eq__(self, obj):
        if hasattr(obj, '__dict__'):
            return self.__dict__==obj.__dict__
        else:
            return False
    def set(self, key, value):
        if key in self.__dict__:
            setattr(self, key, value)
    def get(self, key, default):
        return getattr(self, key, default)


class Instance(dict):
    """ Primitive class 
    """
    __specialkeywords__ = ('name', 'nodes', 'model', 'library')
    def __str__(self):
        return " ".join(["%s=%s" % (k, v) for k, v in self.iteritems() if not k in self.__specialkeywords__])
    def setSpecialKeywords(self, *keywords):
        self.__specialkeywords__ = keywords
    def set(self, *args, **kwargs):
        for i in xrange(0, len(args), 2):
            self[args[i]] = args[i+1]
        for key, value in kwargs.iteritems():
            self[key] = value
    def get(self, key, default=None):
        if key in self:
	    return self[key]
	if key in dir(self):
	    return getattr(self, key)
        return default
    def __eq__(self, obj):
        if isinstance(obj, Instance):
	    return self.__str__() == obj.__str__() and dir(self) == dir(obj)
	return False
	    

#@deprecated
class __public__(object):
    __type__ = 'public'
    fset = None
    fget = None
    def __init__(self, name, default=None, doc=""):
        self.__name__ = name
        self.__value__ = default
        self.__doc__ = doc
    def __get__(self, instance, owner):
        if instance is None:
            return self
        if not(self.fget is None):
            return self.fget(instance)
        return self.__value__
    def __set__(self, instance, value):
        self.__value__ = value
        if not(self.fset is None):
            self.fset(instance, value)
    def __str__(self):
        return str(self.__value__)


from analyse import *
from instance import *
from smu import *
from vna import *
from balun import Balun
from transformer import Transformer
from fracpole import Fracpole
