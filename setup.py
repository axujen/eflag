#!/usr/bin/env python
import sys
from distutils.core import setup

sys.path.insert(0, 'src')
from eflag import package_version

setup(
    name = "eflag",
    version = package_version,
    package_dir = {'': 'src'},
    packages = ['eflag'],
    scripts = ["eflag"],
    description = "Python script to ease editing of portage package file.",
    author = "Axujen",
    author_email = "Axujen <axujen@gmail.org>",
    url = "https://github.com/axujen/eflag",
    keywords = ["portage", "package"],
	classifiers = [
                'Development Status :: 4 - Beta',
                'Environment :: Console',
                'Intended Audience :: System Administrators',
                'Programming Language :: Python',
                'Topic :: System :: Installation/Setup'
                ],
    long_description = """\
eflag
-----
is a script for managing rules in portage's package files.

eflag is designed to be easy and simple to use, making rule management
package file less cumbersome.
"""
)
