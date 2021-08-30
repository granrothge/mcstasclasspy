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
    def test_load2D(self):
        data = mcm.load_ascii_monitor(os.path.join(datadir,'Source_image.dat'))
        assert isinstance(data,mcm.Data2D)
if __name__ == "__main__":
    interactive = True
    unittest.main()
