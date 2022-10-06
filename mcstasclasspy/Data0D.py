import numpy as np
import matplotlib.pyplot as plt
from .DataMCCode import DataMcCode
class Data0D(DataMcCode):
    '''  '''
    def __init__(self):
        super(Data0D, self).__init__()

        self.component = ''
        self.filename = ''        
        self.ylabel = ''
        self.variables = []
        self.yvar = () # pair
        self.values = () # triplet
        

        # data references
        self.yvals = []
        self.y_err_vals = []
        self.Nvals = []