from exception import *
import os
from ngspice.syntax import Instance, Netlist
from ngspice.syntax import *

from string import *
from libarray import *
from function import *

__all__ = ['Ac', 'Dc', 'Op', 'Sp', 'Sweep']

class Ac(Instance):
    __type__ = "analyse"
    __name__ = "ac"
    __pattern__ = """%s {variation} {n} {fstart} {fstop}
write {name}.%s {exprs}
destroy all
set appendwrite""" % (__name__, __name__)
    __default__ = { 'freq':1e9, 'exprs':'all' }
    def __init__(self, name='ac1', **kwargs):
        self['name'] = name
	self.update( Ac.__default__ )
	if not 'freq' in kwargs:
	    del self['freq']
	self.update( kwargs )
    def __str__(self):
	if 'freq' in self:
            return self.__pattern__.format(**{'variation': 'lin', 
	                                      'name': self['name'],
	                                      'n': 1, 
	                                      'fstart': self['freq'], 
	                                      'fstop': self['freq'], 
					      'exprs' : " ".join(self['exprs'])
	                                  })
	else:
            return self.__pattern__.format(**{'variation': self['variation'], 
	                                      'name': self['name'],
	                                      'n': self['n'], 
	                                      'fstart': self['fstart'], 
	                                      'fstop': self['fstop'], 
					      'exprs' : " ".join(self['exprs'])
	                                  })
    def getRawFiles(self):
        return ['{name}.{extension}'.format(name=self['name'], extension=self.__name__)]


class Dc(Instance):
    __type__ = "analyse"
    __name__ = "dc"
    __pattern__ = """%s {srcname} {vstart} {vstop} {vincr}
write {name}.%s all""" % (__name__, __name__)
    def __init__(self, name='dc1', **parameters):
        self['name'] = name
        self.update(self.__default__)
        self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{'srcname': self['srcname'], 
	                                  'name': self['name'],
	                                  'vstart': self['vstart'], 
	                                  'vstop': self['vstop'], 
	                                  'vincr': self['vincr'], 
	                              })
    def getRawFiles(self):
        return ['{name}.{extension}'.format(name=self['name'], extension=self.__name__)]


class Op(Instance):
    __type__ = "analyse"
    __name__ = "op"
    __pattern__ = """%s
write {name}.%s all""" % (__name__, __name__)
    def __init__(self, name='op1'):
        self['name'] = name
    def __str__(self):
        return self.__pattern__.format(**{'name': self['name']
	                              })

    def getRawFiles(self):
        return ['{name}.{extension}'.format(name=self['name'], extension=self.__name__)]


