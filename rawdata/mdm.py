from libarray import *
from functions import *
import sys
from collections import OrderedDict

__all__ = ['mdm']

class mdm(list):
    def __init__(self, filename=''):
        list.__init__(self)
        self.filename = filename
    def read(self):
        f = open(self.filename, 'r')
        isBEGIN = False
        isDATA = False
        isVAR = False
        isHEADER = False
        isICCAP_OUTPUTS = False
        keys = []
        indxline = 0
        header = {}

        while 1:
            indxline +=1
            line = f.readline()
            if line == '': break
            line = line.strip()
            if line == '' or line[0]=='!':
                pass
            elif 'BEGIN_HEADER' == line:
                isHEADER = True
            elif 'BEGIN_DB' == line:
                if isBEGIN == True:
                    raise Exception('\'END_DB\' is missing.')
                isBEGIN = True
                isDATA = False
                #data = {}
                data = OrderedDict()
                keys = []
            elif 'END_DB' == line:
                if isBEGIN == False:
                    raise Exception('\'BEGIN_DB\' is missing.')
                isBEGIN = False
                isDATA = False
                isVAR = False
                self.append(data)
            elif isHEADER:
                if 'END_HEADER' == line:
                    isHEADER = False
                elif 'ICCAP_OUTPUTS' == line:
                    isICCAP_OUTPUTS = True
                elif 'ICCAP_VALUES' == line:
                    isICCAP_OUTPUTS = False
                elif isICCAP_OUTPUTS:
                    d = line.split()
                    header[d[0]] = d[1]
            elif isBEGIN:
                if line[:9] == 'ICCAP_VAR' and not isDATA:
                    line = line.split(None, 1)[1]
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
        self.header = header

        ### simplify keys name (not efficient but it works)
        # if complex
        for db in self:
            for k in db.keys():
                if 'R:' == k[:2]:
                    db[k[2:]] = [complex(r, i) for r, i in zip(db['R:' + k[2:]] , db['I:' + k[2:]]) ]
                    del db['R:' + k[2:]]
                    del db['I:' + k[2:]]
        # if array 
        to_del = []
        for db in self:
            for k in db.keys():
               if len(k)>5 and k[-5]=='(' and  k[-3]==',' and  k[-1]==')' :
                   n2 = [s1 for s1 in db.keys() if k[:-5]==s1[:-5]]
                   if len(n2)>1:
                       for s2 in n2:
                           db[s2[:-5]+s2[-4]+s2[-2]] = db[s2]
                           if not s2 in to_del:
                               to_del.append(s2)
                   else:
                       db[k[:-5]] = db[k]
                       if not k in to_del:
                           to_del.append(k)
            for k in to_del:
                del db[k]


        return self

    

if __name__ == '__main__':
    filename = 'I1_TRANSF_1_1.mdm'
    d = mdm(filename).read()
    #print d.header
    print d[0].keys()
    print d[0]['s11'][:10]

