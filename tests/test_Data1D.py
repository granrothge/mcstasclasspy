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
    def test_plot_ax(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_spectrum.dat'))
        from matplotlib import pyplot as plt
        if not interactive:
            import matplotlib
            matplotlib.use('Agg')
        f,ax =plt.subplots()    
        data.plot(ax=ax)
        if interactive:
            from matplotlib import pyplot as plt
            plt.show()
        return
        
    def test_mult(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_spectrum.dat'))
        data2 = data * 5
        assert(abs(((data2.yvals-5*data.yvals))<1e-5).all())
    def test_mult2(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_image.dat'))
        cut1 = data.cut('x',0,0.5)
        cut2 = data.cut('x',2,0.5)
        cutd = cut1*cut2
        assert np.all(cutd.yvals == cut1.yvals*cut2.yvals)
        return
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
    
    def test_div2(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_spectrum.dat'))
        data2 = data / 5
        assert(abs(((data2.yvals-data.yvals/5))<1e-5).all())

    def test_fit1(self):
        
        dat = mcm.load_MD_Histo(os.path.join(datadir,'test_MDhisto.nxs.h5'))
        cut_1 = dat.cut('y',2.0,0.5,xlims=(3.5,6.5))
        def gaussian(x, I0, FWHM, x0, y0):
            ln2 = 2*np.log(2)
            return y0+I0*np.sqrt(ln2/np.pi)/FWHM*np.exp(-ln2*((x-x0)/FWHM)**2)
        cut_1.setup_fit(gaussian)
        cut_1.fparams['I0'].value = 175
        cut_1.fparams['FWHM'].value = 1
        cut_1.fparams['x0'].value = 5
        cut_1.fparams['y0'].value = 0
        cut_1.fit(useerr=False)
        cut_1.res_str()
        if not interactive:
            import matplotlib
            matplotlib.use('Agg')
        cut_1.plot_fit()
        if interactive:
            from matplotlib import pyplot as plt
            plt.show()
        return

    def test_fit2(self):
         dat = mcm.load_MD_Histo(os.path.join(datadir,'test_MDhisto.nxs.h5'))
         cut_1 = dat.cut('y',2.0,0.5,xlims=(3.5,6.5))
         def gaussian(x, I0, FWHM, x0, y0):
            ln2 = 2*np.log(2)
            return y0+I0*np.sqrt(ln2/np.pi)/FWHM*np.exp(-ln2*((x-x0)/FWHM)**2)
         cut_1.setup_fit(gaussian)
         cut_1.fparams['I0'].value = 175
         cut_1.fparams['FWHM'].value = 1
         cut_1.fparams['x0'].value = 5
         cut_1.fparams['y0'].value = 0
         with self.assertRaises(RuntimeError):
             cut_1.fit()

    def test_fit3(self):
         dat = mcm.load_MD_Histo(os.path.join(datadir,'test_MDhisto.nxs.h5'))
         cut_1 = dat.cut('y',2.0,0.5,xlims=(3.5,6.5))
         with self.assertRaises(RuntimeError):
             cut_1.plot_fit()
         

        
    
if __name__ == "__main__":
    interactive = True
    unittest.main()