class Sp(Instance):
    """ Instance for SP simulation
        inputs : * name (str) : name of the simulation
	         * variation  (str): 'lin' or 'log'
	         * n (int) : number of point
	         * fstart (float) : first frequency point
	         * fstop (float) :  last frequency point
	         * ports (list) : list of port name
	         * paramtype : 'y' or 'z' or 'yz'
	         * freq : one point frequency simulation
    """
    __type__ = "analyse"
    __name__ = "sp"
    __default__ = { 'freq':1e9, 'paramtype':'yz', 'ports':['port1'] }

    def __init__(self, name='sp1', **kwargs):
        Sp.ispostSimulation = False
        self['name'] = name
	self.update( Sp.__default__ )
	if not 'freq' in kwargs:
	    del self['freq']
	self.update( kwargs )

    def __str__(self):
	name = self["name"]
        ports = self["ports"]
	exprs = []
	for port in ports:
	    exprs.append( 'x{port}.v'.format(port=port) )
	    exprs.append( 'v.x{port}.v#branch'.format(port=port) )
	netlist = Netlist()
	for i, porti in enumerate(ports):
	    netlist.append( Alter( dev='V.x{port}.Vsrc'.format(port=porti), ac=1.0 ) )
	    for portj in ports:
	        if portj != porti:
		    netlist.append( Alter( dev='V.x{port}.Vsrc'.format(port=portj), ac=0.0 ) )
	    if 'freq' in self:
	        netlist.append( Ac(name='{name}.ac{i}'.format(name=name, i=i), freq=self['freq'], exprs=exprs) )
	    else:
	    	netlist.append( Ac(name='{name}.ac{i}'.format(name=name, i=i), variation=self['variation'], n=self['n'], fstart=self['fstart'], fstop=self['fstop'], exprs=exprs) )
	return str(netlist)

    def getRawFiles(self):
	name = self["name"]
        ports = self["ports"]
        if Sp.ispostSimulation:
	    return ['{name}.sp'.format(name=self["name"])]
	else:
            return ['{name}.ac{i}.ac'.format(name=name, i=i)  for i in xrange(len(ports))]

    def postSimulation(self, cir):
        if Sp.ispostSimulation:
	    return
	ports = self["ports"]
	name = self["name"]
	sp1 = '{name}.sp'.format(name=name)
        cir.raw[sp1] = {}
	for i, porti in enumerate(ports):
	    filename = '{name}.ac{i}.ac'.format(name=name, i=i)
	    ac = cir.raw[filename]
	    vi = ac['x{port}.v'.format(port=porti)]
	    ii = -ac['i(v.x{port}.v)'.format(port=porti)]
	    for j, portj in enumerate(ports):
	        vj = ac['x{port}.v'.format(port=portj)]
		ij = -ac['i(v.x{port}.v)'.format(port=portj)]
		Sji = (vj-50.*ij)/(vi+50.*ii)
		cir.raw[sp1]['s{}{}'.format(j+1, i+1)] = Sji
	cir.raw[sp1]['freq'] = ac['frequency']

	if 'y' in self['paramtype'].lower():
	     if len(ports) == 1:
	         S11 = cir.raw[sp1]['s11']
	         cir.raw[sp1]['y11'] = stoy(S11)
             elif len(ports) == 2:
	         S11, S12, S21, S22 = cir.raw[sp1]['s11'], cir.raw[sp1]['s12'], cir.raw[sp1]['s21'], cir.raw[sp1]['s22']
	         Y11, Y12, Y21, Y22 = stoy(S11, S12, S21, S22)
	         cir.raw[sp1]['y11'] = Y11
	         cir.raw[sp1]['y12'] = Y12
	         cir.raw[sp1]['y21'] = Y21
	         cir.raw[sp1]['y22'] = Y22
	     else:
	         print 'Warning: yz transformation not yet implemented beyond 2 ports'
	    
	if 'z' in self['paramtype'].lower():
	     if len(ports) == 1:
	         S11 = cir.raw[sp1]['s11']
	         cir.raw[sp1]['z11'] = stoz(S11)
             elif len(ports) == 2:
	         S11, S12, S21, S22 = cir.raw[sp1]['s11'], cir.raw[sp1]['s12'], cir.raw[sp1]['s21'], cir.raw[sp1]['s22']
	         Z11, Z12, Z21, Z22 = stoz(S11, S12, S21, S22)
	         cir.raw[sp1]['z11'] = Z11
	         cir.raw[sp1]['z12'] = Z12
	         cir.raw[sp1]['z21'] = Z21
	         cir.raw[sp1]['z22'] = Z22
	     else:
	         print 'Warning: yz transformation not yet implemented beyond 2 ports'
	    
	for filename in self.getRawFiles():
	    del cir.raw[filename]
        Sp.ispostSimulation = True
	   
	    

from copy import copy
class Sweep(Instance):
    __type__ = "analyse"
    __name__ = "sweep"
    def __init__(self, name='swp1', param='', values='', child=None):
        self['name'] = name
	self['param'] = param
	self['values'] = values
	self['child'] = child

    def __str__(self):
	netlist = Netlist()
	for i in xrange(len(self['values'])):
	    netlist.append( Alter( dev=self['param'], value=self['values'][i] ) )
	    analyse = copy(self['child'])
	    analyse['name'] = "{name}-{number}_{childname}".format(name=self['name'], number=zfill(i+1,3), childname=self['child']['name'])
	    netlist.append( analyse )
	return str(netlist)
    
    def getNumberOfPoints(self):
        if 'values' in self:
            return len(self['values'])

    def getRawFiles(self):
        raw_files = []
        for i in xrange(int(self.getNumberOfPoints())):
            raw_files.append("{name}-{number}_{childname}".format(name=self['name'], number=zfill(i+1,3), childname=self['child'].getRawFiles()[0]))
	return raw_files



