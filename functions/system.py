import re, time, os
from subprocess import Popen, PIPE, STDOUT


__all__ = ['find', 'removedirs', 'source', 'tempfile']

def find(path='.', regex='*', ctime=0):
    r = []
    regex = str(regex).strip()
    if regex == '*': regex = ''
    now = time.time()
    for filename in os.listdir(path):
        try:
            if re.search(regex, filename):
                tmtime = os.path.getmtime(os.path.join(path, filename))
                if ctime>0 and int((now-tmtime)/3600/24) > ctime:
                    r.append(os.path.join(path, filename))
                elif ctime<0 and int((now-tmtime)/3600/24) < ctime:
                    r.append(os.path.join(path, filename))
                elif ctime==0:
                    r.append(os.path.join(path, filename))
        except:
            pass
    return r


def removedirs(*files):
    for i, file in enumerate(files):
        try:
            os.system('/bin/rm -rf %s > /dev/null 2>&1'%file)
	except:
	    pass


def source(filename):
        cmd = "source {filename}; env".format(filename=filename)
        p = Popen(cmd, executable='/bin/tcsh', stdout=PIPE, stderr=STDOUT, shell=True, env=os.environ)
        stdout = p.communicate()[0].splitlines()
        for line in stdout:
            if re.search('[0-9a-zA-Z_-]+=\S+', line):
                key, value = line.split("=", 1)
                os.environ[key] = value

from random import randint, seed
from exceptions import OSError

class tempfile:
    letters = "ABCDEFGHIJLKMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_"
    tempdir = '/tmp/'
    seed()
    
    @staticmethod
    def randstr(n=10):
       return "".join(tempfile.letters[randint(0,len(tempfile.letters)-1)] for i in xrange(n))
       
    @staticmethod
    def mkdtemp(prefix='', suffix=''):
        n = 7
	i = 0
        while 1:
            try:
	        path = os.path.join(tempfile.tempdir, prefix + tempfile.randstr(n) + suffix)
                os.mkdir(path)
		return path
            except OSError:
	        i = i + 1
                if i%10==0:
	            n = n + 1
	        if n > 12:
	            raise OSError('cannot create a temporary directory')

if __name__=='__main__':
    print random_string()
