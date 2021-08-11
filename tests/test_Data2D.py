import os
import unittest
interactive = False
datadir = os.path.join(os.path.dirname(__file__), "data")
import mcstasclasspy.mcmonloader as mcm


class TestCase(unittest.TestCase):
    def test_pcolor(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_image.dat'))
        if not interactive:
            import matplotlib
            matplotlib.use('Agg')
        data.pcolor()
        if interactive:
            from matplotlib import pyplot as plt
            plt.show()
        return
    def test_cut(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_image.dat'))
        cut1 = data.cut('y',0,0.5)
        cut2 = data.cut('x',0,0.5)
        assert isinstance(cut1,mcm.Data1D)
        assert isinstance(cut2,mcm.Data1D)
        return
    
if __name__ == "__main__":
    interactive = True
    unittest.main()
