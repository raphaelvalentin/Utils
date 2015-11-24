from libarray import *
from functions import *
import sys
from collections import OrderedDict

__all__ = ['base']

class base(list):
    def __init__(self, filename=None, mode='r'):
        list.__init__(self)
        self.filename = filename
        self.mode = mode
    def read(self):
        if not self.mode in ('r',):
            raise Exception('File not open for reading')
        f = open(self.filename, 'r')
        isBEGIN = False
        isDATA = False
        isVAR = False
        keys = []
        indxline = 0
        while 1:
            indxline +=1
            line = f.readline()
            if line == '': break
            line = line.strip()
            if line == '':
                pass
            elif 'BEGIN_DB' == line:
                if isBEGIN == True:
                    raise Exception('\'END_DB\' is missing.')
                isBEGIN = True
                isDATA = False
                data = {}
                keys = []
            elif 'END_DB' == line:
                if isBEGIN == False:
                    raise Exception('\'BEGIN_DB\' is missing.')
                isBEGIN = False
                isDATA = False
                isVAR = False
                self.append(data)
            elif isBEGIN:
                if line[:3] == 'VAR' and not isDATA:
                    line = line[3:].strip()
                    if line[0]=='"':
                        end = line.find('"',1)
                        if end>1:
                            key = line[1:end].strip()
                            value = line[end+1:].strip()
                            if value=='':
                                data[key] = ''
                            key_value = key, value.replace('"','')
                        else:
                            raise Exception('Parsing error at line %d:\'%s\'.\n\'VAR\' parameter is not correctly set'%(indxline, line))
                    else:
                        key_value = line.split(None, 1)
                    if len(key_value)>1:
                        try:
                            data[key_value[0]] = float(key_value[1])
                        except ValueError:
                            data[key_value[0]] = key_value[1]
                    else:
                        data[key] = ''
                elif line[0] == '#':
                    if isVAR:
                        raise Exception('Parsing error at line %d: \'%s\'.'%(indxline, line))
                    line = line[1:].strip()
                    if line=='':
                        raise Exception('Parsing error at line %d: \'%s\'.\nNumber of keys is null.'%(indxline, line))
                    if line.count('"')%2==1:
                        raise Exception('Parsing error at line %d: \'%s\'.\nNumber of keys is null.'%(indxline, line))
                    # begin parse
                    keys = []
                    isvar = False
                    isbrack = False
                    beg = 0
                    for i in xrange(len(line)):
                        if line[i] == '"':
                            if isvar:
                                data[line[beg:i]] = array([])
                                keys.append(line[beg:i])
                            beg = i + 1
                            isvar = not(isvar)
                            isbrack = not(isbrack)
                        elif line[i] in [' ','\t']:
                            if not isbrack:
                                if isvar:
                                    data[line[beg:i]] = array([])
                                    keys.append(line[beg:i])
                                beg = i + 1 
                                isvar = False
                        else:
                            isvar = True
                    if isvar:
                        data[line[beg:]] = array([])
                        keys.append(line[beg:])
                    # end parse
                    isDATA = True
                    isVAR = True
                elif isDATA:
                    if not isVAR:
                        raise Exception('Parsing error at line %d: \'%s\'.\nKeys are not declared.'%(indxline, line))
                    row = line.split()
                    if len(row)<>len(keys):
                        raise Exception('Parsing error at line %d:\'%s\'.\nNumber of data columns does not correspond to the number of keys.'%(indxline, line))
                    for key, value in zip(keys, row):
                        try:
                            data[key].append(float(value))
                        except ValueError:
                            data[key].append(value)
                else:
                    raise Exception('Parsing error at line %d:\'%s\'.'%(indxline, line))
            elif line[0] == '#':
                pass
            else:
                raise Exception('Parsing error at line %d:\'%s\'.'%(indxline, line))
        f.close()
        return self
    def filter(self, func):
        self = filter(func, self)
        return self
    def distinct(self, *keys):
        x = []
        for d in self:
            y = {}
            for k in keys:
                y[k]  = d[k]
            x.append(y)
        return distinct(x)
    def select(self, **kw):
        result = []
        for i, d in enumerate(self):
            x = True
            for k ,v in kw.iteritems():
	        try:
                    if d[k] <> v:
                        x = False
	        except KeyError:
                    raise Exception('KeyError of bloc %d. Please check on data file.'%(i))
            if x == True:
                result.append(d)
        return result
    def write(self):
        if not self.mode in ('w', 'a'):
            raise Exception('File not open for writing')
        g = open(self.filename, self.mode)
        for i in xrange(len(self)):
            try:
                buf = []
                buf.append('\nBEGIN_DB\n')
                table_keys = []
                for key, value in self[i].iteritems():
                    if isinstance(value, list):
                        table_keys.append(key)
                    else:
		        if isinstance(value, (float, int, complex)):
			    if ' ' in key:
			        buf.append(" VAR \"{key}\" {value}\n".format(key=key, value=value))
			    else:
			        buf.append(" VAR {key} {value}\n".format(key=key, value=value))
			elif ' ' in key:
			    buf.append(" VAR {key} \"{value}\"\n".format(key=key, value=value))
			else:
                            buf.append(" VAR \"{key}\" \"{value}\"\n".format(key=key, value=value))
		nkeys = 0
		for key, value in self[i].iteritems():
		    if isinstance(value, list):
		        nkeys += 1
		if nkeys>0:
                    buf.append("#")
                l = 0
                for _i, (key, value) in enumerate(self[i].iteritems()):
                    if _i==0:
                        if isinstance(value, list):
                            buf.append("\"{key}\"\t".format(key=key.strip()))
                            l = len(value)
                    else:
                        if isinstance(value, list):
                            buf.append("\"{key}\"\t".format(key=key.strip()).rjust(13))
                            l = len(value)
		if nkeys>0:
                    buf.append('\n')
                for j in xrange(l):
                    #g.write(" ")
                    for key, value in self[i].iteritems():
                        if isinstance(value, list):
                            buf.append("{value:<13.6e}\t".format(value=value[j].real))
                    buf.append('\n')
                buf.append('END_DB\n\n')
            except:
                g.close()
                raise Exception('Error in writing. DataBase[%d] is not consistent.'%i)
            for txt in buf:
	        #print repr(txt)
                g.write(txt)
        g.close()
            

