from ngspice.syntax import *
import os
from math import pi



class vector(list):
    def __init__(self, it):
        if isinstance(it, list):
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


__newnode__ = 1
def newnode():
    global __newnode__
    x = __newnode__
    __newnode__ += 1
    return '_n%r'%x

__newname__ = {}
def newname(prefix):
    global __newname__
    if not prefix in __newname__:
        __newname__[prefix] = 1
    x = __newname__[prefix]
    __newname__[prefix] += 1
    return '%s%r'%(str(prefix), x)

class Device(Instance):
    __name__ = "R"
    __type__ = "instance"
    __pattern__ = "{indent}{name} {nodes} {model} {**parameters}"
    __indent__ = ""
    def __init__(self, name='x1', nodes=('in', 'out'), model='', **parameters):
        self['name'] = name
        self['nodes'] = nodes
        self['model'] = model
	for k, v in parameters.iteritems():
	    if isinstance(v, str):
	        parameters[k] = "{%s}"%v
      	self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{ 'indent': self.__indent__,
	                                   'name': self['name'],
	                                   'nodes': "%s"%" ".join(self['nodes']),
					   'model': self['model'],
		                           '**parameters': " ".join(["%s=%s" % (k, v) \
					                             for k, v in self.iteritems() \
					                             if k not in ('name', 'nodes', 'model') and k[0]<>'_']) 
					 })


class Resistor(Instance):
    __name__ = "r"
    __type__ = "instance"
    __pattern__ = "{indent}%s{name} {nodes} {r} {**parameters}"% __name__
    __indent__ = ""
    def __init__(self, name='R1', nodes=('in', 'out'), r=100, **parameters):
        self['name'] = name
        self['nodes'] = nodes
	if isinstance(r, str):
	    self['r'] = "{%s}"%r
	else:
	    self['r'] = r
	for k, v in parameters.iteritems():
	    if isinstance(v, str):
	        parameters[k] = "{%s}"%v
      	self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{ 'indent': self.__indent__,
	                                   'name': self['name'] if self['name'][0].lower()<>self.__name__ else self['name'][1:],
	                                   'nodes': " ".join(self['nodes']),
					   'r': self['r'],
		                           '**parameters': " ".join(["%s=%s" % (k, v) \
					                             for k, v in self.iteritems() \
					                             if k not in ('name', 'nodes', 'r') and k[0]<>'_']) 
					 })


class Inductor(Instance):
    __name__ = "l"
    __type__ = "instance"
    __pattern__ = "{indent}%s{name} {nodes} {l} {**parameters}"% __name__
    __indent__ = ""
    def __init__(self, name='L1', nodes=('in', 'out'), l=1e-9, **parameters):
        self['name'] = name
        self['nodes'] = nodes
	if isinstance(l, str):
	    self['l'] = "{%s}"%l
	else:
	    self['l'] = l
	for k, v in parameters.iteritems():
	    if isinstance(v, str):
	        parameters[k] = "{%s}"%v
      	self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{ 'indent': self.__indent__,
	                                   'name': self['name'] if self['name'][0].lower()<>self.__name__ else self['name'][1:],
	                                   'nodes': " ".join(self['nodes']),
					   'l': self['l'],
		                           '**parameters': " ".join(["%s=%s" % (k, v) \
					                             for k, v in self.iteritems() \
					                             if k not in ('name', 'nodes', 'l') and k[0]<>'_']) 
					 })


class MutualInductor(Device):
    __name__ = "k"
    __type__ = "instance"
    __pattern__ = "{indent}%s{name} {ind1} {ind2} {coupling}" % __name__
    __indent__ = ""
    def __init__(self, name='K1', coupling=0.5, ind1='l1', ind2='l2'):
        self['name'] = name
	if isinstance(coupling, str):
	    self['coupling'] = "{%s}"%coupling
	else:
	    self['coupling'] = coupling
	self['ind1'] = ind1
	self['ind2'] = ind2
    def __str__(self):
        return self.__pattern__.format(**{ 'name': self['name'] if self['name'][0].lower()<>self.__name__ else self['name'][1:],
	                                   'indent':self.__indent__,
	                                   'ind1':self['ind1'],
	                                   'ind2':self['ind2'],
	                                   'coupling':self['coupling'],
 					     })


