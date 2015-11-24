import os
from spectre.syntax import Instance, common
from string import *
import numpy as np

__all__ = ['Noise', 'Xf', 'Ac', 'Dc', 'Sweep', 'MonteCarlo', 'Sp', 'Transient', 'Pss' ]

class values(list):
    def __init__(self, it):
        if isinstance(it, (list, np.ndarray)):
            list.__init__(self, it)
	else:
	    list.__init__(self, [it])
    def __str__(self):
        l = []
	for v in self:
	    if type(v) == str:
	        l.append(v)
	    else:
	        l.append("%g"%v)
        return "[{it}]".format(it=" ".join(l))


class Noise(Instance):
    __type__ = "analyse"
    __name__ = "noise"
    __pattern__ = "{name} %s {**parameters}" % __name__
    __default__ = {'oprobe':'', 'iprobe':'', 'annotate':'status', 'oppoint':'raw_file' }
    def __init__(self, name='noise1', **parameters):
        self['name'] = name
        self.update(self.__default__)
        self.update(parameters)
    def __str__(self):
        if 'values' in self:
	    self['values'] = values(self['values'])
        return self.__pattern__.format(**{'name': self['name'], 
	                                  '**parameters':" ".join(["%s=%s" % (k, v) for k, v in self.iteritems() if not k in ('name',)])
	                              })
    def getRawFiles(self):
        return ['{name}.{extension}'.format(name=self['name'], extension=self.__name__)]

class Xf(Instance):
    __type__ = "analyse"
    __name__ = "xf"
    __pattern__ = "{name} %s {**parameters}" % __name__
    __default__ = {'annotate':'status', 'oppoint':'raw_file' }
    def __init__(self, name='xf1', **parameters):
        self['name'] = name
        self.update(self.__default__)
        self.update(parameters)
    def __str__(self):
        if 'values' in self:
	    self['values'] = values(self['values'])
        return self.__pattern__.format(**{'name': self['name'], 
	                                  '**parameters':" ".join(["%s=%s" % (k, v) for k, v in self.iteritems() if not k in ('name',)])
	                              })
    def getRawFiles(self):
        return ['{name}.{extension}'.format(name=self['name'], extension=self.__name__)]


class Ac(Instance):
    __type__ = "analyse"
    __name__ = "ac"
    __pattern__ = "{name} %s {**parameters}" % __name__
    def __init__(self, name='ac1', **parameters):
        self['name'] = name
        self.update(parameters)
    def __str__(self):
        if 'values' in self:
	    self['values'] = values(self['values'])
        return self.__pattern__.format(**{'name': self['name'], 
	                                  '**parameters':" ".join(["%s=%s" % (k, v) for k, v in self.iteritems() if not k in ('name',)])
	                              })
    def getRawFiles(self):
        return ['{name}.{extension}'.format(name=self['name'], extension=self.__name__)]

            
class Dc(Instance):
    __type__ = "analyse"
    __name__ = "dc"
    __pattern__ = "{name} %s {**parameters}" % __name__
    __default__ = { 'oppoint':'rawfile', 'maxiters':150, 'maxsteps':10000, 'annotate':'status' }
    def __init__(self, name='dc1', **parameters):
        self['name'] = name
        self.update(self.__default__)
        self.update(parameters)
    def __str__(self):
        if 'values' in self:
	    self['values'] = values(self['values'])
        return self.__pattern__.format(**{'name': self['name'], 
	                                  '**parameters':" ".join(["%s=%s" % (k, v) for k, v in self.iteritems() if not k in ('name',)])
	                              })
    def getRawFiles(self):
        return ['{name}.{extension}'.format(name=self['name'], extension=self.__name__)]


class Sweep(Instance):
    __type__ = "analyse"
    __name__ = "sweep"
    __pattern__ = "{name} %s {**parameters} {child}" % __name__
    __default__ = { 'oppoint':'rawfile' }
    def __init__(self, name='swp1', child=None, **parameters):
        self['name'] = name
        self.update(self.__default__)
        self.update(parameters)
        self['child'] = child
    def __str__(self):
        if 'values' in self:
	    self['values'] = values(self['values'])
	child = ''
	if self['child']:
	    child = "{\n" + str(self['child']) + "\n}"
        return self.__pattern__.format(**{'name': self['name'], 
	                                  'child': child,
	                                  '**parameters':" ".join(["%s=%s" % (k, v) for k, v in self.iteritems() if not k in ('name', 'child')])
	                              })
    def getNumberOfPoints(self):
        if 'values' in self:
            return len(self['values'])
        elif 'stop' in self:
            if 'lin' in self:
                return self['lin']+1
            elif 'log' in self:
                return self['log']
            elif 'step' in self:
                if 'start' in self:
                    return (self['stop']-self['start'])/self['step']+1
                else:
                    return self['stop']/self['step']+1
            else:
                return 50
        else:
            return 1
    def getRawFiles(self):
        raw_files = []
        if self['child']:
            for i in xrange(int(self.getNumberOfPoints())):
                raw_files.append("{name}-{number}_{childname}".format(name=self['name'], number=zfill(i,3), childname=self['child'].getRawFiles()[0]))
        else:
            raw_files.append(['{name}.{extension}'.format(name=self['name'], extension=self.__name__)])
	return raw_files

            
