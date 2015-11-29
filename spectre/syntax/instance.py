import os
from spectre.syntax import *

class Device(Instance):
    __name__ = "device"
    __type__ = "instance"
    __pattern__ = "{indent}{name} {nodes} {model} {**parameters}"
    __indent__ = ""
    def __init__(self, name='X1', nodes=(), model='', **parameters):
        self['name'] = name
        self['nodes'] = nodes
        self['model'] = model
      	self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{ 'indent': self.__indent__,
	                                   'name': self['name'],
	                                   'nodes': "(%s)"%" ".join(self['nodes']),
					   'model': self['model'],
		                           '**parameters': " ".join(["%s=%s" % (k, v) \
					                             for k, v in self.iteritems() \
					                             if k not in ('name', 'nodes', 'model') and k[0]<>'_']) 
					 })

class Resistor(Device):
    __name__ = "resistor"
    __type__ = "instance"
    __indent__ = ""
    def __init__(self, name='R1', nodes=('in', 'out'), r=100, **parameters):
	Device.__init__(self, name=name, nodes=nodes, model='resistor', r=r, **parameters)

class Inductor(Device):
    __name__ = "inductor"
    __type__ = "instance"
    __indent__ = ""
    def __init__(self, name='L1', nodes=('in', 'out'), l=1e-9, **parameters):
	Device.__init__(self, name=name, nodes=nodes, model='inductor', l=l, **parameters)

class MutualInductor(Device):
    __name__ = "mutual_inductor"
    __type__ = "instance"
    __pattern__ = "{indent}{name} %s {**parameters}" % __name__
    __indent__ = ""
    def __init__(self, name='ML1', coupling=0.5, ind1='l1', ind2='l2'):
        self['name'] = name
	self['coupling'] = coupling
	self['ind1'] = ind1
	self['ind2'] = ind2
    def __str__(self):
        if self['coupling']<>0:
            return self.__pattern__.format(**{ 'name': self['name'],
	                                       'indent':self.__indent__,
    		                               '**parameters': " ".join(["%s=%s" % (k, v) \
					                                 for k, v in self.iteritems() \
							    	         if not k in ('name',)]) 
					     })
        return '// ' + self.__pattern__.format(**{ 'name': self['name'],
    		                                   '**parameters': " ".join(["%s=%s" % (k, v) \
					                                     for k, v in self.iteritems() \
							    	             if not k in ('name',)]) 
					     })

class Capacitor(Device):
    __name__ = "capacitor"
    __type__ = "instance"
    __indent__ = ""
    def __init__(self, name='C1', nodes=('in', 'out'), c=1e-12, **parameters):
	Device.__init__(self, name=name, nodes=nodes, model='capacitor', c=c, **parameters)

class Vsource(Instance):
    __name__ = "vsource"
    __type__ = "instance"
    __pattern__ = "{indent}{name} ({nodes}) %s {**parameters}" % __name__
    __indent__ = ""
    def __init__(self, name='V1', nodes=(), **parameters):
        self['name'] = name
	self['nodes'] = nodes
	self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{ 'name': self['name'],
	                                   'indent':self.__indent__,
	                                   'nodes': " ".join(self['nodes']),
		                           '**parameters': " ".join(["%s=%s" % (k, v) \
					                             for k, v in self.iteritems() \
								     if not k in ('name', 'nodes')]) 
					 })

class Isource(Instance):
    __name__ = "isource"
    __type__ = "instance"
    __pattern__ = "{indent}{name} ({nodes}) %s {**parameters}" % __name__
    __indent__ = ""
    def __init__(self, name='I1', nodes=(), **parameters):
        self['name'] = name
	self['nodes'] = nodes
	self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{ 'name': self['name'],
	                                   'indent':self.__indent__,
	                                   'nodes': " ".join(self['nodes']),
		                           '**parameters': " ".join(["%s=%s" % (k, v) \
					                             for k, v in self.iteritems() \
								     if not k in ('name', 'nodes')]) 
					 })

class Port(Instance):
    __type__ = "instance"
    __name__ = "port"
    __pattern__ = "{indent}{name} ({nodes}) %s {**parameters}" % __name__
    __default__ = { 'num':1, 'r':50, 'type':'sine', 'x':0 }
    __indent__ = ""
    def __init__(self, name='', nodes=(), **parameters):
        self['name'] = name
        self['nodes'] = nodes
        self.update(self.__default__)
        self.update(parameters)
	self.__default__['num'] += 1
    def __str__(self):
        return self.__pattern__.format(**{ 'name': self['name'],
	                                   'indent':self.__indent__,
	                                   'nodes': " ".join(self['nodes']),
		                           '**parameters': " ".join(["%s=%s" % (k, v) \
					                             for k, v in self.iteritems() \
								     if not k in ('name', 'nodes')]) 
					 })

