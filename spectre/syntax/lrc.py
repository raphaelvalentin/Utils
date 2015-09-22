
class LCR(Netlist):
    __name__ = "LCR"
    __type__ = "netlist"
    def __init__(self, name='LCR', nodes=('1', '2'), V1=0):
        Netlist.__init__(self)
        self.name = name
        self.nodes = nodes
        self.V1 = V1
        self.append( Vsource(name='VLCR', nodes=(nodes[0], nodes[1]), dc=V1, type='sine', mag=1, phase=0) )
        self.append( Save(name='Save', IAC='VLCR:2') )
