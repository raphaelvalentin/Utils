import csv

__all__ = ['csvreader']

class csvreader(csv.DictReader):
    def __init__(self, filename):
        self.csvfile = open(filename)
        csv.DictReader.__init__(self, self.csvfile)

    def lookup(self, **kwargs):
        for row in self:
            isfound = True
            for k, v in kwargs.iteritems():
                if k in row:
                   if row[k] <> str(v):
                       isfound = False
                       break
                else:
                    raise KeyError(k)
            if isfound:
                self.csvfile.seek(0)
                return row
        self.csvfile.seek(0)

    def __del__(self):
        self.csvfile.close()

if __name__ == '__main__':
    a = csvreader('noise.csv')
    print a.lookup(Vds=1.5,Vgs=0.5)['Filename']

    for row in a:
        print row