class Capacitor(Instance):
    __name__ = "c"
    __type__ = "instance"
    __pattern__ = "{indent}%s{name} {nodes} {c} {**parameters}"% __name__
    __indent__ = ""
    def __init__(self, name='C1', nodes=('in', 'out'), c=1e-12, **parameters):
        self['name'] = name
        self['nodes'] = nodes
	if isinstance(c, str):
	    self['c'] = "{%s}"%c
	else:
	    self['c'] = c
	for k, v in parameters.iteritems():
	    if isinstance(v, str):
	        parameters[k] = "{%s}"%v
      	self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{ 'indent': self.__indent__,
	                                   'name': self['name'] if self['name'][0].lower()<>self.__name__ else self['name'][1:],
	                                   'nodes': " ".join(self['nodes']),
					   'c': self['c'],
		                           '**parameters': " ".join(["%s=%s" % (k, v) \
					                             for k, v in self.iteritems() \
					                             if k not in ('name', 'nodes', 'c') and k[0]<>'_']) 
					 })


class Vsource(Instance):
    __name__ = "v"
    __type__ = "instance"
    __pattern__ = "{indent}%s{name} {nodes} dc {dc} ac {ac} {**parameters}" % __name__
    __indent__ = ""
    def __init__(self, name='V1', nodes=(), dc=0, ac=0, **parameters):
        self['name'] = name
	self['nodes'] = nodes
	self['dc'] = dc
	self['ac'] = ac
	self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{ 'name': self['name'] if self['name'][0].lower()<>self.__name__ else self['name'][1:],
	                                   'indent':self.__indent__,
	                                   'nodes': " ".join(self['nodes']),
					   'dc': self['dc'],
					   'ac': self['ac'],
		                           '**parameters': " ".join(["%s=%s" % (k, v) \
					                             for k, v in self.iteritems() \
								     if not k in ('name', 'nodes', 'dc', 'ac')]) 
					 })


class Options(Instance):
    __name__ = ".options"
    __type__ = "instance"
    __pattern__ = "%s {*args} {**kwargs}" % __name__
    __indent__ = ""
    __default__ = { 'noacct':'' }
    def __init__(self, name='simulatorOptions', *args,  **kwargs):
        self['name'] = name
        for arg in args:
	    self[arg] = ''
	self.update(self.__default__)
        self.update(kwargs)
    def __str__(self):
        return self.__pattern__.format(**{ '*args': " ".join(["%s" % key \
					                             for key, value in self.iteritems() \
								     if not key in ('name',) and value == '']),
	                                   '**kwargs': " ".join(["%s=%s" % (key, value) \
					                             for key, value in self.iteritems() \
								     if not key in ('name',) and value <> '']) })


class Save(Instance):
    __type__ = "instance"
    __name__ = "save"
    __pattern__ = "%s {*args} {**kwargs}" % __name__
    __indent__ = ""
    __default__ = { 'all':'' }
    def __init__(self, name='', *args,  **kwargs):
        self['name'] = name
        for arg in args:
	    self[arg] = ''
	self.update(self.__default__)
        self.update(kwargs)
    def __str__(self):
        return self.__pattern__.format(**{ '*args': " ".join(["%s" % key \
					                             for key, value in self.iteritems() \
								     if not key in ('name',) and value == '']),
	                                   '**kwargs': " ".join([str(value) \
	                                                             for key, value in self.iteritems() \
								     if not key in ('name',) and value <> '']) })


class Parameters(Instance):
    __type__ = "instance"
    __name__ = ".param"
    __pattern__ = "{indent}%s {**parameters}" % __name__
    __maxchar_per_line__ = 85
    __indent__ = ""
    def __init__(self, name='', **parameters):
        self['name'] = name
        self.update(parameters)
    def __str__(self):
        elts = []
        for key, value in self.iteritems():
            if not key in ('name',):
                if not isinstance(value, (float, int)):
                    value = "{%s}"%str(value)
                elts.append("{key}={value}".format(key=key, value=value))
        lines = ['{indent}.param'.format(indent=Parameters.__indent__)]
        for elt in elts:
            if lines[-1].strip() != '':
                lines[-1] += ' '
            lines[-1] += elt.replace(' ', '')
            sumchar  = len(lines[-1])
            if sumchar > Parameters.__maxchar_per_line__:
                for i, c in enumerate( lines[-1][Parameters.__maxchar_per_line__:]):
                    line = lines[-1]
                    if c in ('/', '*', '+', '-'):
                        lines[-1] = line[:Parameters.__maxchar_per_line__+i] + c
                        break
                lines.append('       '+line[Parameters.__maxchar_per_line__+i+1:])
        return '\t\\\n{indent}'.format(indent=Parameters.__indent__).join(lines)




