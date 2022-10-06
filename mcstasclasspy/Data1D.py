import numpy as np
import matplotlib.pyplot as plt
import functools
from .DataMCCode import DataMcCode
from .utils import plt_func_wrap
import lmfit

def check_type(func):
    @functools.wraps(func)
    def _wrapper(*args,**kwargs):
        if not isinstance(args[1], (Data1D, float, int)):
            raise RuntimeError("other must be a 1D instance or a constant")
        return func(*args,**kwargs)
    return _wrapper

class Data1D(DataMcCode):
    ''' 1d plots use this data type '''
    def __init__(self):
        super(Data1D, self).__init__()

        self.component = ''
        self.filename = ''
        self.xvar = ''
        self.xlimits = () # pair

        self.variables = []

        self.yvar = () # pair
        self.values = () # triplet
        
        # data references
        self.xvals = []
        self.yvals = []
        self.y_err_vals = []
        self.Nvals = []

    @check_type
    def __truediv__(self, other):
        """
        divide by a 1D instance or a constant
        """
        outdat = Data1D()
        outdat.xvals = self.xvals
        outdat.xlabel = self.xlabel
        if isinstance(other, Data1D):
            outdat.title = '{}/{}'.format(self.title,other.title)
            outdat.yvals = self.yvals/other.yvals
            outdat.y_err_vals = outdat.yvals*np.sqrt((self.y_err_vals/self.yvals)**2 +
                                                     (other.y_err_vals/other.yvals)**2)
        else:
            outdat.yvals = self.yvals/other
            outdat.y_err_vals = self.y_err_vals/other
        return outdat

    @check_type
    def __mul__(self, other):
        """
        multiply by a 1D instance or a constant
        """
        outdat = Data1D()
        outdat.xvals = self.xvals
        outdat.xlabel = self.xlabel
        if isinstance(other, Data1D):
            outdat.title = '{}*{}'.format(self.title,other.title)
            outdat.yvals = self.yvals * other.yvals
            outdat.y_err_vals = outdat.yvals*np.sqrt((self.y_err_vals/self.yvals)**2 +
                                                     (other.y_err_vals/other.yvals)**2)
        else:
            outdat.yvals = self.yvals * other
            outdat.y_err_vals = self.y_err_vals * other
        return outdat

    @check_type
    def __add__(self,other):
        """
        add 2 1d instances together or add a constant
        """
        
        outdat = Data1D()
        outdat.xvals = self.xvals
        outdat.xlabel = self.xlabel
        if isinstance(other,Data1D):
            outdat.title = '{}+{}'.format(self.title,other.title)
            outdat.yvals = self.yvals + other.yvals
            outdat.y_err_vals = np.sqrt(self.y_err_vals**2+other.y_err_vals**2)
        else:
            outdat.yvals = self.yvals + other
            outdat.y_err_vals =self.y_err_vals 
        return outdat
    
    @check_type
    def __sub__(self,other):
        """
       subtract 2 1d instances subtract a constant
        """
        outdat = Data1D()
        outdat.xvals = self.xvals
        outdat.xlabel = self.xlabel
        if isinstance(other,Data1D):
            outdat.title = '{}-{}'.format(self.title,other.title)
            outdat.yvals = self.yvals - other.yvals
            outdat.y_err_vals = np.sqrt(self.y_err_vals**2+other.y_err_vals**2)
        else:
            outdat.yvals = self.yvals - other
            outdat.y_err_vals =self.y_err_vals 
        return outdat

    def clone(self):
        data = Data1D()

        data.filepath = self.filepath

        data.component = self.component
        data.filename = self.filename
        data.title = self.title
        data.xlabel = self.xlabel
        data.ylabel = self.ylabel

        data.xvar = self.xvar
        data.xlimits = self.xlimits

        data.variables = self.variables

        data.yvar = self.yvar
        data.values = self.values
        data.statistics = self.statistics

        # data references
        data.xvals = self.xvals
        data.yvals = self.yvals
        data.y_err_vals = self.y_err_vals
        data.Nvals = self.Nvals

        return data

    def get_stats_title(self):
        '''I=.... Err=... N=...; X0=...; dX=...;'''
        try:
            stitle = '%s=%e Err=%e N=%d; %s' % (self.yvar[0], self.values[0], self.values[1], self.values[2], self.statistics)
        except:
            stitle = '%s of %s' % (self.yvar[0], self.xvar)
        return stitle

    def __str__(self):
        return 'Data1D, ' + self.get_stats_title()

    @plt_func_wrap 
    def errorbar(self,ax=None,**kwargs):
        """
        plot an errorbar plot
        """
        im = ax.errorbar(self.xvals, self.yvals, self.y_err_vals, **kwargs)
        return im

    @plt_func_wrap
    def plot(self, ax=None, **kwargs):
        """plot an x y plot"""
        im = ax.plot(self.xvals, self.yvals, **kwargs)
        return im

    def bin(self, binwidth):
        """
        rebins the data into bins of width binwidth
        """
        # Do we need to do type checking
        outcls = self.clone()
        xidx_sorted = np.argsort(self.xvals)
        x = np.array(self.xvals)[xidx_sorted]
        y = np.array(self.yvals)[xidx_sorted]
        e = np.array(self.y_err_vals)[xidx_sorted]

        # for storing the values to be combined
        xcombi = []
        ycombi = []
        ecombi = []
        # for storing the results
        xres = []
        yres = []
        eres = []

        for idx, xval in enumerate(x):
            if len(xcombi) > 0:
                if (xval-xcombi[0]) > binwidth:
                    xres.append(np.sum(xcombi)/len(xcombi))
                    yres.append(np.sum(ycombi)/len(xcombi))
                    eres.append(np.sqrt(np.sum(np.array(ecombi)*np.array(ecombi)))/len(xcombi))
                    xcombi = [xval]
                    ycombi = [y[idx]]
                    ecombi = [e[idx]]
            else:
                xcombi.append(xval)
                ycombi.append(y[idx])
                ecombi.append(e[idx])
        # handle last point
        if len(xcombi) > 0:
            xres.append(np.sum(xcombi)/len(xcombi))
            yres.append(np.sum(ycombi)/len(xcombi))
            eres.append(np.sqrt(np.sum(np.array(ecombi)*np.array(ecombi)))/len(xcombi))
        outcls.xvals = np.array(xres)
        outcls.yvals = np.array(yres)
        outcls.y_err_vals = np.array(eres)
        outcls.title = outcls.title+" binned to {}".format(binwidth)
        outcls.xlimits = (np.min(xres), np.max(xres))
        return outcls

    def peakstats(self):
        """
        Calculate statistics assuming there is a peak.
        returns total area, center, and width
        """
        area = np.sum(self.yvals)
        center = np.sum(self.yvals*self.xvals)/np.sum(self.yvals)
        wid = np.sqrt(np.sum(self.yvals*(self.xvals-center)**2)/np.sum(self.yvals))
        return(area, center, wid)
    
    def setup_fit(self,model_fun,**kwargs):
        """ setup a Model and its fit parameters"""
        self.fmodel = lmfit.Model(model_fun)
        self.fparams = self.model.make_params(**kwargs)
    
    def fit(self, nonzeroerr=True, useerr=True,**kwargs):
        """perform a fit using lmfit
        by default only points with non zero error will be included in the fit """

        if (self.fmodel==None) or (self.fparams==None):
            raise RuntimeError("Run setup_fit to define a model first")
        x = np.array(self.xvals)
        y = np.array(self.yvals)
        yerr = np.array(self.y_err_vals)
        fbl = np.full(len(x),True) 
        if nonzeroerr:
            fbl =  yerr>0
        if useerr:  
            self.fresult = self.fmodel.fit(y[fbl],self.fparams,x=x[fbl],
                                           weights=1/yerr[fbl],**kwargs)
        else:
            self.fresult = self.fmodel.fit(y[fbl],self.fparams,x=x[fbl],
                                           **kwargs)
    
    
    def get_parm_val(parmobj):
        """
        get a parameter value and its error from a lmfit result object
        if there is no stderr field return a nan.
        """
        vout = parmobj.value
        try:
            errout = parmobj.stderr
        except:
            errout = np.nan
        return vout, errout
    
    def res_str(res):
        """ Given a result object from lmfit format the parameters for output
        and provide a string"""
        outstr = ''
        for ky in res.params.keys():
            pval, perr = get_parm_val(res.params[ky])
            try:
                if np.isfinite(perr):
                    outstr += '${} = {:.5e}\pm{:.2e}$\n'.format(ky, pval, perr)
                else:
                    outstr += '${} = {:.5e}\pm${}\n'.format(ky, pval, perr)
            except:
                outstr += '${} = {:.5e}\pm${}\n'.format(ky, pval, perr)
        outstr += '$\chi^2$ = {:.2f}'.format(res.redchi)
        return outstr

    def plot_fit(self,npts=None,
                 sp_kw={'figsize':(10,6),'gridspec_kw':{'width_ratios': [1, 2]}}):
        """plot data and resultant fit """
        if self.fresult==None:
            raise RuntimeError("A fit must be performed first")
        fig,ax = plt.subplots(ncols=2, **sp_kw)
        self.errorbar(ax=ax[1],fmt='bo')
        xt = np.array(self.xvals)
        if npts==None:
            npts=len(xt)*3
        xev = np.linspace(xt.min(),xt.max(),npts)
        ax[1].plot(xev,self.fmodel.eval(self.fresult.params,x=xev),'r')
        ax[0].axis('off')
        ax[0].text(0.01,0.99,self.fresult.fit_report(),
                   ha='left', va='top')
        return fig,ax


        
  
    