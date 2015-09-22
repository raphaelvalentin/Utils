
class modelParameter(dict):
    def __init__(self, filename=None):
        dict.__init__(self)
        self.filename = filename
    def read(self):
        with open(self.filename) as f:
	    lines = f.readlines()
        isHEADER = False
        isVALUE = False
        isTYPE = False
        TYPE = []
	VALUE = []
	indxLine = 0
        while True:
            line = lines[indxLine]
            indxLine += 1
            if line == '': break
            line= line.strip()
            if line == "HEADER":
                isHEADER = True
                isTYPE =  False
                isVALUE = False
            elif line == "TYPE":
                isHEADER = False
                isTYPE =  True
                isTRACE = False
            elif line == "VALUE":
                isHEADER = False
                isTYPE = False
                isVALUE = True
            elif line == "END":
                break
            elif isHEADER:
	        pass
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
		key = d[0]
		if d[1] == "STRUCT(":
		    ibracket = 0
		    for elt in d[2:-1]:
		        ibracket += elt.count('(') - elt.count(')')
			if elt in ('FLOAT', 'DOUBLE','INT','BYTE','LONG') or '(' in elt or ')' in elt:
			    pass
			elif ibracket==0:
			    TYPE.append(elt)
		else:
                    TYPE.append(key)
            elif isVALUE:
	        ibracket = 0
                if "(" in line:
                    while indxLine<len(lines):
		        ibracket = line.count('(') - line.count(')')
			if ibracket == 0: break
                        l = lines[indxLine]
		        indxLine += 1
                        line += " " + l.strip()
                d = line.replace("\"", "").split()
		self.name = d.pop(0)
		self.model = d.pop(0)
		for elt in d[1:-1]:
		    try :
   		        VALUE.append(float(elt))
		    except:
		        pass
        
	for k, v in zip(TYPE,VALUE):
	    self[k]=v
	return self		 
		    
		
	    
	
		
	
	
#a = modelParameter(filename='modelParameter.info').read()
#print a['capmod']
