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
supported_types=('accept_keywords', 'env', 'keywords', 'license', 'mask',
'properties', 'unmask', 'use')

class Package(object):
	"""portage package file."""
	def __init__(self, type):
		self.type = type
		self.path = '.'.join(('/etc/portage/package', self.type))

		# for the sake of simplicity create the file if it does not exist
		if not os.path.exists(self.path):
			open(self.path, 'a', encoding='utf-8').close()

		# Detect package style
		if os.path.isdir(self.path):
			self.style = 'directory'
		elif os.path.isfile(self.path):
			self.style = 'file'
		else:
			# It can only be a directory or file (symlinks should pass)
			raise TypeError('"%s" is not a file or directory!' % self.path)

		self.rules = None # None means that we have not read the rules yet.

	def read_rules(self):
		"""Read the rules from package file."""

		pkg_file = self.path
		rules = {}

		# the rules are split into a list in the form [atom, flags]
		if self.style == 'file':
			with open(pkg_file, 'r', encoding='utf-8') as f:
				# filter empty lines and comments
				for line in f.readlines():
					if not line.isspace() and not line.startswith("#"):
						try:
							atom, flags = line.rstrip('\n').split(None, 1)
							flags=flags.split(None)
						except ValueError:
							atom, flags = line.rstrip('\n'), []
						rules[atom.strip()]=list(set(flags))

		# directories go by another layout with seperate files for categories
		# with each category file containing atoms for ebuilds that
		# fall into that category
		elif self.style == 'directory':
			for category in os.listdir(pkg_file):
				with open(os.path.join(pkg_file, category), 'r', encoding='utf-8') as f:
					for line in f.readlines():
						if not line.isspace() and not line.startswith("#"):
							try:
								atom, flags = line.rstrip('\n').split(None, 1)
								flags=flags.split(None)
							except ValueError:
								atom, flags = line.rstrip('\n'), []
							rules[atom.strip()]=list(set(flags))

		self.rules = rules
		return self.rules

	def save_rules(self):
		"""Save the rules to the package file."""

		# modify the rules for a more writable format
		rules = []
		for atom in self.rules:
			rule = self._atom_rule(atom) + '\n'
			rules.append(rule)
		rules.sort()

		# Save according to the directory format if working with directories.
		if self.style == 'directory':
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
				category_file = os.path.join(self.path, category)
				with open(category_file, 'w', encoding='utf-8') as f:
					f.write(categories[category])

		# Save normaly if working with a file.
		elif self.style == 'file':
			with open(self.path, 'w', encoding='utf-8') as f:
				f.write(''.join(rules))

	def convert(self):
		"""Convert the package style."""

		if self.rules == None:
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
			os.mkdir(self.path)
			self.style = 'directory'

		elif self.style == 'directory':
			print('Going from directory to file style.')
			open(self.path, 'a', encoding='utf-8').close()
			self.style = 'file'

		self.save_rules()

	def modify_atom(self, atom, flags):
		"""Add or modify an atom."""

		if self.rules == None:
			self.read_rules()

		if not flags:
			# mask and unmask do not require flags
			if self.type in ('mask', 'unmask'):
				self.rules[atom]=[]
				print('"%s" has been %sed.' % (atom, self.type))
				self.save_rules()
			# If no modifications are made then just print the rule.
			elif atom in self.rules:
				print(self._atom_rule(atom))
			else:
				print('No rule found for "%s" in "%s"!' % (atom, self.path))
			return

		if atom in self.rules:
			old_atom = self._atom_rule(atom)
			for flag in flags:
				if flag.startswith("%"):
					matches = [f for f in self.rules[atom] if flag[1:] in (f, f[1:])]
					if matches:
						for match in matches:
							self.rules[atom].remove(match)
				elif flag in self.rules[atom]:
					print('Warning flag "%s" already exists!' % flag)
				else:
					self.rules[atom].append(flag)
			print('Modified "%s":' % atom)
			diff(old_atom, self._atom_rule(atom))
		else:
			self.rules[atom]=flags
			print('Added "%s" to "%s"!' % (self._atom_rule(atom), self.path))

		self.save_rules()

	def delete_rule(self, atom):
		"""Delete the rule associated with the `atom`"""

		if self.rules == None:
			self.read_rules()

		if atom in self.rules:
			self.rules.pop(atom)
			print('Removed "%s" from "%s"!' % (atom, self.path))
		else:
			print('No match for "%s" found in "%s"!' % (atom, self.path))

		self.save_rules()

	def print_rules(self):
		if self.rules == None:
			self.read_rules()

		for atom in self.rules:
			print(self._atom_rule(atom))

	def _atom_rule(self, atom):
		"""Join the rule for the specified atom into one line."""
		if atom in self.rules:
			return ' '.join((atom, ' '.join((self.rules[atom]))))
		else:
			return None

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
	arguments = ArgumentParser(description="Ease your /etc/portage/package.* "\
			"file edition.")
	arguments.add_argument('-v', '--version', action='version', version=__version__)
	arguments.add_argument('atom', type=str, nargs='?', default=None,
			help="atom to be added/modified")
	arguments.add_argument('flags', type=str, nargs=REMAINDER, default=[],
			help="flags to be enabled for the atom, flags starting with %% "\
					"will be deleted")
	arguments.add_argument('-t', type=str, default='use', dest='type',
			help='package file type', choices=(supported_types))
	arguments.add_argument('-d', action='store_true', default=False, dest='delete',
			help='delete the sepecified atom from the rules')
	arguments.add_argument('-s', default=False, action='store_true', dest='show',
			help="show the rules for this type")
	arguments.add_argument('-c', default=False, action='store_true', dest='convert',
			help="convert the current package file from file style to folder "\
					"style and vice-versa")

	args = arguments.parse_args()
	package=Package(args.type)

	if args.show:
		package.print_rules()
	if args.convert:
		package.convert()

	if args.atom:
		if args.delete:
			package.delete_rule(args.atom)
		else:
			package.modify_atom(args.atom, args.flags)

# vim: ft=python:tabstop=4:softtabstop=4:shiftwidth=4:noexpandtab
