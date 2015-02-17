#!/usr/bin/python

from setuptools import setup, find_packages
import os, sys, re
import codecs

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()
    
def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
    version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='cgsdata',
    version=find_version('cgsdata','__init__.py'),
    url='https://github.com/jpoullet2000/cgs-data',
    license='Apache Software License',
    author='Jean-Baptiste Poullet',
    author_email='jeanbaptistepoullet@statrgy.com',
    description='Databases for genomics/exomics data in CGS',
    long_description=read_md('README.md'),
    packages=['cgsdata'],
    package_dir={'cgsdata': 'cgsdata'},
    package_data={'cgsdata': ['data/*.csv']},
    include_package_data=True,
    tests_require=['pytest'],
    test_suite='tests',
    classifiers = [
        'Programming Language :: Python',
         'License :: OSI Approved :: Apache Software License'
        ]
    )
