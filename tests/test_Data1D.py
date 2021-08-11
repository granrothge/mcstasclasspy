import os
import unittest
interactive = False
datadir = os.path.join(os.path.dirname(__file__), "data")
import mcstasclasspy.mcmonloader as mcm


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
    def test_bin(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_spectrum.dat'))
        data.bin(0.2)
    
if __name__ == "__main__":
    interactive = True
    unittest.main()
