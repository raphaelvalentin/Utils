from spectre.syntax import *

class SMU2P(Netlist):
    __name__ = "SMU2P"
    __type__ = "netlist"
    def __init__(self, name='SMU2P', nodes=('1', '2'), V1=0, V2=0):
        Netlist.__init__(self)
        self.name = name
        self.nodes = nodes
        self.V1 = V1; self.V2 = V2
        save = dict(V1=nodes[0], V2=nodes[1])
        self.append( Vsource(name='V1', nodes=(nodes[0], '0'), dc=V1, type='dc') )
        save['I1'] = 'V1:2'
        self.append( Vsource(name='V2', nodes=(nodes[1], '0'), dc=V2, type='dc') )
        save['I2'] = 'V2:2'
        self.append( Save(**save) )


class SMU4P(Netlist):
    __name__ = "SMU4P"
    __type__ = "netlist"
    def __init__(self, name='SMU4P', nodes=('1', '2', '3', '4'), V1=0, V2=0, V3=0, V4=0):
        Netlist.__init__(self)
        self.name = name
        self.nodes = nodes
        self.V1 = V1; self.V2 = V2; self.V3 = V3; self.V4 = V4
        self.append( Vsource(name='V1', nodes=(nodes[0], '0'), dc=V1, type='dc') )
        self.append( Vsource(name='V2', nodes=(nodes[1], '0'), dc=V2, type='dc') )
        self.append( Vsource(name='V3', nodes=(nodes[2], '0'), dc=V3, type='dc') )
        self.append( Vsource(name='V4', nodes=(nodes[3], '0'), dc=V4, type='dc'))
        self.append( Save(I1='V1:2', I2="V2:2", I3="V3:2", I4="V4:2", V1=nodes[0], V2=nodes[1], V3=nodes[2], V4=nodes[3]) )


class SMU5P(Netlist):
    __name__ = "SMU5P"
    __type__ = "netlist"
    def __init__(self, name='SMU5P', nodes=('1', '2', '3', '4', '5'), V1=0, V2=0, V3=0, V4=0, V5=0):
        Netlist.__init__(self)
        self.name = name
        self.nodes = nodes
        self.V1 = V1; self.V2 = V2; self.V3 = V3; self.V4 = V4; self.V5 = V5
        self.append( Vsource(name='V1', nodes=(nodes[0], '0'), dc=V1, type='dc') )
        self.append( Vsource(name='V2', nodes=(nodes[1], '0'), dc=V2, type='dc') )
        self.append( Vsource(name='V3', nodes=(nodes[2], '0'), dc=V3, type='dc') )
        self.append( Vsource(name='V4', nodes=(nodes[3], '0'), dc=V4, type='dc'))
        self.append( Vsource(name='V5', nodes=(nodes[4], '0'), dc=V5, type='dc'))
        self.append( Save(I1='V1:2', I2="V2:2", I3="V3:2", I4="V4:2", I5="V5:2", V1=nodes[0], V2=nodes[1], V3=nodes[2], V4=nodes[3], V5=nodes[4]) )

class SMU3P(Netlist):
    __name__ = "SMU3P"
    __type__ = "netlist"
    def __init__(self, name='SMU3P', nodes=('1', '2', '3'), V1=0, V2=0, V3=0, I1=None, I2=None, I3=None):
        Netlist.__init__(self)
        self.name = name
        self.nodes = nodes
        self.V1 = V1; self.V2 = V2; self.V3 = V3;
        save = { 'V1':nodes[0], 'V2':nodes[1], 'V3':nodes[2] }
        if I1 == None:
            self.append( Vsource(name='V1', nodes=(nodes[0], '0'), dc=V1, type='dc') )
            save['I1'] = 'V1:2'
        else:
            self.append( Isource(name='I1', nodes=(nodes[0], '0'), dc=I1, type='dc') )
            save['I1'] = 'I1:2'
        if I2 == None:
            self.append( Vsource(name='V2', nodes=(nodes[1], '0'), dc=V2, type='dc') )
            save['I2'] = 'V2:2'
        else:
            self.append( Isource(name='I2', nodes=(nodes[1], '0'), dc=I2, type='dc') )
            save['I2'] = 'I2:2'
        if I3 == None:
            self.append( Vsource(name='V3', nodes=(nodes[2], '0'), dc=V3, type='dc') )
            save['I3'] = 'V3:2'
        else:
            self.append( Isource(name='I3', nodes=(nodes[2], '0'), dc=I3, type='dc') )
            save['I3'] = 'I3:2'
        self.append( Save(**save) )


class SMU(Netlist):
    __name__ = "SMU"
    __type__ = "netlist"
    def __init__(self, name='SMU', nodes=(), **parameters):
        Netlist.__init__(self)
        self.name = name
        self.nodes = nodes
        save = {}
        for node in nodes:
            if 'V{node}'.format(node=node) in parameters:
                dc = parameters['V{node}'.format(node=node)]
                self.append( Vsource(name='V{node}'.format(node=node), nodes=(node, '0'), dc=dc, type='dc') )
                save['I{node}'.format(node=node)] = 'V{node}:2'.format(node=node)
                save['V{node}'.format(node=node)] = node
            elif 'I{node}'.format(node=node) in parameters:
                dc = parameters['I{node}'.format(node=node)]
                self.append( Isource(name='I{node}'.format(node=node), nodes=(node, '0'), dc=dc, type='dc') )
                save['I{node}'.format(node=node)] = 'I{node}:2'.format(node=node)
                save['V{node}'.format(node=node)] = node
            else:
                self.append( Vsource(name='V{node}'.format(node=node), nodes=(node, '0'), dc=0, type='dc') )
                save['I{node}'.format(node=node)] = 'V{node}:2'.format(node=node)
                save['V{node}'.format(node=node)] = node
        if len(save):   
            self.append( Save(**save) )



