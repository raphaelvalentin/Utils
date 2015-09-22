from ngspice.syntax import *

class Fracpole(Netlist):
    __name__ = "fracpole"
    __type__ = "model"
    
    def __init__(self, name='fracpole', **parameters):
        # name of the netlist
        self.orderame = name
        # set default parameters
	
	self.order = parameters.get('order', 4)
	self.fac = parameters.get('fac', 20e9)
	self.tc1 = parameters.get('tc1', 0.0039)
        self.rdc = 1.0
        self.ldc = 1e-10
        self.rac = 5.0

        subckt1 = []
	param = { 'rdc': self.rdc, 
	          'ldc': '{self.ldc:.6g}'.format(self=self),
		  'rac': self.rac, 
		  'fac': '{self.fac:.6g}'.format(self=self),
		  'tc1': self.tc1
	        }
	
        subckt1.append( Parameters( l='ldc*3', 
				    g='3.141592653589793*fac*l/(rac*rac)' ) )
        subckt1.append( Comment(s = 'Non Symmetric RL Continued Fraction Expansion') )
	
        for i in xrange(self.order):
	    if i==0:
                subckt1.append( Resistor( name='r%d'%(i), 
                                          nodes=('%d'%(i+1), '%d'%(i+2)), 
        	                          r='rdc', tc1='tc1') )
            else:
                subckt1.append( Resistor( name='r%d'%(i), 
                                          nodes=('%d'%(i+1), '%d'%(i+2)), 
        	                          r='%d/g'%(4*i+1), tc1='tc1') )
            subckt1.append( Inductor( name='l%d'%i, 
                                      nodes=('%d'%(i+2), '%d'%(self.order+2)), 
        	                      l='l/%d'%(4*(i+1)-1)) )
        self.append (Subckt(name=self.orderame, nodes=('1', '%d'%(self.order+2)), childs=subckt1, **param))