class Vcvs(Instance):
    __name__ = "vcvs"
    __type__ = "instance"
    __pattern__ = "{indent}{name} ({nodes}) %s {**parameters}" % __name__
    __indent__ = ""
    def __init__(self, name='E1', nodes=(), **parameters):
        self['name'] = name
	self['nodes'] = nodes
	self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{ 'name': self['name'],
	                                   'indent':self.__indent__,
	                                   'nodes': " ".join(self['nodes']),
		                           '**parameters': " ".join(["%s=%s" % (k, v) \
					                             for k, v in self.iteritems() \
								     if not k in ('name', 'nodes')]) 
					 })

class Cccs(Instance):
    __name__ = "cccs"
    __type__ = "instance"
    __pattern__ = "{indent}{name} ({nodes}) %s {**parameters}" % __name__
    __indent__ = ""
    def __init__(self, name='F1', nodes=(), **parameters):
        self['name'] = name
	self['nodes'] = nodes
	self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{ 'name': self['name'],
	                                   'indent':self.__indent__,
	                                   'nodes': " ".join(self['nodes']),
		                           '**parameters': " ".join(["%s=%s" % (k, v) \
					                             for k, v in self.iteritems() \
								     if not k in ('name', 'nodes')]) 
					 })

class Options(Instance):
    __name__ = "options"
    __type__ = "instance"
    __pattern__ = "{indent}{name} %s {**parameters}" % __name__
    __indent__ = ""
    __default__ = { 'save':'allpub', 'reltol':1e-4, 'vabstol':1e-7, 'iabstol':1e-13, 
           'temp':27, 'tnom':27, 'scalem':1.0, 'scale':1.0, 'gmin':1e-18, 
           'rforce':1, 'maxnotes':5, 'maxwarns':5, 'digits':10, 'cols':80,  
           'pivrel':1e-6, 'sensfile':"\"sens.output\"", 'checklimitdest':"\"psf\"", }
    def __init__(self, name='simulatorOptions', default=__default__, **parameters):
        self['name'] = name
        self.update(default)
        self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{ 'name': self['name'],
	                                   'indent':self.__indent__,
	                                   '**parameters': " ".join(["%s=%s" % (key, value) \
					                             for key, value in self.iteritems() \
								     if not key in ('name',)]) })

class Save(Instance):
    __type__ = "instance"
    __name__ = "save"
    __pattern__ = "%s {**parameters}" % __name__
    __indent__ = ""
    def __init__(self, name='', **parameters):
        self['name'] = name
        self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{ '**parameters': " ".join([str(value) \
	                                                             for key, value in self.iteritems() \
								     if not key in ('name',)]) })

class Parameters(Instance):
    __type__ = "instance"
    __name__ = "parameters"
    __pattern__ = "{indent}%s {**parameters}" % __name__
    __maxchar_per_line__ = 55
    __indent__ = ""
    def __init__(self, name='', **parameters):
        self['name'] = name
        self.update(parameters)
    def __str__(self):
        p = ["{key}={value}".format(key=key, value=value) \
		for key, value in self.iteritems() \
		if not key in ('name',)]
	s = ""
	sumchar = 0
	for elt in p:
	    s += elt + " "
	    sumchar += len(elt)
	    if sumchar>Parameters.__maxchar_per_line__:
	         s += "\\\n           " + self.__indent__
		 sumchar = 0
        return self.__pattern__.format(**{ 'indent':self.__indent__, '**parameters': s })


class Subckt(Instance):
    __type__ = "instance"
    __name__ = "subckt"
    __indent__ = ""
    __pattern__ = """{indent}subckt {name} {nodes}
{**parameters}{childs}
{indent}ends {name}"""
    def __init__(self, name='', nodes=(), childs=(), **parameters):
        self['name'] = name
        self.update(parameters)
        self['childs'] = childs
        self['nodes'] = nodes
    def __str__(self):
        nodes = ''
        if len(self['nodes'])>0:
            nodes = "(%s)" % (" ".join(self['nodes']))
	else:
	    nodes = ''
	xparameters = tuple((k, v) for k, v in self.iteritems() if k not in ('name', 'childs', 'nodes'))
        if len(xparameters)>0:
            parameters = self.__indent__+"  "+str(Parameters(**dict(xparameters))) + '\n'
	else:
	    parameters = ''
	for  child in self['childs']:
	    child.__indent__ = self.__indent__+"  "
        childs = "\n".join( [str(child) for child in self['childs']] )
        return self.__pattern__.format(**{ 'name': self['name'],
	                                   'indent':self.__indent__,
	                                   'nodes': nodes,
					   '**parameters': parameters,
		                           'childs': childs 
					 })


