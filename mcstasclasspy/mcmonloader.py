# rework of mcploatloader.py for plotting single monitor data
# expand to also load histogram files
'''
functionality for loading mccode data into suitable data types,
and assembling it in a plot-friendly way.
'''
#from os import fchdir
import h5py
import re
from decimal import Decimal
import numpy as np
from .DataMCCode import DataMcCode
from .Data1D import Data1D
from .Data2D import Data2D

class Data0D(DataMcCode):
    pass


'''
Utility funcitons for loading and parsing mccode output files
'''
freetext_pat = '.+'

def _parse_monitor_common(data,text):
    try:
        '''# filename: Edet.dat'''
        m = re.search(r'# filename: ([\-\+\w\.\,]+)\n', text)
        if m:
            data.filename = m.group(1)
        else:
            data.filename = ''
        '''# component: Ldetector'''
        m = re.search(r'# component: ([\w\.]+)\n', text)
        if m:
            data.component = m.group(1)
        else:
            data.component = "(no comp name)"
        '''# title: Wavelength monitor'''
        m = re.search(r'# title: '+'({})'.format(freetext_pat)+r'\n', text)
        data.title = m.group(1)
        '''# values: 6.72365e-17 4.07766e-18 4750'''
        m = re.search(r'# values: ([\d\-\+\.e]+) ([\d\-\+\.e]+) ([\d\-\+\.e]+)\n', text)
        data.values = (Decimal(m.group(1)), Decimal(m.group(2)), float(m.group(3)))
    except Exception as e:
        print('Common Data load error.')
        raise e
    return data

def _parse_monitor_xylabel(data,text):
    try:
        '''# xlabel: Wavelength [AA]'''
        m = re.search(r'# xlabel: '+'({})'.format(freetext_pat)+r'\n', text)
        data.xlabel = m.group(1)
        '''# ylabel: Intensity'''
        m = re.search(r'# ylabel: '+'({})'.format(freetext_pat)+r'\n', text)
        data.ylabel = m.group(1)
    except Exception as e:
        print('xylabel Data load error.')
        raise e
    return data 

def _parse_0D_monitor(text):
    ''' populates data fields of new Data1D object using the text from a mccode data file '''
    data = Data0D()
    # load essential header data
    data = _parse_monitor_common(data,text)
    try:
        
        '''# statistics: X0=5.99569; dX=0.0266368;'''
        # m = re.search('\# statistics: X0=([\d\.\-\+e]+); dX=([\d\.\-\+e]+);\n', text)
        # data.statistics = 'X0=%.2E; dX=%.2E;' % (Decimal(m.group(1)), Decimal(m.group(2)))

        # load the actual data
        lines = text.splitlines()
        xvals = []
        yvals = []
        y_err_vals = []
        Nvals = []
        for l in lines:
            if '#' in l:
                continue
            vals = l.split()
            yvals.append(float(vals[0]))
            y_err_vals.append(float(vals[1]))
            Nvals.append(float(vals[2]))
        data.yvals = np.array(yvals)
        data.y_err_vals = np.array(y_err_vals)
        data.Nvals = Nvals

    except Exception as e:
        print('Data0D load error.')
        raise e

    return data

def _parse_1D_monitor(text):
    ''' populates data fields of new Data1D object using the text from a mccode data file '''
    data = Data1D()
     # load essential header data
    data = _parse_monitor_common(data,text)      
    data = _parse_monitor_xylabel(data,text)
    try:
        '''# xvar: L'''
        m = re.search(r'# xvar: ([\w]+)\n', text)
        data.xvar = m.group(1)
        '''# xlimits: 5.5 6.5'''
        m = re.search(r'# xlimits: ([\d\.\-\+e]+) ([\d\.\-\+e]+)\n', text)
        data.xlimits = (float(m.group(1)), float(m.group(2)))

        '''# yvar: (I,I_err)'''
        m = re.search(r'# yvar: \(([\w]+),([\w]+)\)\n', text)
        data.yvar = (m.group(1), m.group(2))

        '''# statistics: X0=5.99569; dX=0.0266368;'''
        m = re.search('\# statistics: X0=([\d\.\-\+e]+); dX=([\d\.\-\+e]+);\n', text)
        data.statistics = 'X0=%.2E; dX=%.2E;' % (Decimal(m.group(1)), Decimal(m.group(2)))

        # load the actual data
        lines = text.splitlines()
        xvals = []
        yvals = []
        y_err_vals = []
        Nvals = []
        for l in lines:
            if '#' in l:
                continue

            vals = l.split()
            xvals.append(float(vals[0]))
            yvals.append(float(vals[1]))
            y_err_vals.append(float(vals[2]))
            Nvals.append(float(vals[3]))

        data.xvals = np.array(xvals)
        data.yvals = np.array(yvals)
        data.y_err_vals = np.array(y_err_vals)
        data.Nvals = Nvals

    except Exception as e:
        print('Data1D load error.')
        raise e
    return data

