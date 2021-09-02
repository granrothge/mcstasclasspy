import numpy as np
import matplotlib.pyplot as plt
import functools
from .DataMCCode import DataMcCode

def check_type(func):
    functools.wraps(func)
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
        self.title = ''
        self.xlabel = ''
        self.ylabel = ''

        self.xvar = ''
        self.xlimits = () # pair

        self.variables = []

        self.yvar = () # pair
        self.values = () # triplet
        self.statistics = ''

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

    def errorbar(self, ax=None, **kwargs):
        """
        plot an errorbar plot
        """
        if ax == None:
            fig, ax = plt.subplots()
        im = ax.errorbar(self.xvals, self.yvals, self.y_err_vals, **kwargs)
        self._add_titles(ax)
        return im

    def plot(self, ax=None, **kwargs):
        """plot an x y plot"""
        if ax==None:
            fig, ax = plt.subplots()
        im = ax.plot(self.xvals, self.yvals, **kwargs)
        self._add_titles(ax)
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