class End(Instance):
    __type__ = "instance"
    __name__ = ".end"
    __pattern__ = "%s" % __name__
    def __init__(self):
        pass
    def __str__(self):
        return self.__pattern__


class Control(Instance):
    __type__ = "instance"
    __name__ = ".control"
    __pattern__ = "%s" % __name__
    def __init__(self):
        pass
    def __str__(self):
        return self.__pattern__


class Endc(Instance):
    __type__ = "instance"
    __name__ = ".endc"
    __pattern__ = "%s" % __name__
    def __init__(self):
        pass
    def __str__(self):
        return self.__pattern__

class Run(Instance):
    __type__ = "instance"
    __name__ = "run"
    __pattern__ = "%s" % __name__
    def __init__(self):
        pass
    def __str__(self):
        return self.__pattern__


class Subckt(Instance):
    __type__ = "instance"
    __name__ = ".subckt"
    __indent__ = ""
    __pattern__ = """{indent}%s {name} {nodes} {**parameters}
{childs}
{indent}.ends {name}""" % __name__
    def __init__(self, name='', nodes=(), childs=(), **parameters):
        self['name'] = name
        self.update(parameters)
        self['childs'] = childs
        self['nodes'] = nodes
    def __str__(self):
        nodes = ''
        if len(self['nodes'])>0:
            nodes = " ".join(self['nodes'])
	else:
	    nodes = ""
	xparameters = tuple((k, v) for k, v in self.iteritems() if k not in ('name', 'childs', 'nodes'))
        if len(xparameters)>0:
            parameters = " ".join([ "%s=%s"%(k,v) for k, v in self.iteritems() if k not in ('name', 'childs', 'nodes') ])
	else:
	    parameters = ''
	for  child in self['childs']:
	    if '__indent__' in dir(child):
	        child.__indent__ = self.__indent__+"  "
        childs = "\n".join( [str(child) for child in self['childs']] )
        return self.__pattern__.format(**{ 'name': self['name'],
	                                   'indent':self.__indent__,
	                                   'nodes': nodes,
					   '**parameters': parameters,
		                           'childs': childs 
					 })


class Model(Instance):
    __type__ = "instance"
    __name__ = ".model"
    __pattern__ = "%s {name} {model} ({**parameters})" % __name__
    __indent__ = ""
    def __init__(self, name='model1', model='', **parameters):
        self['name'] = name
        self['model'] = model
        self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{ 'name': self['name'],
	                                   'model': self['model'],
	                                   '**parameters': " ".join(["%s=%s" % (key, value) \
					                             for key, value in self.iteritems() \
								     if not key in ('name','model')]) })


class Title(Instance):
    __type__ = "instance"
    __name__ = "title"
    __pattern__ = "// ---- {**parameters} ----"
    def __init__(self, name='Title1', **parameters):
        self['name'] = name
	self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{ '**parameters': " ".join([str(value) for key, value in self.iteritems() if not key in ('name',)]) })


class Global(Instance):
    __type__ = "instance"
    __name__ = ".global"
    __pattern__ = "%s {nodes}" % __name__
    __indent__ = ""
    def __init__(self, name='Global1', nodes=()):
        self['nodes'] = nodes
        self['name'] = name
    def __str__(self):
        return self.__pattern__.format(**{ 'nodes': " ".join(self['nodes']) })


class Alter(Instance):
    __type__ = "instance"
    __name__ = "alter"
    __pattern__ = "%s {dev} {*args} {**parameters}" % __name__
    __indent__ = ""
    def __init__(self, dev, *args, **parameters):
        self['name'] = 'alter'
        self['dev'] = dev
	self.update(parameters)
	self['args'] = args
    def __str__(self):
        return self.__pattern__.format(**{ 'dev': self['dev'],
	                                   '*args': " ".join(["%s" % value for value in self['args']]),
	                                   '**parameters': " ".join(["%s=%s" % (key, value) \
					                             for key, value in self.iteritems() \
								     if not key in ('name','dev', 'args')]) })