def _parse_2D_monitor(text):
    data = Data2D()

    ''' populates data fields using the text from a mccode data file '''
    # load essential header data
    data = _parse_monitor_common(data,text)
    data = _parse_monitor_xylabel(data,text)
    try:
        '''# xvar: X'''
        m = re.search(r'# xvar: '+'({})'.format(freetext_pat)+r'\n', text)
        data.xvar = m.group(1)
        '''# yvar: Y '''
        m = re.search(r'# yvar: '+'({})'.format(freetext_pat)+r'\n', text)
        data.yvar = m.group(1)

        '''# zvar: I '''
        m = re.search(r'# zvar: '+'({})'.format(freetext_pat)+r'\n', text)
        data.zvar = m.group(1)
        '''
        # xylimits: -30 30 -30 30
        # xylimits: 0 5e+06 0.5 100
        '''
        m = re.search(r'# xylimits: ([\d\.\-\+e]+) ([\d\.\-\+e]+) ([\d\.\-\+e]+) ([\d\.\-\+e]+)([\ \d\.\-\+e]*)\n', text)
        data.xylimits = (float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)))

        '''# statistics: X0=5.99569; dX=0.0266368;'''
        m = re.search('\# statistics: X0=([\d\.\+\-e]+); dX=([\d\.\+\-e]+); Y0=([\d\.\+\-e]+); dY=([\d\.\+\-e]+);\n', text)

        data.statistics = 'X0=%.2E; dX=%.2E; Y0=%.2E; dY=%.2E;' % (Decimal(m.group(1)), Decimal(m.group(2)), Decimal(m.group(3)), Decimal(m.group(4)))
        '''# signal: Min=0; Max=1.20439e-18; Mean=4.10394e-21;'''
        m = re.search('\# signal: Min=([\ \d\.\+\-e]+); Max=([\ \d\.\+\-e]+); Mean=([\ \d\.\+\-e]+);\n', text)
        data.signal = 'Min=%f; Max=%f; Mean=%f;' % (float(m.group(1)), float(m.group(2)), float(m.group(3)))

        '''# Data [detector/PSD.dat] I:'''
        '''# Events [detector/PSD.dat] N:'''
        '''# Errors [detecot/PSD.dat] I_err:'''
        lines = text.splitlines()

        t_flags={'data':False,'counts':False,'errors':False}
        for l in lines:
            if '# Data ' in l:
                t_flags={'data':True,'counts':False,'errors':False}

            if '# Events ' in l:
                t_flags={'data':False,'counts':True,'errors':False}

            if '# Errors ' in l:
                t_flags={'data':False,'counts':False,'errors':True}

            if np.any(list(t_flags.values())):
                try:
                    vals = [float(item) for item in l.strip().split()]
                    if t_flags['data']:
                        data.zvals.append(vals)
                    if t_flags['counts']:
                        data.counts.append(vals)
                    if t_flags['errors']:
                        data.errors.append(vals)
                except:
                    pass

    except Exception as e:
        print('Data2D load error.')
        raise e

    return data

def load_ascii_monitor(monfile):
    f = monfile
    if not f == 'No file':
        with open(f)as fh:
            text = fh.read()
        # determine 1D / 2D data
        m = re.search(r'# type: (\w+)', text)
        typ = m.group(1)
        if typ == 'array_0d':
            data = _parse_0D_monitor(text)
        elif typ == 'array_1d':
            data = _parse_1D_monitor(text)
        elif typ == 'array_2d':
            data = _parse_2D_monitor(text)
        else:
            print('load_monitor: unknown data format %s' % typ)
            data = None
        data.filepath = f  
    else:
        data = Data0D()    
    return data

