class DataMcCode(object):
    ''' base type holding only the data object's title '''
    def __init__(self, *args, **kwargs):
        self.title = ''
        self.filepath = ''
        self.xlabel = ''
        self.ylabel = ''
        self.statistics = ''

    def __str__(self, *args, **kwargs):
        return self.title

    def _add_titles(self,ax):
        """ add titles to plot helper function"""
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.set_title(self.title)