class Include(Instance):
    __type__ = "instance"
    __name__ = ".include"
    __pattern__ = "%s \"{library}\"" % __name__
    __indent__ = ""
    def __init__(self, name='Include1', path='', library='', **parameters):
        self['name'] = name
        self['path'] = path
        self['library'] = library
        self.update(parameters)
    def __str__(self):
        library = os.path.join(self['path'].strip(), self['library'].strip())
        if not os.path.isfile(library):
            raise exception.Error('Library %s does not exist' % library)        
        return self.__pattern__.format(**{ 'library': library,
	                                    })


class Let(Instance):
    __type__ = "instance"
    __name__ = "let"
    __pattern__ = "%s {param} = {value}" % __name__
    def __init__(self, name='Let1', param='', value=''):
        self['name'] = name
        self['param'] = param
        self['value'] = value
    def __str__(self):
        if isinstance(self['value'], list):
	    value = str(vector(self['value']))
	else:
	    value = self['value']
        return self.__pattern__.format(**{ 'param': self['param'],
	                                   'value': value,
	                                    })
    


class Global(Instance):
    __type__ = "instance"
    __name__ = ".global"
    __pattern__ = "%s {nodes}" % __name__
    def __init__(self, name='Global1', nodes=()):
        self['nodes'] = nodes
        self['name'] = name
    def __str__(self):
        return self.__pattern__.format(**{ 'nodes': " ".join(self['nodes']) })


class Port(Netlist):
    __name__ = "Port"
    __type__ = "netlist"
    def __init__(self, name='Port1', nodes=('1', '2')):
        Netlist.__init__(self)
        self.name = name
        self.nodes = nodes
	subckt1 = []
        subckt1.append( Resistor(name='R1', nodes=('v', '3'), r='50' ))
        subckt1.append( Vsource(name='Vsrc', nodes=('3', '2'), dc=0, ac=1))
        subckt1.append( Vsource(name='V', nodes=('1', 'v'), dc=0, ac=0))
        self.append( Subckt(name=name.lower(), nodes=('1', '2'), childs=subckt1) )
	self.append( Device(name='x%s'%name, model=name.lower(), nodes=nodes) )


class VCCS(Instance):
    __name__ = "g"
    __type__ = "instance"
    __pattern__ = "{indent}%s{name} {nodes} {gain}"% __name__
    __indent__ = ""
    def __init__(self, name='G1', nodes=('in', 'out', 'sensp', 'sensm'), gain=1):
        self['name'] = name
        self['nodes'] = nodes
	self['gain'] = gain
    def __str__(self):
        return self.__pattern__.format(**{ 'indent': self.__indent__,
	                                   'name': self['name'] if self['name'][0].lower()<>self.__name__ else self['name'][1:],
	                                   'nodes': " ".join(self['nodes']),
					   'gain': self['gain'],
					 })

class VCVS(Instance):
    __name__ = "e"
    __type__ = "instance"
    __pattern__ = "{indent}%s{name} {nodes} gain={gain}"% __name__
    __indent__ = ""
    def __init__(self, name='E1', nodes=('in', 'out'), vname="v1", gain=1):
        self['name'] = name
        self['nodes'] = nodes
	self['gain'] = gain
    def __str__(self):
        return self.__pattern__.format(**{ 'indent': self.__indent__,
	                                   'name': self['name'] if self['name'][0].lower()<>self.__name__ else self['name'][1:],
	                                   'nodes': " ".join(self['nodes']),
					   'gain': self['gain'],
					 })


class CCVS(Instance):
    __name__ = "h"
    __type__ = "instance"
    __pattern__ = "{indent}%s{name} {nodes} {vname} {gain}"% __name__
    __indent__ = ""
    def __init__(self, name='H1', nodes=('in', 'out'), vname="v1", gain=1):
        self['name'] = name
        self['nodes'] = nodes
	self['gain'] = gain
	self['vname'] = vname
    def __str__(self):
        return self.__pattern__.format(**{ 'indent': self.__indent__,
	                                   'name': self['name'] if self['name'][0].lower()<>self.__name__ else self['name'][1:],
	                                   'nodes': " ".join(self['nodes']),
					   'gain': self['gain'],
					   'vname': self['vname'],
					 })


class Comment(Instance):
    __type__ = "instance"
    __name__ = "comment"
    __pattern__ = "{indent}* {**parameters}"
    __indent__ = ""
    def __init__(self, name='Comment1', **parameters):
        self['name'] = name
	self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{ 'indent':self.__indent__, '**parameters': " ".join([v for k, v in self.iteritems() if not k in ('name',)]) })
