import re, time, os, shutil, string
from subprocess import Popen, PIPE, STDOUT
from random import randint, seed

__all__ = ['find', 'removedirs', 'source', 'tempfile', 'copy', 'rm', 'template, template_dir']

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

def rm(*files):
#    for i, file in enumerate(files):
#        try:
#            os.system('/bin/rm -rf %s > /dev/null 2>&1'%file)
#	except:
#	    pass
    # more pythonic
    for src in files:
        try:
            if os.path.isdir(src):
                shutil.rmtree(src)
            else:
                os.remove(src)
        except OSError as e:
            print('%s not removed. Error: %s'%(src, e))

def removedirs(*args):
    print 'Deprecated: use rm'
    rm(*args)
    
def source(filename):
    cmd = "source {filename}; env".format(filename=filename)
    p = Popen(cmd, executable='/bin/tcsh', stdout=PIPE, stderr=STDOUT, shell=True, env=os.environ)
    stdout = p.communicate()[0].splitlines()
    for line in stdout:
        if re.search('[0-9a-zA-Z_-]+=\S+', line):
            key, value = line.split("=", 1)
            os.environ[key] = value

def copy(src, dest, force=False):
    try:
        if force and os.path.isdir(dest):
            # not good for speed
            rm(dest)
        shutil.copytree(src, dest)
    except OSError as e:
        # if src is not a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('%s not copied. Error: %s'%(src, e))

def template(src, dest, substitute={}):
    with open(src) as f:
        s = string.Template(f.read())
        o = s.safe_substitute(substitute)
    with open(dest, 'w') as g:
        g.write(o)

def template_dir(src, dest, substitute={}):
    if src<>dest:
        copy(src, dest, force=True)
    for root, subdirs, files in os.walk(dest):
        file_path = os.path.join(dest, filename)
        s = template(file_path, file_path, substitute)

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


