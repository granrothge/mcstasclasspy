import os
import unittest
interactive = False
datadir = os.path.join(os.path.dirname(__file__), "data")
import mcstasclasspy.mcmonloader as mcm
import numpy as np


class TestCase(unittest.TestCase):
    def test_errorbar(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_spectrum.dat'))
        if not interactive:
            import matplotlib
            matplotlib.use('Agg')
        data.errorbar()
        if interactive:
            from matplotlib import pyplot as plt
            plt.show()
        return
    def test_plot(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_spectrum.dat'))
        if not interactive:
            import matplotlib
            matplotlib.use('Agg')
        data.plot()
        if interactive:
            from matplotlib import pyplot as plt
            plt.show()
        return
    def test_mult(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_spectrum.dat'))
        data2 = data * 5
        assert(abs(((data2.yvals-5*data.yvals))<1e-5).all())
    def test_peakstats(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_spectrum.dat'))
        data.peakstats()
        return
    def test_bin(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_spectrum.dat'))
        data.bin(0.2)
        return
    def test_add(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_image.dat'))
        cut1 = data.cut('x',0,0.5)
        cut2 = data.cut('x',2,0.5)
        cutd = cut1+cut2
        assert np.all(cutd.yvals == cut1.yvals+cut2.yvals)
        return
    def test_sub(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_image.dat'))
        cut1 = data.cut('x',0,0.5)
        cut2 = data.cut('x',2,0.5)
        cutd = cut1-cut2
        assert np.all(cutd.yvals == cut1.yvals-cut2.yvals)
        return
    
if __name__ == "__main__":
    interactive = True
    unittest.main()