class MonteCarlo(Instance):
    __type__ = "analyse"
    __name__ = "montecarlo"
    __pattern__ = "{name} %s {**parameters} {child}" % __name__
    __default__ = { 'variations':'all', 'numruns':3, 'savefamilyplots':'yes', 'saveprocessparams':'yes', 'processscalarfile':'\"process.dat\"' }
    def __init__(self, name='mc1', child=None, **parameters):
        self['name'] = name
        self.update(self.__default__)
        self.update(parameters)
        self['child'] = child
    def __str__(self):
	child = ''
	if self['child']:
	    child = "{\n" + str(self['child']) + "\n}"
        return self.__pattern__.format(**{'name': self['name'], 
	                                  'child': child,
	                                  '**parameters':" ".join(["%s=%s" % (k, v) for k, v in self.iteritems() if not k in ('name','child')])
	                              })
    def getRawFiles(self):
        raw_files = []
        if self['child']:
            for i in xrange(self.getNumberOfPoints()):
                raw_files.append("{name}-{number}_{childname}".format(name=self['name'], number=zfill(i+1,3), childname=self['child'].getRawFiles()[0]))
        else:
            raw_files.append(['{name}.{extension}'.format(name=self['name'], extension='mc')])
	return raw_files
    def getNumberOfPoints(self):
        return self['numruns']


class Sp(Instance):
    __type__ = "analyse"
    __name__ = "sp"
    __pattern__ = "{name} %s {**parameters}" % __name__
    __default__ = {'annotate':'status', 'paramtype':'yz',
                   'oppoint':'screen',  'datatype':'realimag'}
    def __init__(self, name='sp1', **parameters):
        self['name'] = name
	if isinstance(parameters['ports'], list):
	    parameters['ports'] = "[" + " ".join(parameters['ports']) + "]"
        self.update(self.__default__)
	self.update(parameters)
    def __str__(self):
        if 'values' in self:
	    self['values'] = values(self['values'])
        parameters = ["%s=%s" % (k, v) \
		      for k, v in self.iteritems() \
		      if k not in ('name', 'donoise')]
        if self.get('donoise',False):
            parameters.append('donoise=yes')
        return self.__pattern__.format(**{'name': self['name'], 
		                          '**parameters': " ".join(parameters),
					 })
    def getRawFiles(self):
        if 'donoise' in self:
	    if self['donoise'] in ('True', True):
                return ['{name}.{extension}'.format(name=self['name'], extension=self.__name__), 
                        '{name}.noise.{extension}'.format(name=self['name'], extension=self.__name__)]
        return ['{name}.{extension}'.format(name=self['name'], extension=self.__name__)]


class Transient(Instance):
    __type__ = "analyse"
    __name__ = "tran"
    __pattern__ = "{name} %s {**parameters}" % __name__
    __default__ = { 'errpreset':'conservative', 'write':'spectre.ic', 'writefinal':'spectre.fc', 'annotate':'status', 'maxiters':5 }
    def __init__(self, name='tran1', **parameters):
        self['name'] = name
        self.update(self.__default__)
        self.update(parameters)
    def __str__(self):
        if 'values' in self:
	    self['values'] = values(self['values'])
        return self.__pattern__.format(**{'name': self['name'], 
	                                  '**parameters':" ".join(["%s=%s" % (k, v) for k, v in self.iteritems() if not k in ('name',)])
	                              })
    def getRawFiles(self):
        return ['{name}.{extension}'.format(name=self['name'], extension=self.__name__)]


class Pss(Instance):
    __type__ = "analyse"
    __name__ = "pss"
    __pattern__ = "{name} %s {**parameters}" % __name__
    __default__ = { 'errpreset':'conservative', 'annotate':'status'}
    def __init__(self, name='pss1', **parameters):
        self['name'] = name
        self.update(self.__default__)
        self.update(parameters)
    def __str__(self):
        if 'values' in self:
	    self['values'] = values(self['values'])
        return self.__pattern__.format(**{'name': self['name'], 
	                                  '**parameters':" ".join(["%s=%s" % (k, v) for k, v in self.iteritems() if not k in ('name',)])
	                              })
    def getRawFiles(self):
        return ['{name}.fd.{extension}'.format(name=self['name'], extension=self.__name__)]
"""
liberal      1e-3    sigglobal  traponly   3.5       0.001        period/50
moderate     1e-3    alllocal   gear2only  3.5       0.001        period/200
conservative 1e-4    alllocal   gear2only  *         0.01         period/200
"""
