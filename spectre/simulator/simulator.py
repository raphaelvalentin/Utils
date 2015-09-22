__version__ = '0.0.4'

import os, time, re, tempfile
from spectre.psfascii import psfascii
from subprocess import Popen, PIPE, STDOUT
#from spectre import *nedit 
from function import find, removedirs, source
from config import *


class spectre(object):
    
    __parameters__ = { 'log':'spectre.log', 'path':'', 'filename':'spectre.cir',
                       'debug':False, 'version':0.0, 'verbose':True, 'force':True}
    __history__ = []
    try: __parameters__['version'] = VERSION
    except: pass

    def __init__(self, netlist='', **parameters):
	self.t0=time.time()
        self.raw = {}
        self.netlist = netlist
        self.__parameters__.update(parameters)
        deprecatedfiles = find(regex='{prefix}[0-9a-zA-Z_]'.format(prefix=PREFIX), path=TMP, ctime=EXPIRATION)
        removedirs(*deprecatedfiles)
	if self.__parameters__['verbose'] and len(deprecatedfiles):
	    print "** %d deprecated files has been removed from %s directory."%(len(deprecatedfiles),TMP)
        _version = self.__parameters__['version']
        self.getVersion()
        if _version <> self.__parameters__['version']:
            self.setVersion(_version)
        tempfile.tempdir = TMP
        self.__parameters__['path'] = parameters.get('path', tempfile.mkdtemp(prefix=PREFIX, suffix='/'))
	
	if HISTORY>0:
	    if len( spectre.__history__ ) >= HISTORY:
	        spectre.__history__.pop(0)
	    spectre.__history__.append((netlist, self.__parameters__.copy()))
	
	
    def __mem__(self):
        if not self.__parameters__['force']:
	    for netlist, parameters in spectre.__history__[:-1]:
	        if str(self.netlist)==str(netlist) and self.__parameters__['version']==parameters['version'] and self.__parameters__['filename']==parameters['filename'] and self.__parameters__['log']==parameters['log']:
		    self.__parameters__['path'] = parameters['path']
		    filename = os.path.join(self.__parameters__['path'], self.__parameters__['filename'])
                    if self.__parameters__['debug']:
                        Popen("{text_editor} {filename}".format(text_editor=TEXT_EDITOR, filename=filename), stdout=PIPE, stderr=STDOUT, shell=True).communicate()
                    if self.__parameters__['verbose']: 
            	        print '** A previous simulation was found in the history...'
            	        print '**     Read {filename} - `{title}`'.format(filename=filename, title=str(self.netlist).splitlines()[0][2:])
                    if self.__parameters__['log']:
                        log = os.path.join(self.__parameters__['path'], self.__parameters__['log'])
		    try:
		        with open(log) as f:
			    stdout = f.read()
                        if "You do not have permission to run Virtuoso(R) Spectre" in stdout:
                            raise Exception("spectre was terminated prematurely due to a permission error.")
                        if "spectre terminated prematurely due to fatal error." in stdout:
                            raise Exception("spectre was terminated prematurely due to fatal error.")
                        if "Error found by spectre during" in stdout:
                            raise Exception("spectre was terminated due to a fatal error.")
		    except:
		        return False
                    if hasattr(self.netlist, 'getRawFiles'):
                        for pattern in self.netlist.getRawFiles():
			    try:
                                self.raw[pattern] = psfascii(os.path.join(self.__parameters__['path'],pattern)).read()
			    except:
			        return False
                    if self.__parameters__['verbose']:
            	        print '** Spectre Raw files has been succefully extracted.'
            	        print
		    return True
        return False


    def run(self):
        if self.__mem__():
	    return self
        filename = os.path.join(self.__parameters__['path'], self.__parameters__['filename'])
        with open(filename,'w') as f:
            f.write(str(self.netlist))
        if self.__parameters__['debug']:
            Popen("{text_editor} {filename}".format(text_editor=TEXT_EDITOR, filename=filename), stdout=PIPE, stderr=STDOUT, shell=True).communicate()
        if self.__parameters__['verbose']: 
	    print '** Spectre circuit Simulator {version} is running at {time}...'.format(time=time.strftime("The %b %d %Y at %H:%M:%S"), version=self.__parameters__['version'])
	    print '**     Simulating {filename} - `{title}`'.format(filename=filename, title=str(self.netlist).splitlines()[0][2:])
        cmd = [SPECTRE]
        if self.__parameters__['log']:
            log = os.path.join(self.__parameters__['path'], self.__parameters__['log'])
            cmd.append('+log {log}'.format(log=log))
        cmd.append('-format psfascii')
        cmd.append('-raw {path}'.format(path=self.__parameters__['path']))
        cmd.append(filename)
	time.sleep(0.1)
        start = time.time()
        p = Popen(" ".join(cmd), stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True, env=os.environ)
        stdout = p.communicate()[0]
        end = time.time()
        if "You do not have permission to run Virtuoso(R) Spectre" in stdout:
	    i=1000
	    print '** Restart the simulation...(%d)'%i
	    import sys
	    while i>0:
	        print "\033[F** Restart the simulation...(%d)     "%(1000-i)
                p = Popen(" ".join(cmd), stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True, env=os.environ)
                stdout = p.communicate()[0]
                end = time.time()
		time.sleep(1000-i)
		if not("You do not have permission to run Virtuoso(R) Spectre" in stdout):
		    break
	        i=i-1
	    if i==0:
                raise Exception("spectre was terminated prematurely due to a permission error.")
        if "spectre terminated prematurely due to fatal error." in stdout:
            raise Exception("spectre was terminated prematurely due to fatal error.")
        if "Error found by spectre during" in stdout:
            raise Exception("spectre was terminated due to a fatal error.")
        if self.__parameters__['verbose']: 
	    print '** Spectre completes the simulation in {time:.2f}s.'.format(time=(end-start))
        if hasattr(self.netlist, 'getRawFiles'):
            for pattern in self.netlist.getRawFiles():
                self.raw[pattern] = psfascii(os.path.join(self.__parameters__['path'],pattern)).read()
        if self.__parameters__['verbose']:
	    print '** Spectre Raw files has been succefully extracted.'
	    print
        return self

    def getVersion(self):
        cmd = "{spectre} -version".format(spectre=SPECTRE)
        p = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True, env=os.environ) 
        stdout = p.communicate()[0].split()
        for i in xrange(len(stdout)):
            if stdout[i] == 'version':
                self.__parameters__['version'] = float(stdout[i+1].split('.')[0] + '.' + "".join(stdout[i+1].split('.')[1:]))
                return self.__parameters__['version']
        raise Exception("can not extract version")		
    
    def setVersion(self, version):
        if version not in CONFIG_ENVIRON:
            raise Error("version {version} is not declared in the 'CONFIG_ENVIRON' variable.".format(version=version))
        source(CONFIG_ENVIRON[version])
        self.getVersion()
        if self.__parameters__['version'] <> version:
            raise Exception("version is not set correctly, actual version is {version}.".format(version=self.__parameters__['version']))
        return self



