import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.figure import SubplotParams
from matplotlib.ticker import MaxNLocator
from os.path import isfile
import tempfile

__all__ = ['plot']



from math import floor, log10
inf = float('inf')
  
def eng(x):
    """Returns x as a * 10 ^ b with 0<= a <10"""
    if x == 0: return 0 , 0
    Neg = x <0
    if Neg : x = -x
    a = 1.0 * x / 10**(floor(log10(x)))
    b = int(floor(log10(x)))
    if Neg : a = -a
    a = a * 10**(b%3)
    b = b - b%3
    if b>12 or b<-18: # avoid unvailable unit
        return x, 0
    return a ,b

def unit(x):
    if x==0: return ''
    if x==3: return 'k'
    if x==6: return 'M'
    if x==9: return 'G'
    if x==12: return 'T'
    if x==-3: return 'm'
    if x==-6: return 'u'
    if x==-9: return 'n'
    if x==-12: return 'p'
    if x==-15: return 'f'
    if x==-18: return 'a'
    return ''

class plot(object):
    

    def __init__(self, **kwargs):
        self.dpi = kwargs.get('dpi', 100)
        self._caption = kwargs.get('caption', '')
        self.figsize = kwargs.get('figsize', (8, 6))
        self._xlabel = kwargs.get('xlabel', '')
        self._ylabel = kwargs.get('ylabel', '')
        self.fontsize = kwargs.get('fontsize', 19)
        self.xlogscale = kwargs.pop('xlogscale', False)
        self.ylogscale = kwargs.pop('ylogscale', False)
	self._labels = list()
	self._plots = list()
        self.filename = kwargs.get('filename', 'image.png')
        self.xunit = kwargs.get('xunit', None)
        self.yunit = kwargs.get('yunit', None)
        self.PY_GRAPH_DIR = os.environ.get('PY_GRAPH_DIR', '')

    def xlabel(self, label, unit=None):
        self._xlabel = label
        self.xunit = unit
    def ylabel(self, label, unit=None):
        self._ylabel = label
        self.yunit = unit
    def caption(self, caption):
        self._caption = caption

	
    def plot(self, *args, **kwargs):
        _kwargs = dict(kwargs)
        if not 'linewidth' in kwargs:
	    kwargs['linewidth'] = 2
        i = 0
        _kwargs = dict(kwargs)
        while i<len(args):
	    kwargs = dict(_kwargs)
	    x = args[i]
	    i = i+1
	    if not isinstance(x, (list, np.ndarray)):
	        raise Exception('x is not a list')
	    if len(np.shape(x)) == 1:
	        y = args[i]
		i = i+1
	    elif len(np.shape(x)) == 2:
	        x, y = x
	    elif len(np.shape(x)) == 3:
	        raise Exception('the shape of x is not correct')
   	    if not isinstance(y, (list, np.ndarray)):
	        raise Exception('y is not a list')
	    if len(np.shape(y))<>1:
	        raise Exception('the shape of y is not 1')
	    if len(x)<>len(y):
	        raise Exception('x and y sizes are different.')
	    if 'label' in kwargs:
		if kwargs['label'] in self._labels:
		    del kwargs['label']
		else:
		    self._labels.append(kwargs['label'])
	    if i<len(args) and isinstance(args[i], str):
		linespec = args[i]
		i = i+1
		self._plots.append([x, y, linespec, kwargs])
	    else:
		self._plots.append([x, y, kwargs])

    def scatter(self, *args, **kwargs):
        markeredgecolor = kwargs.pop('color', 'r')
	markersize = kwargs.pop('size', 6)
        properties = {'marker':'s', 'markersize':markersize, 'linewidth':0, 
                      'markerfacecolor':'none', 'markeredgecolor':markeredgecolor, 'markeredgewidth':2
                     }
	properties.update(**kwargs)
	self.plot(*args, **properties)
        
    def savefig(self, filename=None, dpi=100, force=True):
        if filename == None:
            filename = tempfile.mktemp(dir=self.PY_GRAPH_DIR, suffix='.png')
        self.filename = filename
	self.dpi = dpi
	
	# generation of the image
        plt.rc('font', family='sans-serif',  size=self.fontsize)
        plt.rc('figure', figsize=(8,6))
        plt.rc('figure', dpi=self.dpi)
        plt.rc('figure.subplot', left=0.20, bottom=0.13, right=0.93, top=0.93, wspace=0.001, hspace=0.1)
        plt.rc('lines', markersize=6)
        plt.rc('axes', labelsize=self.fontsize)
        plt.rc('axes', color_cycle=('red', 'blue', 'green', 'black', 'grey', 'yellow'))
        plt.rc('axes', grid=True)
        plt.rc('axes', linewidth=2)
        plt.rc('xtick.major', size=8)           # major tick size in points
        plt.rc('xtick.minor', size=5)           # minor tick size in points
        plt.rc('xtick.major', width=1.5)        # major tick width in points
        plt.rc('xtick.minor', width=1.5)        # minor tick width in points
        plt.rc('xtick.major', pad=4)            # distance to major tick label in points
        plt.rc('xtick.minor', pad=4)            # distance to the minor tick label in points
        plt.rc('xtick', color='k')                # color of the tick labels
        plt.rc('xtick', labelsize=self.fontsize)       # fontsize of the tick labels
        plt.rc('xtick', direction='in')           # direction: in, out, or inout
        plt.rc('ytick.major', size=8)           # major tick size in points
        plt.rc('ytick.minor', size=5)           # minor tick size in points
        plt.rc('ytick.major', width=1.5)        # major tick width in points
        plt.rc('ytick.minor', width=1.5)        # minor tick width in points
        plt.rc('ytick.major', pad=4)            # distance to major tick label in points
        plt.rc('ytick.minor', pad=4)            # distance to the minor tick label in points
        plt.rc('ytick', color='k')                # color of the tick labels
        plt.rc('ytick', labelsize=self.fontsize)       # fontsize of the tick labels
        plt.rc('ytick', direction='in')           # direction: in, out, or inout


        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1,1,1)
        self.ax.xaxis.set_major_formatter(FormatStrFormatter('%g'))
        self.ax.yaxis.set_major_formatter(FormatStrFormatter('%g'))

        # Engineering notation, xaxis and rescaling
        if self.xunit<>None and not(self.xlogscale):
            xpower = 0
            xmin, xmax = inf, -inf
	    for plti in self._plots:
                xmin, xmax = min(xmin, min(plti[0])), max(xmax, max(plti[0]))
            xpower = eng(max(abs(xmax),abs(xmin))*1.2)[1]
	    for plti in self._plots:
                plti[0] = np.array(plti[0])*10**-xpower
            if xpower == 0:
                if self.xunit=='':
                    self.xunit = '1'
                plt.xlabel('%s (%s)'%(self._xlabel,self.xunit))
            else:
                if self.xunit=='1':
                    self.xunit = ''
                plt.xlabel('%s (%s%s)'%(self._xlabel,unit(xpower),self.xunit))
        elif self.xunit<>None:
            plt.xlabel('%s (%s)'%(self._xlabel,self.xunit))
        else:
            plt.xlabel(self._xlabel)

        # Engineering notation, yaxis and rescaling
        if self.yunit<>None and not(self.ylogscale):
            ypower = 0
            ymin, ymax = inf, -inf
	    for plti in self._plots:
                ymin, ymax = min(ymin, min(plti[1])), max(ymax, max(plti[1]))
            ypower = eng(max(abs(ymax),abs(ymin))*1.2)[1]
	    for plti in self._plots:
                plti[1] = np.array(plti[1])*10**-ypower
            if ypower == 0:
                if self.yunit=='': 
                    self.yunit = '1'
                plt.ylabel('%s (%s)'%(self._ylabel,self.yunit))
            else:
                if self.yunit=='1':
                    self.yunit = ''
                plt.ylabel('%s (%s%s)'%(self._ylabel,unit(ypower),self.yunit))
        elif self.yunit<>None:
            plt.ylabel('%s (%s)'%(self._ylabel,self.yunit))
        else:
            plt.ylabel(self._ylabel)

	# max number of ticks
	plt.locator_params(nbins=7)
	
        if self.xlogscale:
            self.ax.set_xscale('log')
        if self.ylogscale:
            self.ax.set_yscale('log')
        ax_r = plt.gca() #for each axis or whichever axis you want you should
	
        legend = False
	for plti in self._plots:
	    if len(plti)==3:
	        (x, y, parameters) = plti
	        plt.plot(x, y, **parameters)
	    elif len(plti)==4:
	        (x, y, linespec, parameters) = plti
	        plt.plot(x, y, linespec, **parameters)
            if 'label' in parameters: legend = True
        if len(self._plots)>0 and (force or not(isfile(self.filename))):
            if legend:
                plt.legend(loc=0, prop={'size':self.fontsize})
     	        # transparent legend
                leg = self.ax.legend(loc='best', fancybox=False)
                leg.get_frame().set_alpha(0.5)  
            plt.draw()
	    plt.savefig(self.filename, dpi=self.dpi)
        plt.close(self.fig)
	return self.filename, self._caption

      

if __name__ == '__main__':

    from libarray import *
    a = array([1,2,3,4,5,6,7,8,9,10])
    b = sin(a)*1e-7
    c = a+0.5
    d = cos(c)*1e-7

    x = plot(xlabel='x', ylabel='y', xunit='', yunit='')
    x.plot([a, b], color='r', label='toto')
    x.scatter([c, d], color='r', label='toto')
    x.savefig('totox.png')
    

		
	    


    
