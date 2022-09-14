import numpy as np
import matplotlib.pyplot as plt
import functools
import copy
import h5py
import datetime
from .DataMCCode import DataMcCode
from .Data1D import Data1D
from .utils import plt_func_wrap

def check_type(func):
    @functools.wraps(func)
    def _wrapper(*args,**kwargs):
        if not isinstance(args[1], (Data2D, float, int)):
            raise RuntimeError("other must be a 2D instance or a constant")
        return func(*args,**kwargs)
    return _wrapper

def checkdims(func):
    @functools.wraps(func)
    def _wrapper(*args,**kwargs):
        if isinstance(args[1],(Data2D)):
            if  args[1].xylimits!=args[0].xylimits:
                raise RuntimeError("x and y limits do not match")
            if np.array(args[1].zvals).shape!=np.array(args[0].zvals).shape:
                raise RuntimeError("x and y dimensions do not match")
        return func(*args,**kwargs)
    return _wrapper               

class Data2D(DataMcCode):
    ''' PSD data type '''

    def __init__(self):
        super(Data2D, self).__init__()

        self.component = ''
        self.filename = ''
        self.title = ''

        self.xlabel = ''
        self.ylabel = ''

        self.xvar = ''
        self.yvar = ''
        self.zvar = ''
        self.xylimits = ()  # quadruple

        self.values = ()  # triplet
        self.statistics = ''  # quadruple
        self.signal = ''

        # data references
        self.zvals = []
        self.counts = []
        self.errors = []
        self.mask = []

    @checkdims
    @check_type    
    def __add__(self,other):
        """
        add 2 1d instances together or add a constant
        """
        
        outdat = copy.deepcopy(self)
        if isinstance(other,Data2D):
            outdat.title = '{}+{}'.format(self.title,other.title)
            outdat.zvals = list(np.array(self.zvals) + np.array(other.zvals))
            outdat.errors = list(np.sqrt(np.array(self.errors)**2+np.array(other.errors)**2))
        else:
            outdat.zvals = np.array(self.zvals) + other
            outdat.errors =self.errors 
        return outdat

    def get_stats_title(self):
        '''I=.... Err=... N=...; X0=...; dX=...;'''
        stitle = '%s=%e Err=%e N=%d' % (self.zvar, self.values[0],
                                        self.values[1], self.values[2])
        return stitle

    def __str__(self):
        return 'Data2D, ' + self.get_stats_title()

    @plt_func_wrap
    def pcolor(self, ax=None, **kwargs):
        """ make a pcolor plot of a 2D mcstas monitor """
        xvals, yvals = self.createxyvec()
        im = ax.pcolor(xvals, yvals, self.zvals, **kwargs)
        return im

    @plt_func_wrap
    def contourf(self,ax=None, **kwargs):
        """ make a colorf plot of a 2D mcstas monitor """
        xvals,yvals =self.createxyvec(bin_bounds=False)
        im = ax.contourf(xvals, yvals, np.array(self.zvals), **kwargs)
        return im
    
    @plt_func_wrap
    def contour(self,ax=None, **kwargs):
        """ make a colorf plot of a 2D mcstas monitor """
        xvals,yvals =self.createxyvec(bin_bounds=False)
        im = ax.contour(xvals, yvals, np.array(self.zvals), **kwargs)
        return im

    def createxyvec(self,bin_bounds=True):
        """
        create a vector for the x and y coordinates from a 2D class
        bin_bounds: If true calculate the boundaries of the bins
                    If false calculate the centers of the bins
        """
        zarr = np.array(self.zvals)
        zshp = zarr.shape
        xvec = np.linspace(self.xylimits[0], self.xylimits[1], zshp[1]+1)
        yvec = np.linspace(self.xylimits[2], self.xylimits[3], zshp[0]+1)
        if not bin_bounds:
            xvec = (xvec[1:]+xvec[:-1])/2
            yvec = (yvec[1:]+yvec[:-1])/2
        return xvec, yvec

    def cut(self, cutdir, cutcen, cutwidth, xlims=None):
        """ cut a 2D McStas data set into a 1D data set
            cutdir: must be 'x' or 'y'
            cutcen: center in other direction
            cutwidth: width in other direction
            xlims: limits in new x direction, default = None which uses full length

        """
        xylimits = self.xylimits
        xylimits_idx = np.zeros(4, dtype=int)
        xylimitsidx_dict = {'x': [2, 3], 'y': [0, 1]}
        xyvar_dict = {'x': self.xvar, 'y': self.yvar}
        xylabel_dict = {'x': self.xlabel, 'y': self.ylabel}
        xylimits_dict = {'x': self.xylimits[:2], 'y': self.xylimits[2:]}
        zaxes_dict = {'x': 1, 'y': 0}
        int_dir = np.lib.arraysetops.setxor1d(cutdir, np.array(list(xyvar_dict.keys())))[0]
        #print(int_dir)
        data = Data1D()
        data.component = "cut from {}".format(self.filename)
        data.filename = self.filename
        data.title = "${}\pm{}$ in {}".format(cutcen, cutwidth/2, int_dir)
        data.xvar = xyvar_dict[cutdir]
        data.xlabel = xylabel_dict[cutdir]
        xvals, yvals = self.createxyvec()
        xyvals_dict = {'x': xvals, 'y': yvals}
        zvals = np.array(self.zvals)
        errvals = np.array(self.errors)
        if xlims == None:
            data.xlimits = xylimits_dict[cutdir]
            xmin_idx = 0
            xmax_idx = len(xyvals_dict[cutdir])-1
        else:
            xmin_idx = np.where(xyvals_dict[cutdir] < xlims[0])[0].max()
            xmax_idx = np.where(xyvals_dict[cutdir] > xlims[1])[0].min()
            data.xlimits = (xyvals_dict[cutdir][xmin_idx], xyvals_dict[cutdir][xmax_idx])
        xylimits_idx[xylimitsidx_dict[cutdir]] = [xmin_idx, xmax_idx]  # set index limits along the cut direction
        data.yvar = self.zvar
        try:
            cut_min_idx = np.where(xyvals_dict[int_dir] < (cutcen-cutwidth/2.0))[0].max()
            cut_max_idx = np.where(xyvals_dict[int_dir] > (cutcen+cutwidth/2.0))[0].min()
        except ValueError:
            raise Exception('''check to see that the width is not ouside
            the maximum limits of the data''')
        xylimits_idx[xylimitsidx_dict[int_dir]] = [cut_min_idx, cut_max_idx] # set index limits along the integration direction
        # print (xylimits_idx)
        # note need to convert bin boundaries to centers for 1D data set.
        data.xvals = np.array((xyvals_dict[cutdir][xmin_idx:(xmax_idx)]+xyvals_dict[cutdir][(xmin_idx+1):xmax_idx+1]))/2
        data.yvals = np.array(np.sum(zvals[xylimits_idx[0]:xylimits_idx[1], xylimits_idx[2]:xylimits_idx[3]],axis=zaxes_dict[int_dir]))
        inerrors = errvals[xylimits_idx[0]:xylimits_idx[1], xylimits_idx[2]:xylimits_idx[3]]
        data.y_err_vals = np.array(np.sqrt(np.sum(inerrors*inerrors, axis=zaxes_dict[int_dir])))

        return data

    def save_MDHisto(self,filename):
        """ Saves the data to an MD Histo Slice"""
        with h5py.File(filename, 'w') as fh:
            fh.attrs['HDF5_Version'] = '{}.{}.{}'.format(*(list(h5py.h5.HDF5_VERSION_COMPILED_AGAINST)))
            fh.attrs['NeXus_version'] = '4.4.3' 
            fh.attrs['file_time'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')
            #fh.attrs['h5py_version'] = h5py.__version__
            fh.create_group('MDHistoWorkspace')
            fh['MDHistoWorkspace'].attrs['NX_class'] = 'NXentry'
            fh['MDHistoWorkspace'].attrs['Qconvention'] = 'Inealstic'
            fh['MDHistoWorkspace'].attrs['SaveMDVersion'] = 2
            rt = fh['MDHistoWorkspace'].create_group('data')
            rt.attrs['NX_class'] = 'NXdata'
            rt.create_dataset("signal", data=self.zvals)
            rt.create_dataset("errors_squared", data = self.errors*self.errors)
            rt.create_dataset("mask",data=self.mask)
            rt.create_dataset("num_events", data = np.zeros(self.zvals.shape))
            xvec,yvec = self.createxyvec()
            rt.create_dataset(self.xvar,data = xvec)
            rt.create_dataset(self.yvar,data = yvec)
            axses = {self.xvar:self.xlabel,self.yvar:self.ylabel}
            for ax in axses.keys():
                rt[ax].attrs['long_name'] = ax
                if ax.find('E')>0:
                    rt[ax].attrs['frame']= 'General Frame'   
                elif (ax.find('H')>0) or (ax.find('K')>0) or (ax.find('K')>0) :
                    rt[ax].attrs['frame'] = 'HKL'
                rt[ax].attrs['units'] = axses[ax].split('[')[1].split(']')[0]
            axsstr = "{}:{}".format(self.xvar,self.yvar)
            rt['signal'].attrs['axes'] = axsstr
            rt['signal'].attrs['signal'] = 1
            fh['MDHistoWorkspace'].create_dataset('visual_normalization',data=0.0)
            



