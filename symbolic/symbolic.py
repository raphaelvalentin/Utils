#!/usr/bin/env python

from __future__ import division

__all__ = ['Symbol', 'sqrt', 'cos', 'sin', 'tan', 'exp', 'atan', 'log10', 'log']

class Symbol(str):
    spacing = 0

    def __init__(self, expr):
        self.expr = expr
        self.bracket = False

    def setBracket(self):
        self.bracket = True

    def __add__(self, obj):
        if isinstance(obj, Symbol) and self.expr == obj.expr:
            return Symbol(('*', 2.0, self))
        return Symbol(('+', self, obj))

    def __radd__(self, obj):
        return Symbol(('+', obj, self))

    def __mul__(self, obj):
        if isinstance(obj, (float, int)) and obj==1.0:
            return self
        if isinstance(obj, (float, int)) and obj==0.0:
            return 0.0
        if len(self.expr) in (2, 3) and self.expr[0] in ('+', '-'): 
            self.setBracket()
        if isinstance(obj, Symbol) and len(obj.expr) in (2, 3) and obj.expr[0] in ('+', '-'): 
            obj.setBracket()
        return Symbol(('*', self, obj))

    def __rmul__(self, obj):
        if isinstance(obj, (float, int)) and obj==1.0:
            return self
        if isinstance(obj, (float, int)) and obj==0.0:
            return 0.0
        if len(self.expr) in (2, 3) and self.expr[0] in ('+', '-'): 
            self.setBracket()
        if isinstance(obj, Symbol) and len(obj.expr) in (2, 3) and obj.expr[0] in ('+', '-'): 
            obj.setBracket()
        return Symbol(('*', obj, self))

    def __div__(self, obj):
        if isinstance(obj, (float, int)) and obj==1.0:
            return self
        if isinstance(obj, Symbol) and self.expr == obj.expr:
            return 1.0
        if isinstance(obj, (float, int)) and self.expr == obj:
            return 1.0

        if len(self.expr) in (2, 3) and self.expr[0] in ('+', '-'): 
            self.setBracket()
        if isinstance(obj, Symbol) and len(obj.expr) in (2, 3) and obj.expr[0] in ('+', '-', '*', '/'): 
            obj.setBracket()
        return Symbol(('/', self, obj))

    def __rdiv__(self, obj):
        if isinstance(obj, Symbol) and self.expr == obj.expr:
            return 1.0
        if isinstance(obj, (float, int)) and self.expr == obj:
            return 1.0
        if len(self.expr) in (2, 3) and self.expr[0] in ('+', '-', '*', '/'): 
            self.setBracket()
        if isinstance(obj, Symbol) and len(obj.expr) in (2, 3) and obj.expr[0] in ('+', '-'): 
            obj.setBracket()
        return Symbol(('/', obj, self))

    def __sub__(self, obj):
        if isinstance(obj, Symbol) and len(obj.expr) in (2, 3) and obj.expr[0] in ('+', '-'): 
            obj.setBracket()
        return Symbol(('-', self, obj))

    def __rsub__(self, obj):
        if len(self.expr) in (2, 3) and self.expr[0] in ('+', '-'): 
            self.setBracket()
        return Symbol(('-', obj, self))

    def __neg__(self):
        if len(self.expr) == 2 and self.expr[0] in ('+', '-'): 
            if self.expr[0] == '+':
                self.expr = tuple(['-', Symbol(('-', self.expr[1]))])
            elif self.expr[0] == '-':
                self.expr = tuple(['+', Symbol(('-', self.expr[1]))])
        elif len(self.expr) == 3 and self.expr[0] in ('+', '-'): 
            if self.expr[0] == '+':
                self.expr = tuple(['-', Symbol(('-', self.expr[1]), self.expr[2])])
            elif self.expr[0] == '-':
                self.expr = tuple(['+', Symbol(('-', self.expr[1]), self.expr[2])])
        return self

    def __pos__(self):
        return self

    def __pow__(self, obj):
        if isinstance(obj, (float, int)) and obj==1.0:
            return self 
        if isinstance(obj, (float, int)) and obj==0.0:
            return 1 
        if len(self.expr) in (2, 3) and self.expr[0] in ('+', '-', '*', '/', '**'): 
            self.setBracket()
        if isinstance(obj, Symbol) and len(obj.expr) in (2, 3) and obj.expr[0] in ('+', '-', '*', '/', '**'): 
            obj.setBracket()
        return Symbol(('**', self, obj))

    def __rpow__(self, obj):
        if len(self.expr) in (2, 3) and self.expr[0] in ('+', '-', '*', '/', '**'): 
            self.setBracket()
        if isinstance(obj, Symbol) and len(obj.expr) in (2, 3) and obj.expr[0] in ('+', '-', '*', '/', '**'): 
            obj.setBracket()
        return Symbol(('**', obj, self))

    def __str__(self):

        if len(self.expr) == 1:
            s = str(self.expr[0])

        elif len(self.expr) == 2:
            op, a = self.expr
            if self.bracket:
                s = "(%s%s)" % (op, str(a))
            else:
                s = "%s%s" % (op, str(a))

        elif len(self.expr) == 3:
            op, a, b = self.expr
            if self.bracket:
                s = "(%s%s%s%s%s)" % (str(a),' '*Symbol.spacing, op,' '*Symbol.spacing,str(b))
            else:
                s = "%s%s%s%s%s" % (str(a),' '*Symbol.spacing, op,' '*Symbol.spacing,str(b))
        return s

    def __repr__(self):
        return self.__str__()



