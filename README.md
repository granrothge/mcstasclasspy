A set of classes to work with: 
- ascii files from [mcstas](https://www.mccode.org/)
- hdf histogran files from [mcvine](https://github.com/mcvine)
- MD histo nexus files from [Mantid](https://www.mantidproject.org/)

## Installation instructions

1. Ensure the dependencies are installed

    - python
    - numpy
    - matplotlib
    - lmfit
1. clone the repository ```git clone https://github.com/granrothge/mcstasclasspy.git ```
1. change to mcstasclasspy directory
1. Then use ```python setup.py install``` if you have administrator rights to the machine 
or ```python setup.py install --user``` to install it in your user directory

I try to keep to few and relatively stable libraries.  So it should work on a python 3.X eco system where the dependencies can be installed.
 
There are a few example jupyter notebooks to show example use cases.

This is very much a work in progress and I add functionality as I need it.  Feel free to request something if you need it.