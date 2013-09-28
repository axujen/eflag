#!/usr/bin/env python
#-*-coding:UTF-8-*-
# © Copyright 2013 axujen, <axujen at gmail.com>. All Rights Reserved.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.	If not, see <http://www.gnu.org/licenses/>.

import os, re, sys
from codecs import open
from difflib import Differ

from argparse import ArgumentParser, REMAINDER

__version__ = '0.1.0'

class cituple(tuple):
	"""Case insensitive typle."""
	def __init__(self, set):
		self.set = set

	def __contains__(self, item):
		return item.lower() in (s.lower() for s in self.set)

class Package(object):
	"""portage package file."""
	pkg_types = cituple(('accept_keywords', 'env', 'keywords', 'license',
		'mask', 'properties', 'unmask', 'use'))

	def __init__(self, path, type):
		self.path = os.path.abspath(os.path.expanduser(path))
		self.type = type

		if not type in self.pkg_types:
			raise TypeError('Unsupported package type: %s' % type)

		# Raise error if the file does not exist
		if not os.path.exists(self.path):
			raise OSError('File %s not found!' % self.path)

		# Detect package style
		if os.path.isdir(self.path):
			self.style = 'directory'
		elif os.path.isfile(self.path):
			self.style = 'file'
		else:
			raise TypeError('Unrecognized file type for %s' % path)

		self.rules = None # None means that we have not read the rules yet.

	def read_rules(self):
		"""Read the rules from package file."""

		pkg_file = self.path
		if not os.path.exists(pkg_file):
			raise IOError('Cannot find %s' % pkg_file)

		# the rules are split into a list in the form [atom, flags]
		if self.style == 'file':
			with open(pkg_file, 'r', encoding='utf-8') as f:
				rules = []
				# filter empty lines and comments
				for line in f.readlines():
					if not line.isspace() and not line.startswith("#"):
						rule = line.rstrip('\n').split(None, 1)
						if len(rule) < 2: rule.append('')
						rules.append(rule)

		# directories go by another layout with seperate files for categories
		# with each category file containing atoms for ebuilds that
		# fall into that category
		elif self.style == 'directory':
			rules = []
			for category in os.listdir(pkg_file):
				with open(os.path.join(pkg_file, category), 'r', encoding='utf-8') as f:
					for line in f.readlines():
						if not line.isspace() and not line.startswith("#"):
							rule = line.rstrip('\n').split(None, 1)
							if len(rule) < 2: rule.append('')
							rules.append(rule)

		self.rules = sorted(rules)
		return self.rules

	def save_rules(self):
		"""Save the `rules` to `pkg_file`."""

		# modify the rules for a more writable format
		rules = [' '.join(atom) + '\n' for atom in self.rules]
		pkg_file = self.path

		# Save according to the directory format if working with directories.
		if self.style == 'directory':
			if not os.path.exists(pkg_file):
				os.mkdir(pkg_file)

			# seperate categories and ebuilds, then build a dictionary in the
			# {category:"category/ebuild\ncategory/ebuild2\n"} format for writing
			categories = {}
			for rule in rules:
				category, ebuild = rule.split('/', 1)
				base_category = re.sub('[!~<>=]', '', category)

				if base_category in categories:
				   categories[base_category] += rule
				else:
				   categories[base_category] = rule

			for category in categories:
				category_file = os.path.join(pkg_file, category)
				with open(category_file, 'w', encoding='utf-8') as f:
					f.write(categories[category])

		# Save normaly if working with a file.
		elif self.style == 'file':
			with open(pkg_file, 'w', encoding='utf-8') as f:
				f.write(''.join(rules))

	def convert(self):
		"""Convert the package style."""

		if not self.rules:
			self.read_rules()

		# Backup the old file.
		n = 0
		while True:
			bkp_path = '.'.join((self.path, 'bkp', str(n)))
			if not os.path.exists(bkp_path):
				break
			n +=1
		print('Backing up "%s" to "%s".' % (self.path, bkp_path))
		os.rename(self.path, bkp_path)

		if self.style == 'file':
			print('Going from file to directory style.')
			self.style = 'directory'

		elif self.style == 'directory':
			print('Going from directory to file style.')
			self.style = 'file'
		self.save_rules()

	def add_atom(self, atom):
		"""Add or modify an atom."""

		if not self.rules:
			self.read_rules()

		pass

def diff(string1, string2):
	"""Print a colored diff of 2 rules."""
	Diff = Differ()
	diff = Diff.compare(string1.split(), string2.split())
	result = list(diff)
	for i in result:
		if i[2:] == string1.split(None, 1)[0]:
			# Exception for atoms
			sys.stdout.write(i[2:])
		elif i.startswith("+"):
			sys.stdout.write(' \033[32m'+i[2:]+'\033[0m')
		elif i.startswith("-"):
			sys.stdout.write(' \033[31m'+i[2:]+'\033[0m')
		else:
			sys.stdout.write(i[1:])
	sys.stdout.write("\n")

def main():
	arguments = ArgumentParser(description="Ease your /etc/portage/package.* edition.")
	arguments.add_argument('-s', '--show', default=False, action='store_true')
	arguments.add_argument('--save', default=False, action='store_true')
	arguments.add_argument('-c', '--convert', default=False, action='store_true')

	args = vars(arguments.parse_args())
	pkg='~/Code/eflag/package.use'
	type='use'
	package=Package(pkg, type)
	package.read_rules()

	if args['show']:
		print(package.rules)
	if args['save']:
		package.save_rules()
	if args['convert']:
		package.convert()

# vim: ft=python:tabstop=4:softtabstop=4:shiftwidth=4:noexpandtab
