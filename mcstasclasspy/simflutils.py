
from os.path import isfile, isdir, join, dirname, basename, splitext, exists
import re
def _get_filenames_from_mccodesim(mccodesim):
    dir = dirname(mccodesim)

    text = open(mccodesim).read()
    data_idx = text.find('begin data')
    filenames = []
    secs = text.split('begin data')
    for sec in secs[1:]:
        m = None
        for line in sec.splitlines():
            if m == None:
                m = re.search(r'filename: ([\w\.\,_\-+]+)\s*', line)
        if m:
            filenames.append(join(dir, m.group(1)))
        else:
            filenames.append('No file')
    return filenames

def parms_from_sim(flname,simbnds = {'begin sim': True, 'end sim': False}):
    """
    Get parameters from a sim file
    flname: a path to a file name
    simbnds: tags to decide where to look for parameters.
    """
    parms={}
    with open(flname)as dsimh:
        dotsims = dsimh.readlines()
    sim_flag = False
    for ln in dotsims:
        for sim in simbnds.keys():
            if sim in ln:
                sim_flag = simbnds[sim]
        if sim_flag:
            if 'Param:' in ln:
                parm = ln.split('Param:')[1].split('=')
                parms[parm[0].strip()] = parm[1].strip()
    return parms