def load_mcvine_histogram(monfile):
    """
    load a histogram h5py file.
    """
    with h5py.File(monfile) as fh:
        rtnm = list(fh.keys())
        datain = fh[rtnm[0]]['data'][:]
        errsin = np.sqrt(fh[rtnm[0]]['errors'][:])
        hgrid = fh[rtnm[0]]['grid']
        grid = {}
        binlist = ['bin centers','bin boundaries']
        grdlst  = list(hgrid.keys())
        for item in grdlst:
            grid[item] = {}
            for bint in binlist:
                grid[item][bint] = hgrid[item][bint][:]
        if datain.ndim == 1:
            data = Data1D()
            data.xvals = grid[grdlst[0]]['bin centers']
            data.yvals = datain
            data.y_err_vals = errsin
      #  data.Nvals = Nvals

        elif datain.ndim == 2:
            data = Data2D()
            data.ylabel = '{} [{}]'.format(hgrid[grdlst[1]].attrs['name'],hgrid[grdlst[1]].attrs['unit'])
            data.yvar = grdlst[1]
            data.zvals = datain
            data.xylimits = (grid[grdlst[0]]['bin boundaries'].min(),grid[grdlst[0]]['bin boundaries'].max(),
                             grid[grdlst[1]]['bin boundaries'].min(),grid[grdlst[1]]['bin boundaries'].max())
            data.errors = errsin

        else:
            raise RuntimeError('data of {} dimensions is not implemented'.format(datain.ndim))
        # Common to all types 
        data.xvar = grdlst[0]
        data.xlabel = '{} [{}]'.format(hgrid[grdlst[0]].attrs['name'],hgrid[grdlst[0]].attrs['unit'])       
        data.filename = monfile   
        data.title =  fh[rtnm[0]].attrs['title']
        return data

def load_nxs(monfile,xaxis=None,yaxis=None,dset=None):
    """ 
    load a simlple nexus formated file
    If there is more than one data group in the file, 
    dset specifies the group. 
    If alternate axes should be on the plot, the y and x axis fields are provided.
    monfile is the file.
    the nexus file should have a 1 or 2 dimensional signal array, 
    it may or may not have a <signal>_errors array. If not one will be created that is filled with zeros.
    """
    with h5py.File(monfile,'r') as fh:
        if dset==None:
            rootlst = list(fh.keys())
            if len(rootlst)>1:
                raise RuntimeError("the nexus file has more than one data set please set dset to one of {}".format(rootlst))
            else:
                dset = rootlst[0]
        # handles common       
        signame = fh[dset].attrs['signal']  
        I = fh[dset][signame][:]
        try:
            errsin = fh[dset][signame+'_errors']
        except:
            errsin = np.zeros(I.shape)
        axsnms = fh[dset].attrs['axes']
        
        if xaxis == None:
           xaxis = axsnms[0]
        
        # handle 2D case  
        if I.ndim == 2: 
            data = Data2D()
            data.zvals = I
            if yaxis == None:
                yaxis = axsnms[1]
            data.ylabel = '{} [{}]'.format(yaxis,fh[dset][yaxis].attrs['units'])
            data.yvar = yaxis
            ytmp = fh[dset][yaxis][:]
            xtmp = fh[dset][xaxis][:]
            data.xylimits = (xtmp.min(),xtmp.max(),ytmp.min(),ytmp.max())
            data.errors = errsin
        # handle 1D case    
        elif I.ndim == 1:
            data = Data1D()
            data.yvals = I
            data.xvals = fh[dset][xaxis][:]
            data.y_err_vals = errsin
        else:
            raise RuntimeError ("{} Dimensions is not implemented".format(I.ndim))
        data.xvar = xaxis
        data.xlabel = '{} [{}]'.format(xaxis,fh[dset][xaxis].attrs['units'])
        data.filename = monfile 
    return data
def load_MD_Histo(monfile):
    """load from a MD_Histo file created in Mantid """
    with h5py.File(monfile,'r') as fh:
        rt = fh['MDHistoWorkspace']['data']
        signal = rt['signal'][:]
        axlst = rt['signal'].attrs['axes'].decode().split(':')
        sigsq = signal.squeeze()
        errs = np.sqrt(rt['errors_squared'][:])
        xvals = rt[axlst[0]][:]
        if sigsq.ndim ==1:
            data = Data1D()
            data.yvals = signal.squeeze()
            data.y_err_vals =  errs.squeeze()
            data.xvals = (xvals[1:]+xvals[:-1])/2       
        elif sigsq==2:
            data = Data2D()
            data.yvar = axlst[1]
            data.zvals = signal.squeeze() 
            data.errors = errs
        else:
            raise RuntimeError("Data of {} dimensions is not supported".format(sigd))
        data.xvar=axlst[0]
    return data


