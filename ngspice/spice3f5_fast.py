import numpy as np

FLOAT = 1
COMPLEX = 2

class rawspice(dict):
    def __init__(self, filename=None):
        dict.__init__(self)
        self.filename = filename
    def read(self):
        
        with open(self.filename) as f:

            # READ BLOCK HEADER
            line = f.readline() # Title
            if 'Title' == line[:5]:
                line = line.strip()
                Title = line[:7]
                line = f.readline()  # Date
            if 'Date' == line[:4]:
                line = f.readline()  # Plotname
            if 'Plotname' == line[:8]:
                line = line.strip()
                if 'AC Analysis' == line[10:]:
                    Plotname = 'ac'
                elif 'DC Analysis' == line[10:]:
                    Plotname = 'dc'
                elif 'Operating Point' == line[10:]:
                    Plotname = 'op'
                line = f.readline() # Flags
            if 'Flags' == line[:5]:
                line = line.strip()
	        if line[7:]=='complex':
                    Flags = COMPLEX
                elif line[7:]=='float':
                    Flags = FLOAT
                line = f.readline() # No. Variables
            if 'No. Variables' == line[:13]:
                line = line.strip()
                No_Variables = int(line[15:])
                line = f.readline() # No. Points
            if 'No. Points' == line[:10]:
                line = line.strip()
                No_Points = int(line[12:])
                line = f.readline() # Variables
            if 'Variables' == line[:9]:
                types = {}
	        keys = []
                for i in xrange(No_Variables):
                    line = f.readline()
                    row = line.split()
                    if Flags==COMPLEX:
		        if row[2] == 'frequency':
			    types[row[1]] = FLOAT
			else:
		            types[row[1]] = COMPLEX
                    keys.append(row[1])
                line = f.readline() # Values
            if 'Values' == line[:6]:
                Pos_Values = f.tell()

                # ALLOCATION
                for key in keys:
                    if types[key] == COMPLEX:
                        self[key] = ['0.000000000000000e+00'] * No_Points * 2
                    else:
                        self[key] = ['0.000000000000000e+00'] * No_Points

                # READ BLOCK
                if Flags == COMPLEX:
                    for i in xrange(No_Points):
                        # first line
                        line = f.readline()
                        key = keys[0]
                        value = line.split(None, 1)[1]
		        value = value.split(',', 1)
		        if types[key] == COMPLEX:
		            self[key][2*i:2*i+2] = value
		        else:
		            self[key][i] = value[0]
                        # next lines
                        for key in keys[1:]:
 	                    line = f.readline()
    		            value = line.strip()
		            value = value.split(',', 1)
		            if types[key] == COMPLEX:
		                self[key][2*i:2*i+2] = value
		            else:
		                self[key][i] = value[0]
                else:
                    for i in xrange(No_Points):
                        # first line
                        line = f.readline()
                        key = keys[0]
                        value = line.split(None, 1)[1]
		        self[key][i] = value
                        # next lines
                        for key in keys[1:]:
 	                    line = f.readline()
    		            value = line.strip()
		            self[key][i] = value

            while 1:
                line = f.readline()
                if line == '':
                    # RETURN
                    for key in self.keys():
                        self[key] = np.asfarray(self[key])
                        if types[key] == COMPLEX:
                            n = self[key].shape[0]/2
                            x = np.empty(n, dtype=complex)
                            x.real, x.imag = np.reshape(self[key], (2, n))
                            self[key] = x
                    return self
                    
                elif 'Title' == line[:5]:
                    break
            
            current = f.tell()
            size_block = current - len(line)
            f.seek(0,2)
            No_Blocks = f.tell()/size_block

            # ALLOCATION
            for key in keys:
                if types[key] == COMPLEX:
                    self[key].extend(['0.000000000000000e+00'] * No_Points * 2 * (No_Blocks-1))
                else:
                    self[key].extend(['0.000000000000000e+00'] * No_Points * (No_Blocks-1))

            f.seek(current)
            j = 1 * No_Points
            while 1:
                
                line = f.readline()
                if line == '':
                    # RETURN
                    for key in self.keys():
                        self[key] = np.asfarray(self[key])
                        if types[key] == COMPLEX:
                            n = self[key].shape[0]/2
                            x = np.empty(n, dtype=complex)
                            x.real, x.imag = np.reshape(self[key], (n, 2)).transpose()
                            self[key] = x
                    return self

                if 'Values' == line[:6]:

                    # READ BLOCK
                    if Flags == COMPLEX:
                        for i in xrange(No_Points):
                            # first line
                            line = f.readline()
                            key = keys[0]
                            value = line.split(None, 1)[1]
		            value = value.split(',', 1)
		            if types[key] == COMPLEX:
		                self[key][2*(i+j):2*(i+j)+2] = value
		            else:
		                self[key][i+j] = value[0]
                            # next lines
                            for key in keys[1:]:
 	                        line = f.readline()
    		                value = line.strip()
		                value = value.split(',', 1)
		                if types[key] == COMPLEX:
		                    self[key][2*(i+j):2*(i+j)+2] = value
		                else:
		                    self[key][i+j] = value[0]
                    else:
                        for i in xrange(No_Points):
                            # first line
                            line = f.readline()
                            key = keys[0]
                            value = line.split(None, 1)[1]
		            self[key][i+j] = value
                            # next lines
                            for key in keys[1:]:
 	                        line = f.readline()
    		                value = line.strip()
		                self[key][i+j] = value

                    j = j + No_Points



if __name__=='__main__':
     from time import time
     t0 = time()
     for i in xrange(1000):
          x = rawspice('data.ac').read()
     print time()-t0
     #print x['frequency']
     #print x.keys()
     print x['xp2.v']
	    
