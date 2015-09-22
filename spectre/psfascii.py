from libarray import *
import time

__all__ = ['psfascii']

class psfascii(dict):
    def __init__(self, filename=None):
        dict.__init__(self)
        self.filename = filename
	self.test = 5
    def read(self):
        isreadable = False
        for i in xrange(self.test):
	    with open(self.filename) as f:
	        lines = f.readlines()
		if len(lines)>3:
                    if lines[0].strip() == "HEADER" and lines[1].strip() == '"PSFversion" "1.00"' and lines[-1].strip() == "END":
		        isreadable = True
	                break
	    time.sleep(0.1)
	if not isreadable:
	    raise Exception('Error: %s is not readable.'%(filename))
        isHEADER = False
        isVALUE = False
        isTYPE = False
        isSWEEP = False
        isTRACE = False
        isSWEEPed = False
        TYPE = {}
        type = {}
	indxLine = 0
        while True:
            line = lines[indxLine]
            indxLine += 1
            if line == '': break
            line= line.strip()
            if line == "HEADER":
                isHEADER = True
                isTYPE =  False
                isSWEEP = False
                isTRACE = False
                isVALUE = False
            elif line == "TYPE":
                isHEADER = False
                isTYPE =  True
                isSWEEP = False
                isTRACE = False
                isVALUE = False
            elif line == "SWEEP":
                isSWEEPed = True
                isHEADER = False
                isTYPE =  False
                isSWEEP = True
                isTRACE = False
                isVALUE = False
            elif line == "TRACE":
                isHEADER = False
                isTYPE =  False
                isSWEEP = False
                isTRACE = True
                isVALUE = False
            elif line == "VALUE":
                isHEADER = False
                isTYPE = False
                isSWEEP = False
                isTRACE = False
                isVALUE = True
            elif line == "END":
                break
            elif isHEADER:
	        d = line.replace('"', '').split()
                if "analysis type" in line:
		    self["analysis type"] = d[2]
                if "analysis name" in line:
		    self["analysis name"] = d[2]
            elif isTYPE:
	        ibracket = 0
                if "(" in line:
                    while indxLine<len(lines):
		        ibracket = line.count('(') - line.count(')')
			if ibracket == 0: break
                        l = lines[indxLine]
		        indxLine += 1
                        line += " " + l.strip()
                d = line.replace("\"", "").split()
                key, value = d[0], d[1]
                TYPE[key] = value
            elif isSWEEP:
	        ibracket = 0
                if "(" in line:
                    while indxLine<len(lines):
		        ibracket = line.count('(') - line.count(')')
			if ibracket == 0: break
                        l = lines[indxLine]
		        indxLine += 1
                        line += " " + l.strip()
                d = line.replace("\"", "").split()
                key, value = d[0], d[1]
                self[key] = array([])
                if TYPE[value] == "FLOAT":
                    type[key] = float
                elif TYPE[value] == "COMPLEX":
                    type[key] = complex
                elif TYPE[value] == "STRUCT(":
		    type[key] = dict
            elif isTRACE:
	        ibracket = 0
                if "(" in line:
                    while indxLine<len(lines):
		        ibracket = line.count('(') - line.count(')')
			if ibracket == 0: break
                        l = lines[indxLine]
		        indxLine += 1
                        line += " " + l.strip()
                d = line.replace("\"", "").split()
                key, value = d[0], d[1]
                self[key] = array([])
                if TYPE[value] == "FLOAT":
                    type[key] = float
                elif TYPE[value] == "COMPLEX":
                    type[key] = complex
                elif TYPE[value] == "STRUCT(":
		    type[key] = dict
            elif isVALUE:
	        ibracket = 0
                if "(" in line:
                    while indxLine<len(lines):
		        ibracket = line.count('(') - line.count(')')
			if ibracket == 0: break
                        l = lines[indxLine]
		        indxLine += 1
                        line += " " + l.strip()
                key, value = line.replace("\"", "").split(None, 1)
                if isSWEEPed:
                    if type[key] == float:
                        self[key].append(float(value))
                    elif type[key] == complex:
                        v = value.replace('(', '').replace(')', '').split()
                        self[key].append(complex(float(v[0]), float(v[1])))
                    elif type[key] == dict:
                        v = value.replace('(', '').replace(')', '').split()
                        self[key].append(list(float(x) for x in v))
                else:
                    if not(key in self):
                        self[key]=array([])
                    type[key] = value.split()[0]
                    self[key].append(float(value.split()[1]))
        return self
