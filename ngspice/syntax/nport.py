from ngspice.syntax import *
from function import flatten
from rawdata import touchstone
from interpolate import interp1d        

__all__ = ['Nport']

class VCVSx(Netlist):
    __name__ = "vcvs"
    __type__ = "instance"
    __indent__ = ""
    def __init__(self, name='E1', nodes=('in', 'out', 'sensp', 'sensm'), gain=complex(0,0), freq=1e9 ):
    
	self.name = name
        self.nodes = nodes
	self.gain = gain
	self.freq = freq
	n1, n2, n3 = newnode(), newnode(), newnode()
	self.e1, self.e2, self.l1 = newname('e'), newname('e'), newname('l')
	self.append( VCVS(name=self.e1, nodes=(nodes[0], n1, nodes[2], nodes[3]), gain=gain.real) )	
	self.append( VCVS(name=self.e2, nodes=(n1, nodes[1], n2, '0'), gain=abs(gain)) )
	self.append( VCCS(name=newname('g'), nodes=('0', n2, nodes[2], nodes[3]), gain=1.0) )
	self.append( Inductor(name=self.l1, nodes=(n2, '0'), l=gain.imag/(2.0*pi*freq)/abs(gain) ) )
	
    def alter(self, gain, freq):
        netlist = Netlist()
	netlist.append( Alter(self.e1, gain=gain.real) )
	netlist.append( Alter(self.e2, gain=abs(gain)) )
	netlist.append( Alter(self.l1, gain.imag/(2.0*pi*freq)/abs(gain)) )
	return netlist


class OnePort(Netlist):
    __name__ = "oneport"
    __type__ = "instance"
    def __init__(self, name='oneport1', nodes=('1', '0'), gain=complex(0, 0), freq=1e9):
	self.name = name
        self.nodes = nodes
	n1, n2 = newnode(), newnode()
	self.append( Resistor(name=newname('r'), nodes=(nodes[0], n1), r=-50) )	
	self.append( Resistor(name=newname('r'), nodes=(n1, n2), r=100) )	
	self.append( VCVS(nodes=(n2, nodes[1], n1, nodes[1]), gain=gain, freq=freq) )
    def alter(self, gain):
        return self[2].alter(gain)
	
	    
class Nport(Netlist):
    # http://analog-innovation.com/CreateS-ParameterSubcircuitsforSpice.pdf
    __name__ = "nport"
    __type__ = "instance"
    def __init__(self, name='nport1', nodes=('1', '0', '2', '0'), file="", freq=None):
	self.name = name
        self.nodes = nodes
	self.file = file
	self.data = touchstone.snp(self.file).read()
	x = []
	for i in xrange(len(nodes)/2):
	    row = []
	    for j in xrange(len(nodes)/2):
	        if freq:
	            freqs = self.data['freq']
		    sij = self.data['s%d%d'%(i+1,j+1)]
		    xsij = interp1d(freqs, sij)(freq)
	            row.append( xsij )
		else:
	            row.append( self.data['s%d%d'%(i+1,j+1)][0] )
	    x.append(row)

	self._ivcvs = []
	n1 = [newnode() for i in xrange(len(nodes)/2)]
	for i in xrange(len(nodes)/2):
	    self.append( Resistor(name=newname('r'), nodes=(nodes[i*2], n1[i]), r=-50) )	
	    n2 = [newnode() for _i in xrange(len(nodes)/2)] + [nodes[1]]
	    self.append( Resistor(name=newname('r'), nodes=(n1[i], n2[0]), r=100) )
	    for j in xrange(len(nodes)/2):
	        self.append( VCVSx(nodes=(n2[j], n2[j+1], n1[j], nodes[-1]), gain=x[i][j]) )
		self._ivcvs.append( len(self)-1 )
    def alter(self, freq):
	x = []
	for i in xrange(len(self.nodes)/2):
	    row = []
	    for j in xrange(len(self.nodes)/2):
	        freqs = self.data['freq']
		sij = self.data['s%d%d'%(i+1,j+1)]
		xsij = interp1d(freqs, sij)(freq)
	        row.append( xsij )
	    x.append(row)
        y = list(flatten(x))
        netlist = Netlist()
        for i, k in enumerate(self._ivcvs):
	    netlist.append( self[k].alter(y[i], freq) )
        return netlist
    
        
