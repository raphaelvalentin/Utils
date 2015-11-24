__version__ = '0.0.2'

import os, time, tempfile
from spectre.psfascii import psfascii
from subprocess import Popen, PIPE, STDOUT
from functions.system import rm, source
from config import *


__all__ = ['spectre']

class spectre(object):
    
    __parameters__ = { 'log':'spectre.log', 'path':'', 'filename':'spectre.cir',
                       'debug':False, 'verbose':True}
    __history__ = []

    # config the shell environnement
    if os.path.isfile(SETMMSIM):
        source(SETMMSIM)
    os.environ.update(CONFIG_ENVIRON)

    def __init__(self, netlist='', **parameters):
        self.raw = {}
        self.netlist = netlist
        self.__parameters__.update(parameters)

        # define temp dir
        tempfile.tempdir = TMP

        # clean history
        rm(*spectre.__history__[:-MAX_HISTORY])
        spectre.__history__ = spectre.__history__[-MAX_HISTORY:]

        # make dir and netlist
        self.__parameters__['path'] = parameters.get('path', tempfile.mkdtemp(prefix=PREFIX, suffix='/'))
        spectre.__history__.append( self.__parameters__['path'] )
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
            cmd = "{spectre} +log {log} -format psfascii -raw {path} {filename}"
        else:
            cmd = "{spectre} -format psfascii -raw {path} {filename}"
        cmd = cmd.format( path=self.__parameters__['path'], 
                          spectre=SPECTRE, 
                          log=os.path.join(self.__parameters__['path'], self.__parameters__['log']), 
                          filename=self.filename )

        # open process
        pid = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True, env=os.environ)

        # run process
        try:
            start = time.time()
            if self.__parameters__['verbose']:
	        print '** Spectre circuit Simulator is running at {time}...'.format(time=time.strftime("The %b %d %Y at %H:%M:%S", time.localtime(start)))
	        print '**     Simulating {filename} - `{title}`'.format(filename=self.filename, title=self.raw_netlist.splitlines()[0][2:])
            stdout = pid.communicate()[0]
            end = time.time()
        except KeyboardInterrupt:
            print
            print 'KeyboardInterrupt: Spectre simulator has been stopped during running by user.'
            exit(1)

        # check error in stdout
        if "You do not have permission to run Virtuoso(R) Spectre" in stdout:
            raise Exception("Spectre was terminated prematurely due to a permission error. \n           Please check the logfile : %s"%os.path.join(self.__parameters__['path'], self.__parameters__['log']))
        if "spectre terminated prematurely due to fatal error." in stdout:
            raise Exception("Spectre was terminated prematurely due to fatal error. \n           Please check the logfile : %s"%os.path.join(self.__parameters__['path'], self.__parameters__['log']))
        if "Error found by spectre during" in stdout:
            raise Exception("Spectre was terminated due to a fatal error. \n           Please check the logfile : %s"%os.path.join(self.__parameters__['path'], self.__parameters__['log']))
 
        if self.__parameters__['verbose']: 
	    print '** Spectre  completes the simulation in {time:.2f}s.'.format(time=(end-start))

        start = time.time()
        # extract output data files
        if hasattr(self.netlist, 'getRawFiles'):
            for pattern in self.netlist.getRawFiles():
	        outfile = os.path.join(self.__parameters__['path'], pattern)
	        if not os.path.isfile(outfile):
		    raise Exception("Spectre was terminated due to a fatal error. \n           Please check the logfile : %s"%os.path.join(self.__parameters__['path'], self.__parameters__['log']))
                self.raw[pattern] = psfascii(os.path.join(self.__parameters__['path'],pattern)).read()
            end = time.time()

            # successfull data file extraction
            if self.__parameters__['verbose']:
	        print '** Spectre Raw files has been succefully extracted in {time:.2f}s.'.format(time=(end-start))
        if self.__parameters__['verbose']:
	    print

        return self



