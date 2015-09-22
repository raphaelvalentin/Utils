from functions.science import rms, mae, average, nan, inf
from collections import OrderedDict
from rawdata.table import table
from numpy import array, log10
import cma
from time import time, strftime

__all__ = ['fmin', 'optimbox', 'box', 'array', 'log10', 'rms', 'mae', 'average', 'nan', 'inf']

def box(x, y, xmin=-inf, xmax=inf, ymin=-inf, ymax=inf):
    xs, ys = [], []
    for xi, yi in zip(x, y):
        if xmin<=xi<=xmax and ymin<=yi<=ymax:
            xs.append(xi)
            ys.append(yi)
    return array(xs), array(ys)


class optimbox(object):
    """optimbox is a class used for fitting curves and linked with the fmin decorator.
       as input, it must contains a dictionary with the keys 'objective', 'goal'.
       it can contain optionally the keys 'xlim', 'ylim', 'weight', 'yscale'.
       if yscale is set to 'lin' (default), the error calculation is done by weight*(objective-goal)  
       if yscale is set to 'log', the fit is done by weight*(objective-goal)/goal.
       if weight is not defined, weight is calculated when yscale='lin' as mae(goal)
       if weight is not defined, weight is set when yscale='log' as 1.0.
       the optimbox's error is returned using the class function self.error().
       self.error() is used in fmin.
    """


    def mean(self, x):
        return mae(x)

    def __init__(self, kwargs):
        self._error = 0.0
        if 'objective' in kwargs and 'goal' in kwargs:
            x1, y1 = kwargs['objective']
            x2, y2 = kwargs['goal']
        else:
            raise Exception('instances for the optimbox are not correct')
        yscale = kwargs.get('yscale', 'lin')
        xmin, xmax = kwargs.get('xlim', (-inf, inf))
        ymin, ymax = kwargs.get('ylim', (-inf, inf))
        x1, y1 = box(x1, y1, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)
        x2, y2 = box(x2, y2, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)
        if yscale == 'lin':
            weight = kwargs.get('weight', self.mean(y2))
            if hasattr(weight, '__iter__'):
                raise Exception('weight cannot be a list of values')
            error = weight*(y1-y2)
            if hasattr(error, '__iter__'):
                self._error = self.mean(error)
            else:    
                self._error = abs(error)
        elif yscale == 'log':
            weight = kwargs.get('weight', 1.0)
            if hasattr(weight, '__iter__'):
                raise Exception('weight cannot be a list of values')
            try:
                error = weight*(y1-y2)/y2
            except ZeroDivisionError:
                ZeroDivisionError('at least one point of the scatter data is zero')
            if hasattr(error, '__iter__'):
                self._error = self.mean(error)
            else:    
                self._error = abs(error)

    def error(self):
        return self._error




