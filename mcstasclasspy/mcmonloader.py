# rework of mcploatloader.py for plotting single monitor data

'''
functionality for loading mccode data into suitable data types,
and assembling it in a plot-friendly way.
'''
from os import fchdir
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

    try:
        # load essential header data
        data = _parse_monitor_common(data,text)
        '''# filename: Edet.dat'''
        #m = re.search('\# filename: ([\-\+\w\.\,]+)\n', text)
        #data.filename = m.group(1)
      
        '''# values: 6.72365e-17 4.07766e-18 4750'''
        m = re.search('\# values: ([\d\-\+\.e]+) ([\d\-\+\.e]+) ([\d\-\+\.e]+)\n', text)
        data.values = (Decimal(m.group(1)), Decimal(m.group(2)), float(m.group(3)))
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

    try:
        # load essential header data
        data = _parse_monitor_common(data,text)      
        data = _parse_monitor_xylabel(data,text)
        '''# xvar: L'''
        m = re.search('\# xvar: ([\w]+)\n', text)
        data.xvar = m.group(1)
        '''# xlimits: 5.5 6.5'''
        m = re.search('\# xlimits: ([\d\.\-\+e]+) ([\d\.\-\+e]+)\n', text)
        data.xlimits = (float(m.group(1)), float(m.group(2)))

        '''# yvar: (I,I_err)'''
        m = re.search('\# yvar: \(([\w]+),([\w]+)\)\n', text)
        data.yvar = (m.group(1), m.group(2))

        '''# values: 6.72365e-17 4.07766e-18 4750'''
        m = re.search('\# values: ([\d\-\+\.e]+) ([\d\-\+\.e]+) ([\d\-\+\.e]+)\n', text)
        data.values = (Decimal(m.group(1)), Decimal(m.group(2)), float(m.group(3)))
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
    try:
        # load essential header data
        data = _parse_monitor_common(data,text)
        data = _parse_monitor_xylabel(data,text)

        '''# xvar: X'''
        m = re.search('\# xvar: (%s)\n' % freetext_pat, text)
        data.xvar = m.group(1)
        '''# yvar: Y '''
        m = re.search('\# yvar: (%s)\n' % freetext_pat, text)
        data.yvar = m.group(1)

        '''# zvar: I '''
        m = re.search('\# zvar: (%s)\n' % freetext_pat, text)
        data.zvar = m.group(1)
        '''
        # xylimits: -30 30 -30 30
        # xylimits: 0 5e+06 0.5 100
        '''
        m = re.search('\# xylimits: ([\d\.\-\+e]+) ([\d\.\-\+e]+) ([\d\.\-\+e]+) ([\d\.\-\+e]+)([\ \d\.\-\+e]*)\n', text)
        data.xylimits = (float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)))

        '''# values: 6.72365e-17 4.07766e-18 4750'''
        m = re.search('\# values: ([\d\+\-\.e]+) ([\d\+\-\.e]+) ([\d\+\-\.e]+)\n', text)
        data.values = (Decimal(m.group(1)), Decimal(m.group(2)), float(m.group(3)))
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
        m = re.search('\# type: (\w+)', text)
        typ = m.group(1)
        if typ == 'array_0d':
            #print("load_monitor: Not loading 0d dataset %s" % monfile)
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


