from libarray import *

class rawspice(dict):
    def __init__(self, filename=None):
        dict.__init__(self)
        self.filename = filename
    def read(self):
        with open(self.filename) as f:
	    isVariables = False
	    isValues = False
	    isTitle = False
	    appendTab = False
	    types = {}
	    ikey = 0
	    keys = []
	    ikey = 0
            while True:
	        line = f.readline()
		if line=='': break
		line = line.strip()
		if line=='': continue
		if 'Title' == line[:5]:
		    if isTitle:
		        if Title != line[:7]:
			    print line
		            raise Exception('Different plotnames in the same rawfile')
			isVariables = False
			isValues = False
			appendTab = True
		    else:
		        Title = line[:7]
		        isTitle = True
		elif 'Plotname' == line[:8]:
		    if appendTab:
		        if Plotname == 'ac' and 'AC Analysis' != line[10:]:
			     print line
			     raise Exception('Different plotnames in the same rawfile')
		        if Plotname == 'dc' and 'DC Analysis' != line[10:]:
			     print line
			     raise Exception('Different plotnames in the same rawfile')
		        if Plotname == 'op' and 'Operating Point' != line[10:]:
			     print line
			     raise Exception('Different plotnames in the same rawfile')
			continue
		    if 'AC Analysis' == line[10:]:
		        Plotname = 'ac'
		    if 'DC Analysis' == line[10:]:
		        Plotname = 'dc'
		    if 'Operating Point' == line[10:]:
		        Plotname = 'op'
		elif 'Flags' == line[:5]:
		    if appendTab:
		        if Flags != line[7:]:
			     raise Exception('Different plotnames in the same rawfile')
		    else:
		        Flags = line[7:]
		elif 'No. Variables' == line[:13]:
		    if appendTab:
		        if No_Variables != int(line[15:]):
			    print line
			    raise Exception('Different plotnames in the same rawfile')
		    else:
		        No_Variables = int(line[15:])
		elif 'No. Points' == line[:10]:
		    if appendTab:
		        if No_Points != int(line[12:]):
			    print line
			    raise Exception('Different plotnames in the same rawfile')
		    else:
		        No_Points = int(line[12:])
		elif 'Variables' == line[:9]:
		    isVariables = True
		    isValues = False
		elif 'Values' == line[:6]:
		    isValues = True
		    isVariables = False
		elif isVariables:
		    row = line.split(None, 2)
		    if appendTab:
		        try:
			    self[row[1]]
			except KeyError:
			    raise Exception('Different plotnames in the same rawfile')
		    else:
		        if Flags=='complex':
			    if row[2] == 'frequency':
			        types[row[1]] = 'float'
			    else:
		                types[row[1]] = 'complex'
		        else:
		            types[row[1]] = 'float'
		        self[row[1]] = array([])
		        keys.append(row[1])
		elif isValues:
		    key = keys[ikey]
		    if ikey == 0:
		        value = line.split(None, 1)[1]
		    else:
		        value = line
		    if Flags=='complex':
		        value = value.split(',', 1)
		        if types[key] == 'complex':
		            self[key].append( complex(float(value[0]), float(value[1])) )
		        elif types[key] == 'float':
		            self[key].append( float(value[0]) )
		    else:
		        self[key].append( float(value) )
		    if ikey>len(keys)-2:
		        ikey = 0
		    else:
		        ikey += 1
        return self


if __name__=='__main__':
     x = rawspice('data.ac').read()
     print x

	    