import math    
def sqrt(obj):
    if isinstance(obj, Symbol):
        return Symbol('sqrt({a})'.format(a=obj))
    return math.sqrt(obj)

def cos(obj):
    if isinstance(obj, Symbol):
        return Symbol('cos({a})'.format(a=obj))
    return math.cos(obj)

def sin(obj):
    if isinstance(obj, Symbol):
        return Symbol('sin({a})'.format(a=obj))
    return math.sin(obj)

def tan(obj):
    if isinstance(obj, Symbol):
        return Symbol('tan({a})'.format(a=obj))
    return math.tan(obj)

def exp(obj):
    if isinstance(obj, Symbol):
        return Symbol('exp({a})'.format(a=obj))
    return math.exp(obj)

def atan(obj):
    if isinstance(obj, Symbol):
        return Symbol('atan({a})'.format(a=obj))
    return math.atan(obj)

def log10(obj):
    if isinstance(obj, Symbol):
        return Symbol('log10({a})'.format(a=obj))
    return math.atan(obj)

def log(obj):
    if isinstance(obj, Symbol):
        return Symbol('log({a})'.format(a=obj))
    return math.atan(obj)

   
if __name__ == '__main__': 


    from random import randint, random
    def pick_var():
        var = ['x', 'y', 'z', 1., 2., 3.]
        i = randint(0, len(var)-1)
        return var[i]

    def pick_op():
        op = ['+', '-', '*', '/', '**']
        i = randint(0, len(op)-1)
        return op[i]



    def isbracket():
        i = random()<0.3
        return i

    def bench():
        expr = ''
        a = pick_var()
        b = pick_var()
        op = pick_op()
        if isbracket():
            expr="(%s%s%s)"%(a,op,b)
        else:
            expr="%s%s%s"%(a,op,b)
        for i in xrange(10):
            if random()<0.5:
                a = expr
                b = pick_var()
            else:
                b = expr
                a = pick_var()
            op = pick_op()
            if isbracket():
                expr="(%s%s%s)"%(a,op,b)
            else:
                expr="%s%s%s"%(a,op,b)
        return expr
    
    
    def test(expr, i):

        from symbolic import Symbol
    
        x = Symbol('x')
        y = Symbol('y')
        z = Symbol('z')
        try:
            f1 =  eval(expr)
            x1 = random()
            y1 = random()
            z1 = random()
            x, y, z = x1, y1, z1
            res1 = eval(str(f1))
        except:
            res1 = None
    
    
        from sympy import Symbol
        
        x = Symbol('x')
        y = Symbol('y')
        z = Symbol('z')
        try:
            f2 =  eval(expr)
            x, y, z = x1, y1, z1
            res2 = eval(str(f2))
        except:
            res2 = None
    
        if res1<>res2 and res1<>None and res2<>None and res2 <> 0 and abs(res1-res2)>1e-6*abs(res2):
            print expr
            print f1
            print res1
            print f2
            print res2
            raise Exception()
    
          
    for i in xrange(1000):
        test( bench(), i )