class Include(Instance):
    __type__ = "instance"
    __name__ = "include"
    __pattern__ = "%s \"{library}\" {**parameters}" % __name__
    __indent__ = ""
    def __init__(self, name='Include1', path='', library='', **parameters):
        self['name'] = name
        self['path'] = path
        self['library'] = library
        self.update(parameters)
    def __str__(self):
        library = os.path.join(self['path'].strip(), self['library'].strip())
        if not os.path.isfile(library):
            raise Exception('Library \'%s\' does not exist' % library)        
        return self.__pattern__.format(**{ 'library': library,
	                                   '**parameters': " ".join(["%s=%s" % (k, v) \
					                             for k, v in self.iteritems() \
								     if not k in ('name', 'path', 'library', )]) })


class Model(Instance):
    __type__ = "instance"
    __name__ = "model"
    __pattern__ = "%s {name} {model} {**parameters}" % __name__
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
           
class Comment(Instance):
    __type__ = "instance"
    __name__ = "comment"
    __pattern__ = "{indent}// {**parameters}"
    __indent__ = ""
    def __init__(self, name='Comment1', **parameters):
        self['name'] = name
	self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{ 'indent':self.__indent__, '**parameters': " ".join([v for k, v in self.iteritems() if not k in ('name',)]) })

class Section(Instance):
    __type__ = "instance"
    __name__ = "section"
    __pattern__ = "%s {name}\n {section}\n endsection {name}" % __name__
    __indent__ = ""
    def __init__(self, name='Section1', *section):
        self['name'] = name
	self['section'] = section
    def __str__(self):
        return self.__pattern__.format(**{ 'name': self['name'],
	                                   'section':  "\n".join([str(elt) for elt in self['section']])
					 })

class Statistic(Instance):
    __type__ = "instance"
    __name__ = "statistics"
    __pattern__ = "%s {{\n{statistics}\n}}" % __name__
    __indent__ = ""
    def __init__(self, *statistics):
	self['statistics'] = statistics
    def __str__(self):
        return self.__pattern__.format(**{ 'statistics':  "\n".join([str(elt) for elt in self['statistics']])})

class Mismatch(Instance):
    __type__ = "instance"
    __name__ = "mismatch"
    __pattern__ = "%s {mismatch}" % __name__
    __indent__ = ""
    def __init__(self, *vary):
	self['vary'] = vary
    def __str__(self):
	mismatch = "{\n" 
	for vary in self['vary']:
	    mismatch += str(vary) + "\n"
	mismatch += "}"
        return self.__pattern__.format(**{ 'mismatch': mismatch,
					 })

class Process(Instance):
    __type__ = "instance"
    __name__ = "process"
    __pattern__ = "%s {process}" % __name__
    __indent__ = ""
    def __init__(self, *vary):
	self['vary'] = vary
    def __str__(self):
	process = "{\n" 
	for vary in self['vary']:
	    process += str(vary) + "\n"
	process += "}"
        return self.__pattern__.format(**{ 'process': process,
					 })

class Vary(Instance):
    __type__ = "instance"
    __name__ = "vary"
    __pattern__ = "%s {name} {**vary} " % __name__
    __indent__ = ""
    def __init__(self, name='parameter', **parameters):
        self['name'] = name
	self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{ 'name':self['name'], 
	                                   '**vary': " ".join(['{key}={value}'.format(key=str(key), value=str(value)) for key, value in self.iteritems() if not key in ('name',)]) 
					})

class Title(Instance):
    __type__ = "instance"
    __name__ = "title"
    __pattern__ = "// ---- {**parameters} ----"
    __indent__ = ""
    def __init__(self, name='Title1', **parameters):
        self['name'] = name
	self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{ '**parameters': " ".join([str(value) for key, value in self.iteritems() if not key in ('name',)]) })

class Simulator(Instance):
    __type__ = "instance"
    __name__ = "simulator"
    __pattern__ = "%s {**parameters}" % __name__
    __indent__ = ""
    def __init__(self, name='', **parameters):
        self['name'] = name
        self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{ '**parameters': " ".join(["%s=%s" % (k, v) \
					                             for k, v in self.iteritems() \
								     if not k in ('name', )]) })

class Global(Instance):
    __type__ = "instance"
    __name__ = "global"
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
    __pattern__ = "{name} %s {**parameters}" % __name__
    __indent__ = ""
    def __init__(self, name='', dev='', param='', value=''):
        self['name'] = name
        self['dev'] = dev
        self['param'] = param
        self['value'] = value
    def __str__(self):
        return self.__pattern__.format(**{ 'name': self['name'],
		                           '**parameters': " ".join(["%s=%s" % (k, v) \
					                             for k, v in self.iteritems() \
								     if not k in ('name', )]) 
					 })

class Text(Instance):
    __type__ = "instance"
    __name__ = "text"
    __indent__ = ""
    def __init__(self, text):
        self.text = str(text)
    def __str__(self):
        return self.text

