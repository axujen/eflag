eflag
=====
is a tool for managing rules in portage's package files.

eflag is designed to be easy and simple to use, making rule management of
package files less cumbersome and error prone.


Goals:
======
* Adding, deleting, and modifying rules on the fly.
* Converting package files from directory to file structure and vice versa.
* Simplicity and ease of use.

Installation:
=============
	git clone https://github.com/axujen/eflag.git
	cd eflag
	sudo ./setup.py install # ./setup.py install --user to install without root privilege

Alternatively you can find an ebuild for it in [my overlay](https://github.com/axujen/overlay/tree/master/app-portage/eflag)

Usage:
======
	usage: eflag [-h] [-v] [-t {accept_keywords,env,keywords,license,mask,properties,unmask,use}] [-d] [-s]
	             [-c]
	             [atom] ...
	
	Ease your /etc/portage/package.* file edition.
	
	positional arguments:
	  atom                  atom to be added/modified
	  flags                 flags to be enabled for the atom, flags starting with % will be deleted
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -v, --version         show program's version number and exit
	  -t {accept_keywords,env,keywords,license,mask,properties,unmask,use}
	                        package file type
	  -d                    delete the sepecified atom from the rules
	  -s                    show the rules listed in the package file
	  -c                    convert the current package file from file style to folder style and vice-versa

Thanks:
=======
Thanks to [Pyntony](http://github.com/Pyntony) for the original tool
[emod](http://github.com/Pyntony/emod).

*Note: eflag is still in development, don't use it directly on your package files
unless if you have a backup.
