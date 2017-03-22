import setuptools
from metnocharts.version import version


setuptools.setup(name='python-metnocharts',
                 version=version,
                 description='Python Package for Met Norway Ice charts processing',
                 long_description=open('README.rst').read().strip(),
                 author='Mikhail Itkin',
                 author_email='itkin.m@gmail.com',
                 py_modules=['metnocharts'],
                 install_requires=[],
                 license='GPLv3',
                 zip_safe=False,
                 keywords='sea ice charts',
classifiers=['Packages'])
