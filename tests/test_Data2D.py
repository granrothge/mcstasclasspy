import os
import copy
import unittest
import pytest
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
    def test_contourf(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_image.dat'))
        if not interactive:
            import matplotlib
            matplotlib.use('Agg')
        data.contourf()
        if interactive:
            from matplotlib import pyplot as plt
            plt.show()
        return
    def test_contour(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_image.dat'))
        if not interactive:
            import matplotlib
            matplotlib.use('Agg')
        data.contour()
        if interactive:
            from matplotlib import pyplot as plt
            plt.show()
        return
    def test_cut(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_image.dat'))
        cut1 = data.cut('y',0,0.5)
        cut2 = data.cut('x',0,0.5)
        cut3 = data.cut('x',0,0.5,xlims=(-1,1))
        assert isinstance(cut1,mcm.Data1D)
        assert isinstance(cut2,mcm.Data1D)
        assert isinstance(cut3,mcm.Data1D)
        return

    def test_cutoutrange(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_image.dat'))
        with pytest.raises(Exception):
            data.cut('y',1000.0,0.5)
        return

    def test_addconst(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_image.dat'))
        datao = data+2
        return
    def test_add(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_image.dat'))
        data2=copy.deepcopy(data)
        datao = data+data2
        return
    def test_mult_const(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_image.dat'))
        datao = data*2
        return
    def test_mult(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_image.dat'))
        data2 = copy.deepcopy(data)
        datao = data*data2
        return
    def test_checkxylimsfail(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_image.dat'))
        data2 = mcm.load_ascii_monitor(os.path.join(datadir,'Source_vertical_divLambda_map.dat'))
        with pytest.raises(RuntimeError):
            data+data2
        return
    def test_checktypefail(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_image.dat'))
        cut1 = data.cut('x',0,0.5)
        with pytest.raises(RuntimeError):
            data+cut1
        return

    def test_write_MDHisto(self):
        import numpy as np
        data = mcm.load_nxs(os.path.join(datadir,'nxs_tst.nxs.h5'),xaxis='k',yaxis='E')
        data.mask=np.zeros(data.zvals.shape,dtype=np.int8)
        data.save_MDHisto('/tmp/test_gen_MD_histo.nxs')
        os.remove('/tmp/test_gen_MD_histo.nxs')
    
    def test_str(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_image.dat'))
        print(data)

    
if __name__ == "__main__":
    interactive = True
    unittest.main()
