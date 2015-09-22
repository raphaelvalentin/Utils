""" primitives
"""
from time import time
from exception import *
from function import flatten
import os
from ngspice.syntax import *
from ngspice import simulator

class Netlist(list):
    __name__ = 'netlist'
    __indent__ = ""
    def __init__(self, *kwargs):
        list.__init__(self, kwargs)
	self.raw = {}
    def __str__(self):
        s = []
        isverbose = False
        for dev in self:
	    if hasattr(dev, '__indent__'):
	        dev.__indent__ = self.__indent__
	    if hasattr(dev, '__name__') and dev.__name__ is 'verbose':
	        isverbose = True
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
	    if hasattr(el, "__type__") and el.__type__ is 'analyse' and hasattr(el, "getRawFiles"):
	        for rawfile in el.getRawFiles():
		    if not rawfile in r:
		        r.append( rawfile )
	return r
    def postSimulation(self, cir):
        analyse_names = []
	for el in flatten(self):
	    if hasattr(el, "__type__") and el.__type__ is 'analyse':
	        if hasattr(el, "postSimulation"):
		    if not el['name'] in analyse_names:
	                el.postSimulation(cir)
			analyse_names.append( el['name'] )
    def simulate(self, **parameters):
        s = simulator.ngspice(netlist=self, **parameters)
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
 

#from collections import OrderedDict

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
	    

from instance import *
from analyse import *
from ngspice.syntax.nport import *
from fracpole import *
