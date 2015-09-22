import cma
from time import time, strftime
from collections import OrderedDict

def tf(X, bounds):
    # rescale X-values between 0 to 1
    Y = []
    for x, (xmin, xmax) in zip(X, bounds):
        slope = 1./(xmax-xmin)
        intercept = 1.0-slope*xmax
        y = slope*x + intercept
        Y.append(y)
    return Y

def tfinv(Y, bounds):
    # unscale 0 to 1 values to X-values
    X = []
    for y, (xmin, xmax) in zip(Y, bounds):
        slope = xmax-xmin
        intercept = xmax-slope
        x = slope*y + intercept
        X.append(x)
    return X

def fmin_cma_es( func, x0, args, bounds, sigma0=0.1, tolx=1e-3, seed=1234, 
                 maxiter='100+50*(N+3)**2//popsize**0.5', verbose=-1, 
                 maxfevals=float('inf'), popsize='4+int(3*log(N))', tolfun=1e-5, keys=None ):
    # init
    now = time()
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
    error = func(x0)
    xbest = x0
    best_objective = error

    print 'Start CMA-ES Optimizer...'
    print
    print '{step:>6}{residual:>11}{x}'.format(step='step', x='{:>11}'*len(x0), residual='residual').format(*keys)
    print '-'*(6+11+11*len(keys))
    print '{step:>6}{residual:>11.3e}{x}'.format(step=0, x='{:>11.3e}'*len(x0), residual=error).format(*x0)

    while not es.stop():
        solutions = es.ask() # provide a set of variables values

        objectives = [] # init
        for i, x in enumerate(solutions):

            xt = tfinv(x, bounds)
            error = func(xt)
            objectives.append( error )

            # if error is better then update fmin.x
            if error < best_objective:
                xbest.update(xt)
                best_objective = error

        es.tell(solutions, objectives)

        if es.countiter%10==0:
            print
            print '{step:>6}{residual:>11}{x}'.format(step='step', x='{:>11}'*len(keys), residual='residual').format(*keys)
            print '-'*(6+11+11*len(variables))

        indx = objectives.index(min(objectives))
        x = tfinv(solutions[indx], bounds)
        isbest = ''
        if objectives[indx] == best_objective:
            isbest = '*'
	print '{step:>6}{residual:>11.3e}{x} {isbest}'.format(step=es.countiter, x='{:>11.3e}'*len(x), residual=objectives[indx], isbest=isbest).format(*x)

    xbest, f_xbest, evaluations_xbest, evaluations, iterations, pheno_xmean, effective_stds = es.result()
    stop = es.stop()
    print
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
    return xbest
        