class fmin(object):

    x = OrderedDict() # ordered dictionary
    bounds = OrderedDict() # ordered dictionary

    def __init__(self, method='cma-es', **options):
        """fmin is a function decorator used for minimization of function.
        options: 
            for method = 'cma-es'
                variables = 'all'
                sigma0 = 0.1
                tolx = 1e-3
                tolfun = 1e-5
                seed = 1234
                maxiter = '100 + 50*(N+3)**2 // popsize**0.5'
                maxfevals = inf
                popsize = '4 + int(3*log(N))'
                verbose = -1
                fmin.x <- dict 
                fmin.bounds <- dict 
        """
        self.method = method
        self.options = options


    def __call__(self, func):

        if self.method == 'cma-es':
            results = self._fmin_cma_es(func=func, **dict(self.options))
        return results


    def _fmin_cma_es(self, func, variables='all', sigma0=0.1, tolx=1e-3, seed=1234, 
                          maxiter='100+50*(N+3)**2//popsize**0.5', verbose=-1, 
                          maxfevals=float('inf'), popsize='4+int(3*log(N))', tolfun=1e-5 ):

        now = time()
        def tf(X, bounds):
            Y = []
            for x, (xmin, xmax) in zip(X, bounds):
                slope = 1./(xmax-xmin)
                intercept = 1.0-slope*xmax
                y = slope*x + intercept
                Y.append(y)
            return Y

        def tfinv(Y, bounds):
            X = []
            for y, (xmin, xmax) in zip(Y, bounds):
                slope = xmax-xmin
                intercept = xmax-slope
                x = slope*y + intercept
                X.append(x)
            return X

        def eval_error(output):
            if isinstance(output, dict):
                return optimbox(output).error()
            elif isinstance(output, (float, int)):
                return float(abs(output))
            elif isinstance(output, tuple):
                return average([ eval_error(elt) for elt in output ])
            elif hasattr(output, '__iter__'):
                return mae(output)
            else:
                raise Exception('output must be based on optimbox, float, tuple or list/array')
                

        # init
        if variables == 'all':
            variables = fmin.x.keys()
        x0 = [fmin.x[key] for key in variables]
        bounds = [fmin.bounds[key] for key in variables]

        options = { 'boundary_handling' : 'BoundTransform ',
                    'bounds' : [[0]*len(x0), [1]*len(x0)], 
                    'seed' : seed,
                    'verb_time' : False, 
                    'scaling_of_variables' : None,
                    'verb_disp' : 1,
                    'maxiter' : maxiter,  
                    'maxfevals' : maxfevals,  
                    'signals_filename' : 'cmaes_signals.par',  
                    'tolx' : tolx,
                    'popsize' : popsize,
                    'verbose' : verbose,
                    'ftarget': 1e-12,
                    'tolfun' : 1e-5,
                 }

        es = cma.CMAEvolutionStrategy(tf(x0, bounds), sigma0, options)

        # initial error with the original set of variables values
        error = eval_error( func(**fmin.x) )
        best_objective = error

        print 'Start CMA-ES Optimizer...'
        print
        print '{step:>6}{residual:>11}{x}'.format(step='step', x='{:>11}'*len(variables), residual='residual').format(*variables)
        print '-'*(6+11+11*len(variables))
	print '{step:>6}{residual:>11.3e}{x}'.format(step=0, x='{:>11.3e}'*len(x0), residual=error).format(*x0)

        while not es.stop():
            solutions = es.ask() # provide a set of variables values

            objectives = [] # init
            for i, x in enumerate(solutions):

                xt = { k:v for k, v in zip(variables, tfinv(x, bounds)) }

                # add other keyword arguments
                for key in fmin.x.keys():
                    if not(key in variables):
                        xt[key] = fmin.x[key]

                error = eval_error( func(**xt) )
                objectives.append( error )

                # if error is better then update fmin.x
                if error < best_objective:
                    fmin.x.update(xt)
                    best_objective = error

            es.tell(solutions, objectives)
            #es.disp(1)

            if es.countiter%10==0:
                print
                print '{step:>6}{residual:>11}{x}'.format(step='step', x='{:>11}'*len(variables), residual='residual').format(*variables)
                print '-'*(6+11+11*len(variables))

            indx = objectives.index(min(objectives))
            x = tfinv(solutions[indx], bounds)
            isbest = ''
            if objectives[indx] == best_objective:
                isbest = '*'
	    print '{step:>6}{residual:>11.3e}{x} {isbest}'.format(step=es.countiter, x='{:>11.3e}'*len(x), residual=objectives[indx], isbest=isbest).format(*x)


        #es.result_pretty()
        xbest, f_xbest, evaluations_xbest, evaluations, iterations, pheno_xmean, effective_stds = es.result()
        stop = es.stop()
        print '-----------------'
        print 'termination on %s=%.2e'%(stop.keys()[0], stop.values()[0])
        print 'bestever f-value: %r'%(f_xbest)
        print 'incumbent solution: %r'%(list(tfinv(xbest, bounds)))
        print 'std deviation: %r'%(list(effective_stds))
        print 'evaluation func: %r'%(evaluations)
        
        print 'total time:', 
        minutes = int((time()-now)/60)
        if minutes>1:
            print "%d minutes"%(minutes),
        elif minutes>0:
            print "%d minute"%(minutes),
        print "%d seconds"%((time()-now)-minutes*60)
        