class AlterGroup(Instance):
    __type__ = "instance"
    __name__ = "altergroup"
    __pattern__ = "{name} %s {childs}" % __name__
    __indent__ = ""
    i = 0
    def __init__(self, name='altergroup', childs=()):
        self['name'] = name
        self['childs'] = childs
	AlterGroup.i+=1
#	self.restrict = ('save', 'include')
    def __str__(self):
	childs = ''
	if self['childs']:
	    childs = "{\n" 
	    for child in self['childs']:
	        childs += str(child) + "\n"
	    childs += "}"
        return self.__pattern__.format(**{ 'name': "%s%d"%(self['name'],AlterGroup.i),
		                           'childs': childs,
					 })

class Nport(Device):
    __type__='instance'
    __name__='nport'
    __default__ = {'datafmt':'touchstone', 'thermalnoise':'yes', 
                   'dcextrap':'constant', 'hfextrap':'constant', 
		   'passivity':'no', 'pabstol':1e-06}
    __indent__ = ""
    def __init__(self, name='NPORT1', nodes=('in', 'out'), file='data.s2p', **parameters): 
        __parameters__ = dict(self.__default__)
	__parameters__.update(parameters)
        Device.__init__(self, name=name, nodes=nodes, model='nport', file="\"%s\""%file, **__parameters__)

class Hdl(Instance):
    __type__='instance'
    __name__='ahdl_include'
    __pattern__ = "%s \"{filename}\"" % __name__
    __indent__ = ""
    def __init__(self, name='hdl1', path='', filename=''):
        self['name'] = name
        self['path'] = path
        self['filename'] = filename
    def __str__(self):
        filename = os.path.join(self['path'].strip(), self['filename'].strip())
        if not os.path.isfile(filename):
            raise Exception('Filename \'%s\' does not exist' % filename)        
        return self.__pattern__.format(**{ 'filename': filename })


################## VERBOSE

class Info(Instance):
    __type__ = "instance"
    __name__ = "info"
    __pattern__ = "{name} %s {**parameters}" % __name__
    __default__ = {'where':'rawfile'}
    __indent__ = ""
    def __init__(self, name='sp1', **parameters):
        self['name']	= name
	self.update(self.__default__)
	self.update(parameters)
    def __str__(self):
        return self.__pattern__.format(**{ 'name': self['name'],
	                                   '**parameters': " ".join(["%s=%s" % (key, value) \
					                             for key, value in self.iteritems() \
								     if not key in ('name',)])
	                                 })

class Verbose(Netlist):
    __name__ = "verbose"
    __type__ = "netlist"
    __indent__ = ""
    def __init__(self, name='Verbose', **parameters):
        self.name = name
        self.models = parameters.get('models', True)
        self.inst = parameters.get('inst', True)
        self.output = parameters.get('output', True)
        self.parameters = parameters.get('parameters', True)
        self.primitives = parameters.get('primitives', True)
        self.subckts = parameters.get('subckts', True)
	if self.models:
	    self.append( Info(name='modelParameter', what='models') )
	if self.inst:
	    self.append( Info(name='element', what='inst') )
	if self.output:
	    self.append( Info(name='outputParameter', what='output') )
	if self.parameters:
	    self.append( Info(name='designParamVals', what='parameters') )
	if self.primitives:
	    self.append( Info(name='primitives', what='primitives') )
	if self.subckts:
	    self.append( Info(name='subckts', what='subckts') )



################### NEW DEVICES
        
class Tbias(Netlist):
    __name__ = "tbias"
    __type__ = "netlist"
    __indent__ = ""
    def __init__(self, name='Tbias', **parameters):
        self.name = name
        self.c = parameters.get('c', 1)
        self.l = parameters.get('l', 1)
        dcblock = Device(name='DCblock', nodes=('input', 'output'), model='capacitor', c='c') 
        acblock = Device(name='ACblock', nodes=('dc', 'output'), model='inductor', l='l') 
        self.append( Subckt(name=name, nodes=('input', 'dc', 'output'), c=self.c, l=self.l, childs=(dcblock, acblock)) )


class ACBlock(Device):
    __name__ = "acblock"
    __type__ = "device"
    __indent__ = ""
    def __init__(self, name='ACBlock1', nodes=('1', '2'), l=1):
        Device.__init__(self, name=name, nodes=nodes, model='inductor', l=l)

class DCBlock(Device):
    __name__ = "dcblock"
    __type__ = "device"
    __indent__ = ""
    def __init__(self, name='DCBlock1', nodes=('1', '2'), c=1):
        Device.__init__(self, name=name, nodes=nodes, model='capacitor', c=c)



class Z(Instance):
    """ High Impedance
    """
    __type__ = "instance"
    __name__ = "z"
    dc = True
    rf = True
    def __init__(self, dc=True, sp=True):
        self['dc'] = dc
	self['sp'] = sp


