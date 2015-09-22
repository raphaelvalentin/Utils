from spectre.syntax import *

class Transformer(Netlist):
    """
    3 ports Transformer : primary winding nodes=('1', '2'), secondary winding nodes=('3', '4', '5'). The node '4' is the CT node.
    The model include 3 inductances, 3 series resistances and 3 parallel coupling capacitances.
    Per default: l1 = l2 = l3 = 1n, r1 = r2 = r3 = 1m, c1 = c2 = c3 = 1f
    """

    __name__ = "transformer"
    __type__ = "netlist"
    
    def __init__(self, name='transformer', nodes=('1', '2', '3', '4', '5'), **parameters):
        # name of the netlist
        self.name = name
	self.nodes = nodes
        # set default parameters
	self.l1 = parameters.get('l1', 1e-9)
	self.l2 = parameters.get('l2', 1e-9)
	self.l3 = parameters.get('l3', 1e-9)
	self.r1 = parameters.get('r1', 1e-3)
	self.r2 = parameters.get('r2', 1e-3)
	self.r3 = parameters.get('r3', 1e-3)
	self.k12 = parameters.get('k1', 0.9)
	self.k13 = parameters.get('k2', 0.9)
	self.k23 = parameters.get('k3', 0.9)
	self.c1 = parameters.get('c1', 1e-15)
	self.c2 = parameters.get('c2', 1e-15)
	self.c3 = parameters.get('c3', 1e-15)
	
        subckt1 = []
	# primary
	subckt1.append( Resistor(name='R1', nodes=('1', '6'), r=self.r1) )
	subckt1.append( Inductor(name='L1', nodes=('6', '2'), l=self.l1) )
	
	# secondary
	subckt1.append( Resistor(name='R2', nodes=('3', '7'), r=self.r2) )
	subckt1.append( Inductor(name='L2', nodes=('7', '4'), l=self.l2) )
	subckt1.append( Inductor(name='L3', nodes=('4', '8'), l=self.l3) )
	subckt1.append( Resistor(name='R3', nodes=('8', '5'), r=self.r3) )
	
	# coupling
	subckt1.append( MutualInductor(name='M12', coupling=self.k12, ind1='L1', ind2='L2') )
	subckt1.append( MutualInductor(name='M13', coupling=self.k13, ind1='L1', ind2='L3') )
	subckt1.append( MutualInductor(name='M23', coupling=self.k23, ind1='L2', ind2='L3') )

	# cap
	subckt1.append( Capacitor(name='C1', nodes=('1', '2'), c=self.c1) )
	subckt1.append( Capacitor(name='C2', nodes=('3', '4'), c=self.c2) )
	subckt1.append( Capacitor(name='C3', nodes=('4', '5'), c=self.c3) )
	
	self.append (Subckt(name=self.name, nodes=nodes, childs=subckt1))
