from rawdata.mdm import mdm
from rawdata.touchstone import snp

def mdm2snp(filename):
    db = mdm(filename).read()[0]
    name = filename.split('.')[0]
    if 's22' in db:
        x = snp(name+'.s2p')
        x.write(db)
    elif 's11' in db:
        x = snp(name+'.s1p')
        x.write(db)

    
if __name__ == '__main__':
    import sys
    mdm2snp(sys.argv[1])    
