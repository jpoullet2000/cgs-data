#!/usr/bin/python

from setuptools import setup, find_packages
import os, sys, re
import codecs
from sphinx.setup_command import BuildDoc
cmdclass = {'build_sphinx': BuildDoc}

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
    
def find_version_release(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
    version_file, re.M)
    if version_match:
        release = version_match.group(1)
        version = re.search(r"^([0-9]*\.[0-9])*\.[0-9]*$",
    release, re.M).group(1)
        return [version,release]
    raise RuntimeError("Unable to find version string.")

name = 'cgsdata'
[version,release] = find_version_release('cgsdata','__init__.py')

setup(
    name=name,
    version=version,
    release=release,
    url='https://github.com/jpoullet2000/cgs-data',
    license='Apache Software License',
    author='Jean-Baptiste Poullet',
    author_email='jeanbaptistepoullet@statrgy.com',
    description='Databases for genomics/exomics data in CGS',
    long_description=read_md('README.md'),
    packages=['cgsdata'],
    package_dir={'cgsdata': 'cgsdata'},
    package_data={'cgsdata': ['data/*.yml']},
    include_package_data=True,
    #dependency_links = ['https://github.com/perenecabuto/json_schema_generator/tarball/master']
    install_require = ['avro','PyVCF']
    #tests_require=['pytest'],
    #test_suite='tests',
    tests_require=['nose2'],
    test_suite='nose2.collector.collector',
    cmdclass=cmdclass,
    command_options={
           'build_sphinx': {
               'project': ('setup.py', name),
               'version': ('setup.py', version),
               'release': ('setup.py', release)
               }},
    classifiers = [
        'Programming Language :: Python',
         'License :: OSI Approved :: Apache Software License'
        ]
    )
