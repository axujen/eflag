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
    author = eflag.author,
    author_email = eflag.email,
    version = eflag.version,
	description = eflag.description,
	license = 'GPLv3',
	platforms='Linux',
    url = "https://github.com/axujen/eflag",
    keywords = ["Portage", "Package", "Gentoo", "Funtoo", "Linux"],
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
is a tool for managing rules in portage's package files.

eflag is designed to be easy and simple to use, making rule management of
package files less cumbersome and error prone.
"""
)
