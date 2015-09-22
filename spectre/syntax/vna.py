"""
 VNA 1/2 Ports including TeeBias
"""

from spectre.syntax import *
from function import *

@deprecated	
class VNA1P(Netlist):
    __name__ = "VNA1P"
    __type__ = "netlist"
    ports = '[p1]'
    def __init__(self, name='VNA1P', nodes=('rf1', 'dc1',)):
        Netlist.__init__(self)
        self.name = name
        self.nodes = nodes
        self.append( Port(name='p1', nodes=('1', '0'), num=1, type='sine') )
        self.append( Tbias(name='tbias') )
        self.append( Device(name='tbias1', nodes=('1', 'plus', 'In'), model='tbias') )

@deprecated	
class VNA2P(Netlist):
    __name__ = "VNA2P"
    __type__ = "netlist"
    ports = '[p1, p2]'
    def __init__(self, name='VNA2P', nodes=('rf1', 'dc1', 'rf2', 'dc2')):
        Netlist.__init__(self)
        self.name = name
        self.nodes = nodes
        self.append( Port(name='p1', nodes=('p1', '0'), num=1, type='sine') )
        self.append( Port(name='p2', nodes=('p2', '0'), num=2, type='sine') )
        self.append( Tbias(name='tbias') )
        self.append( Device(name='tbias1', nodes=('p1', nodes[1], nodes[0]), model='tbias') )
        self.append( Device(name='tbias2', nodes=('p2', nodes[3], nodes[2]), model='tbias') )

class VNA2Px(Netlist):
    __name__ = "VNA2P"
    __type__ = "netlist"
    ports = '[p1, p2]'
    def __init__(self, name='VNA', port1=('rf1','0'), port2=('rf2','0'), dc=()):
        Netlist.__init__(self)
        self.name = name
	if len(port1)==3 or len(port2)==3:
	    self.append( Tbias(name='tbias') )
	if len(port1)==3:
	    self.append( Port(name='p1', nodes=('p1', port1[1]), num=1, type='sine') )
	    self.append( Device(name='tbias1', nodes=('p1', port1[2], port1[0]), model='tbias') )
	else:
	    self.append( Port(name='p1', nodes=(port1[0], port1[1]), num=1, type='sine') )
	if len(port2)==3:
            self.append( Port(name='p2', nodes=('p2', port1[1]), num=2, type='sine') )
            self.append( Device(name='tbias2', nodes=('p2', port2[2], port2[0]), model='tbias') )
	else:
            self.append( Port(name='p2', nodes=(port2[0], port1[1]), num=2, type='sine') )

class VNA1Px(Netlist):
    __name__ = "VNA1P"
    __type__ = "netlist"
    ports = '[p1]'
    def __init__(self, name='VNA', port1=('rf1','0')):
        Netlist.__init__(self)
        self.name = name
	if len(port1)==3:
	    self.append( Tbias(name='tbias') )
	if len(port1)==3:
	    self.append( Port(name='p1', nodes=('p1', port1[1]), num=1, type='sine') )
	    self.append( Device(name='tbias1', nodes=('p1', port1[2], port1[0]), model='tbias') )
	else:
	    self.append( Port(name='p1', nodes=(port1[0], port1[1]), num=1, type='sine') )


class VNA(Netlist):
    __name__ = "VNA"
    __type__ = "netlist"
    def __init__(self, name='VNA', **parameters):
        self.name = name
	for i, (name, nodes) in enumerate(parameters.iteritems()):
	    if isinstance(nodes, tuple) and len(nodes)==2 and isinstance(nodes[0], str) and isinstance(nodes[1], str):
   	        self.append( Port(name=name, nodes=nodes, num=i+1, type='sine') )

class VNA(Netlist):
    __name__ = "VNA"
    __type__ = "netlist"
    def __init__(self, name='VNA', **parameters):
        self.name = name
	for i, (name, nodes) in enumerate(parameters.iteritems()):
	    if isinstance(nodes, tuple) and len(nodes)==2 and isinstance(nodes[0], str) and isinstance(nodes[1], str):
   	        self.append( Port(name=name, nodes=nodes, num=i+1, type='sine') )
	        
