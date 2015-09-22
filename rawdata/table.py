
from collections import OrderedDict

__all__ = ['table']

class table(OrderedDict):
    def __init__(self, filename):
        OrderedDict.__init__(self)
        if filename[-4:] <> '.dat':
            raise Exception('wrong filename')
        self.filename = filename

    def read(self):
        try:
            with open(self.filename) as f:
                table = []
                for line in f:
                    line = line.strip()
                    if line=='' or line[0]=='#':
                        continue
                    row = line.split()
                    if len(row) > 1:
                        key = row[0]
                        values = [float(elt) for elt in row[1:]]
                        self[key] = values
                    else:
                        raise Exception( 'Failed to load the file. Error in the format of data...' )        
        except:
            raise Exception( 'Failed to load the file. The file has wrong format...')
        return self

    def write(self):
        try:
            max_number_of_char = max([len(k) for k in self.keys()])
            with open(self.filename, 'w') as g:
               g.write("# -*- type: table -*-\n")
               formatting = '{:<%d}' % (max_number_of_char)
               for key, value in self.iteritems():
                   key = formatting.format(key)
                   if hasattr(value, '__iter__'):
                       row = [key] + ['{:>13.6g}'.format(e) for e in value]
                   else:
                       row = [key, '{:>13.6g}'.format(value)]
                   g.write("\t".join(row) + "\n")
        except:
            raise Exception( 'Failed to save the file. The file cannot be write...')

