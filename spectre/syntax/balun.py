from spectre.syntax import *

class Balun(Netlist):
    """ A bidirectional balanced-unbalanced Subckt converter
        maps between the unbalanced signal 'd=1' and 'c=2' and the balanced signals
	'p=3' and 'n=4' 
    """
    __name__ = "Balun"
    __type__ = "netlist"
    def __init__(self, name='Balun', nodes=('1', '2', '3', '4'), gain=0.5, ):
        Netlist.__init__(self)
        self.name = name
        self.nodes = nodes
	subckt1 = []
        subckt1.append( Vcvs(name='E1', nodes=('5', '2', '1', '0'), gain=gain))
        subckt1.append( Vsource(name='V1', nodes=('3', '5'), type='dc' ))
        subckt1.append( Cccs(name='F1', nodes=('1', '0'), gain=-gain, probe='V1' ))
        subckt1.append( Resistor(name='R1', nodes=('1', '0'), r='1G' ))
        subckt1.append( Vcvs(name='E2', nodes=('6', '4', '1', '0'), gain=gain ))
        subckt1.append( Vsource(name='V2', nodes=('2', '7'), type='dc' ))
        subckt1.append( Cccs(name='F2', nodes=('1', '0'), gain=-gain, probe='V2' ))
        subckt1.append( Resistor(name='R2', nodes=('7', '6'), r='1u' ))
        self.append( Subckt(name=name, nodes=nodes, childs=subckt1) )
