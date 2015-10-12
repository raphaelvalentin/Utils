__version__ = '0.0.2'

import os, time, tempfile
from ngspice.spice3f5 import rawspice
from subprocess import Popen, PIPE, STDOUT
from functions.system import removedirs
from config import *

__all__ = ['ngspice']

class ngspice(object):
    
    __parameters__ = { 'log':'ngspice.log', 'path':'', 'filename':'ngspice.cir',
                       'debug':False, 'verbose':True}
    __history__ = []

    def __init__(self, netlist='', **parameters):
        self.raw = {}
        self.netlist = netlist
        self.__parameters__.update(parameters)

        # define temp dir
        tempfile.tempdir = TMP

        # clean history
        removedirs(*ngspice.__history__[:-MAX_HISTORY])

        # make dir and netlist
        self.__parameters__['path'] = parameters.get('path', tempfile.mkdtemp(prefix=PREFIX, suffix='/'))
        ngspice.__history__.append( self.__parameters__['path'] )
        self.raw_netlist = str(self.netlist)

        # convert netlist into text file
        self.filename = os.path.join(self.__parameters__['path'], self.__parameters__['filename'])

        # write netlist into text file
        try:
            # avoid Segmentation fault
            stat = os.statvfs(self.__parameters__['path'])
            if stat.f_bfree*stat.f_bsize<2*len(self.netlist):
                raise IOError('Not enough disk space')
            with open(self.filename,'w') as g:
                g.write(self.raw_netlist)
        except IOError, e:
            raise Exception("Netlist can not be written into disk. \n           %s."%e)

        # if debug, open text editor
        if self.__parameters__['debug']:
            cmd = "{text_editor} {filename}".format(text_editor=TEXT_EDITOR, filename=self.filename)
            Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True).communicate()

    def run(self):
        if self.__parameters__['log']:
            cmd = "cd {path}; {ngspice} -b -o {log} {filename}".format(path=self.__parameters__['path'], ngspice=NGSPICE, log=self.__parameters__['log'], filename=self.filename)
        else:
            cmd = "cd {path}; {ngspice} -b {filename}".format(path=self.__parameters__['path'], ngspice=NGSPICE, filename=self.filename)

        # open process
        pid = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True, env=os.environ)

        # run process
        start = time.time()
        if self.__parameters__['verbose']:
	    print '** NgSpice circuit Simulator is running at {time}...'.format(time=time.strftime("The %b %d %Y at %H:%M:%S", time.localtime(start)))
	    print '**     Simulating {filename} - `{title}`'.format(filename=self.filename, title=self.raw_netlist.splitlines()[0][2:])
        stdout = pid.communicate()[0]
        end = time.time()
 
        # check error in stdout
	if 'error' in stdout:
	    raise Exception("NgSpice was terminated due to a fatal error. \n           Please check the logfile : %s"%os.path.join(self.__parameters__['path'], self.__parameters__['log']))

        # check error in log file
        if self.__parameters__['log']:
  	    with open(os.path.join(self.__parameters__['path'], self.__parameters__['log'])) as f:
	        stdlog = f.read().lower()
                if 'error' in stdlog:
                    raise Exception("NgSpice was terminated due to a fatal error. \n           Please check the logfile : %s"%os.path.join(self.__parameters__['path'], self.__parameters__['log']))
 
        if self.__parameters__['verbose']: 
	    print '** NgSpice  completes the simulation in {time:.2f}s.'.format(time=(end-start))

        # extract output data files
        if hasattr(self.netlist, 'getRawFiles'):
            for pattern in self.netlist.getRawFiles():
	        outfile = os.path.join(self.__parameters__['path'], pattern)
	        if not os.path.isfile(outfile):
		    raise Exception("NgSpice was terminated due to a fatal error. \n           Please check the logfile : %s"%os.path.join(self.__parameters__['path'], self.__parameters__['log']))
                self.raw[pattern] = rawspice(outfile).read()
            if hasattr(self.netlist, 'postSimulation'):
	        self.netlist.postSimulation(self)

            # successfull data file extraction
            if self.__parameters__['verbose']:
	        print '** NgSpice Raw files has been succefully extracted.'
	print

        return self



