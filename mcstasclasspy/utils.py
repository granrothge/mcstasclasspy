import functools
import matplotlib.pyplot as plt
def plt_func_wrap(func):
    @functools.wraps(func)
    def _plt_wrapper(*args,**kwargs):
        if not 'ax' in kwargs.keys():
            fig, kwargs['ax'] = plt.subplots()
        im = func(*args,**kwargs)
        args[0]._add_titles(kwargs['ax'])
        return im
    return _plt_wrapper