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
from functions.science import linspace

__all__ = ['smithchart']


from math import floor, log10, pi
import math
import cmath
inf = float('inf')



class smithchart(object):
    def __init__(self, **kwargs):
        self.dpi = kwargs.get('dpi', 100)
        self._caption = kwargs.get('caption', '')
        self.figsize = kwargs.get('figsize', (8, 6))
        self._xlabel = kwargs.get('xlabel', '')
        self._ylabel = kwargs.get('ylabel', '')
        self.fontsize = kwargs.get('fontsize', 19)
	self._labels = list()
	self._plots = list()
        self.filename = kwargs.get('filename', 'image.png')
        self.PY_GRAPH_DIR = os.environ.get('PY_GRAPH_DIR', '')

        self.draw_cadran()

    def xlabel(self, label):
        self._xlabel = label
    def ylabel(self, label):
        self._ylabel = label
    def caption(self, caption):
        self._caption = caption

    def draw_cadran(self):
        grain=500.
        # quart de cercles a S constant
        Teta=linspace(0.,pi/2,step=pi/grain/2.)
        S=[5., 2.,1.,0.5, 0.2,-0.2, -0.5,-1.,-2.,-5, 0.]
        for s in S:
            data=[]
            R=np.tan(Teta)
            for r in R:
                d=(r+1.)**2+s**2
                x=((r*r-1.)+s*s)/d
                y=2*s/d
                pt = complex(x,y)
                if abs(pt)<1:
                    data.append(pt)
            self.plot(np.array(data),color='grey', linestyle=':', linewidth=1)

        # trace de l'abaque
        # cercles a r constant
        Teta=linspace(-pi/2.,pi/2.,step=pi/grain/2.)
        S=np.tan(Teta)
        R=[0.1, .3,0.6, 1.,2., 3.,10., 0.]
        for r in R:
            data=[]
            for s in S:
                d=s**2+(r+1.)**2
                x=(s**2+(r**2-1.))/d
                y=2.*(s/d)
                data.append(complex(x,y))
            if r==0.:
                self.plot(np.array(data),color='black')
            else:    
                self.plot(np.array(data),color='grey', linestyle=':', linewidth=1)
        # ticks
        s = 0.0
        R=[0.1, 0.2, 0.3,0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.2, 1.4, 1.6,1.8,2.0, 3., 4., 5., 10, 20]
        for r in R:
            data=[]
            d=s**2+(r+1.)**2
            x=(s**2+(r**2-1.))/d
            y=2.*(s/d)
            data.append(complex(x,y+0.01))
            data.append(complex(x,y-0.01))
            self.plot(np.array(data),color='black', linestyle='-', linewidth=1.5)
        #
        self.plot(np.array([complex(-1,0), complex(1,0)]),color='black', linestyle='-', linewidth=1.5)
        #
        S = [0.0, 0.1, 0.2, 0.3,0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.2, 1.4, 1.6,1.8,2.0, 3., 4., 5., 10, 20]
        S += [-0.1, -0.2, -0.3,-0.4, -0.5, -0.6, -0.7, -0.8, -0.9, -1, -1.2, -1.4, -1.6,-1.8,-2.0, -3., -4.,-5., -10, -20]
        for s in S:
            data=[]
            r=0
            d=(r+1.)**2+s**2
            x=((r*r-1.)+s*s)/d
            y=2*s/d
            pt = complex(x,y)
            m, phi = cmath.polar(pt)
            pt = cmath.rect(m*1.03, phi)
            x, y = pt.real, pt.imag
            pt1 = cmath.rect(m-0.02, phi)
            pt2 = cmath.rect(m, phi)
            data = [pt1, pt2]
            self.plot(np.array(data),color='black', linestyle='-', linewidth=1.5)

    def annotate(self, plt):
        R=[0.1, 0.2, 0.3,0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.2, 1.4, 1.6,1.8,2.0, 3., 4., 5., 10, 20]
        for r in R:
            data=[]
            s = 0.0
            d=s**2+(r+1.)**2
            x=(s**2+(r**2-1.))/d
            y=2.*(s/d)
            data.append(complex(x,y+0.01))
            data.append(complex(x,y-0.01))
            plt.annotate(str(r), xy=(x, y+0.07), size=10, rotation=90, va="center", ha="center", )
        #
        S = [0.0, 0.1, 0.2, 0.3,0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.2, 1.4, 1.6,1.8,2.0, 3., 4., 5., 10, 20]
        for s in S:
            data=[]
            r=0
            d=(r+1.)**2+s**2
            x=((r*r-1.)+s*s)/d
            y=2*s/d
            pt = complex(x,y)
            m, phi = cmath.polar(pt)
            m = m*1.04
            pt = cmath.rect(m, phi)
            x, y = pt.real, pt.imag
            plt.annotate(str(s), xy=(x, y), size=10, va="center", ha="center", rotation=phi*180/pi-90 )
        S = [-0.1, -0.2, -0.3,-0.4, -0.5, -0.6, -0.7, -0.8, -0.9, -1, -1.2, -1.4, -1.6,-1.8,-2.0, -3., -4.,-5., -10, -20]
        for s in S:
            data=[]
            r=0
            d=(r+1.)**2+s**2
            x=((r*r-1.)+s*s)/d
            y=2*s/d
            pt = complex(x,y)
            m, phi = cmath.polar(pt)
            m = m*1.05
            pt = cmath.rect(m, phi)
            x, y = pt.real, pt.imag
            plt.annotate(str(s), xy=(x, y), size=10, va="center", ha="center", rotation=phi*180/pi+90 )



    def plot(self, c, **kwargs):
        if not 'linewidth' in kwargs:
	    kwargs['linewidth'] = 2
        if 'label' in kwargs:
	    if kwargs['label'] in self._labels:
                del kwargs['label']
	    else:
		self._labels.append(kwargs['label'])
        self._plots.append([c.real, c.imag, kwargs])

    def scatter(self, c, **kwargs):
        markeredgecolor = kwargs.pop('color', 'r')
	markersize = kwargs.pop('size', 6)
        properties = {'marker':'s', 'markersize':markersize, 'linewidth':0, 
                      'markerfacecolor':'none', 'markeredgecolor':markeredgecolor, 'markeredgewidth':2
                     }
	properties.update(**kwargs)
	self.plot(c, **properties)

    def savefig(self, filename=None, dpi=100, force=True):
        if filename == None:
            filename = tempfile.mktemp(dir=self.PY_GRAPH_DIR, suffix='.png')
        self.filename = filename
	self.dpi = dpi
	
	# generation of the image
        plt.rc('font', family='sans-serif',  size=self.fontsize)
        plt.rc('figure', figsize=(8,6))
        plt.rc('figure', dpi=self.dpi)
        plt.rc('figure.subplot', left=0.00, bottom=0.00, right=1.0, top=1.0, wspace=0.001, hspace=0.1)
        plt.rc('lines', markersize=6)
        plt.rc('axes', labelsize=self.fontsize)
        plt.rc('axes', color_cycle=('red', 'blue', 'green', 'black', 'grey', 'yellow'))
        plt.rc('axes', grid=False)
        plt.rc('axes', linewidth=0)
        plt.rc('xtick.major', size=8)           # major tick size in points
        plt.rc('xtick.minor', size=5)           # minor tick size in points
        plt.rc('xtick.major', width=0)        # major tick width in points
        plt.rc('xtick.minor', width=0)        # minor tick width in points
        plt.rc('xtick.major', pad=4)            # distance to major tick label in points
        plt.rc('xtick', color='k')                # color of the tick labels
        plt.rc('xtick', labelsize=0)       # fontsize of the tick labels
        plt.rc('xtick', direction='in')           # direction: in, out, or inout
        plt.rc('ytick.major', size=1)           # major tick size in points
        plt.rc('ytick.minor', size=1)           # minor tick size in points
        plt.rc('ytick.major', width=0)        # major tick width in points
        plt.rc('ytick.minor', width=0)        # minor tick width in points
        plt.rc('ytick', labelsize=0)       # fontsize of the tick labels

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1,1,1)
        self.ax.set_xlim(-1.15,1.15)
        self.ax.set_ylim(-1.15,1.15)
        plt.axes().set_aspect('equal', 'datalim')
        plt.axis('off')

        self.ax.set_axis_off()


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
            self.annotate(plt)
            plt.draw()
	    plt.savefig(self.filename, dpi=self.dpi)
        plt.close(self.fig)
	return self.filename, self._caption



if __name__ == '__main__':
    from numpy import array
    plot1 = smithchart(xlabel='s11')
    
    s = array([ complex(-0.577832859,-0.631478424),
                complex(-0.872221469,0.175553879),
                complex(-0.27989901,0.848322599),
                complex(0.625836677,0.630661307),
                complex(0.833655352,-0.25903236),
                complex(0.200238299,-0.876183465),
                complex(0.091123769,-0.706343188),
                complex(0.511222482,-0.249041717),
                complex(0.385652964,0.223033934),
                complex(-0.045832001,0.354777424),
                complex(-0.245491847,0.136919746),
                complex(-0.193731962,-0.091411262),
                complex(-0.151810832,0.097273845),
                complex(0.007344177,0.147523939),
                complex(0.107016177,0.034567346),
                complex(0.057517023,-0.062991385),
                complex(-0.029108675,-0.061496518),
                complex(0.002598262,-0.004237322) ])

    plot1.plot(s, label='model')
    plot1.scatter(s, label='meas.')
    plot1.savefig('toto.jpg')
    


