import mcstasclasspy
from setuptools import setup, find_packages
import os

def read_md(fl):
    with open(fl,'r') as f:
        return f.read()
init = os.path.join(os.path.dirname(__file__),'mcstasclasspy','__init__.py')
v_l = list(filter(lambda l: l.startswith('VERSION'),open(init)))[0]
Vtpl = eval(v_l.split('=')[-1])
PKG_V = ".".join([str(x) for x in Vtpl])
setup(
    name='mcstasclasspy',
    version = PKG_V,
    long_description=read_md("README.md"),
    long_description_content_type='text/markdown',
    packages= find_packages(".", exclude=['tests']),
    author = "G. E. Granroth",
    install_requires = ['numpy','matplotlib','lmfit']
)