import os
import unittest
interactive = False
datadir = os.path.join(os.path.dirname(__file__), "data")
import mcstasclasspy.mcmonloader as mcm

class TestCase(unittest.TestCase):
    def test_load0D(self):
         data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_Flux.dat'))
         assert isinstance(data,mcm.Data0D)
         assert data.component=='Source_Flux'
         assert data.title=='Single monitor Source_Flux'

    def test_load1D(self):
        #import mcstasclasspy.mcmonloader as mcm
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_spectrum.dat'))
        assert isinstance(data,mcm.Data1D)
        assert data.component=='Source_Spectrum'
        assert data.title=='Wavelength monitor'
        assert data.xlabel=='Wavelength [AA]'
        assert data.ylabel=='Intensity'
        assert data.filename=='Source_spectrum.dat'
        assert data.xvar=='L'
        assert data.yvar==('I', 'I_err')
        assert data.xlimits==(0.0, 10.0)

    def test_load2D(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_image.dat'))
        assert isinstance(data,mcm.Data2D)
        assert data.component == 'Source_Image'
        assert data.title == 'PSD monitor'
        assert data.xlabel == 'X position [cm]'
        assert data.ylabel == 'Y position [cm]'
        assert data.filename == 'Source_image.dat'
        assert data.xvar == 'X'
        assert data.yvar == 'Y' 
        assert data.zvar == 'I'
        assert data.xylimits == (-10.0, 10.0, -10.0, 10.0)

    def test_load_hist1D(self):
        data =mcm.load_mcvine_histogram(os.path.join(datadir,'ienergy.h5'))

    def test_load_hist2D(self):
        data =mcm.load_mcvine_histogram(os.path.join(datadir,'ix_y.h5'))

if __name__ == "__main__":
    interactive = True
    unittest.main()
