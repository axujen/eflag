#!/usr/bin/env python
import sys
from distutils.core import setup

sys.path.insert(0, 'src')
import eflag

setup(
    name = "eflag",
    package_dir = {'': 'src'},
    packages = ['eflag'],
    scripts = ["eflag"],
	description = eflag.description,
    version = eflag.package_version,
    author = eflag.author,
    author_email = eflag.author_email,
    url = "https://github.com/axujen/eflag",
    keywords = ["portage", "package"],
	classifiers = [
                'Development Status :: 3 - Alpha',
                'Environment :: Console',
                'Intended Audience :: System Administrators',
				'Intended Audience :: End Users/Desktop',
                'Programming Language :: Python',
				'Programming Language :: Python :: 3',
				'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
				'Operating System :: POSIX :: Linux',
                'Topic :: System :: Installation/Setup'
				'Topic :: System :: Systems Administration',
				'Topic :: Utilities',
                ],
    long_description = """\
eflag
-----
is a script for managing rules in portage's package files.

eflag is designed to be easy and simple to use, making rule management
package file less cumbersome.
"""
)
