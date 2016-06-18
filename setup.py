#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    readme = f.read()

packages = [
]

package_data = {
}

requires = [
    'appnope==0.1.0',
    'backports.shutil-get-terminal-size==1.0.0',
    'beautifulsoup4==4.4.1',
    'cssselect==0.9.1',
    'decorator==4.0.10',
    'hiredis==0.2.0',
    'ipython==4.2.0',
    'ipython-genutils==0.1.0',
    'lxml==3.6.0',
    'path.py==0.0.0',
    'pathlib2==2.1.0',
    'pexpect==4.0.1',
    'pickleshare==0.7.2',
    'ptyprocess==0.5.1',
    'redis==2.10.5',
    'simplegeneric==0.8.1',
    'six==1.10.0',
    'traitlets==4.2.1',
    'urlnorm==1.1.3'
]

classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='',
    version='',
    description='',
    long_description=readme,
    packages=packages,
    package_data=package_data,
    install_requires=requires,
    author='',
    author_email='',
    url='',
    license='MIT',
    classifiers=classifiers,
)