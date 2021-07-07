from setuptools import find_packages, setup

setup(
    name = 'PumPy',
    packages = find_packages(include=['PumPy']),
    version = '0.1.10',
    description = 'Python library to control Pumpy',
    author = 'Rebecca Saleeb',
    license = 'GNU GPLv3',
    install_requires = ['pyserial']
)
