#!/usr/bin/python3
"""
Add the location where cookie/ will be to
system path. Prompts for a custom directoy,
otherwise uses current. Installs requirements
specified in project.yml. Allows 'import cookie'
in any Python instance :)

@auhtor chairs
"""
from yaml import load
import subprocess, sys, os

# check file
try: 
	stream = open('project.yml')
except (OSError, Exception):
	print('project file not found')
	exit()


# globals
silent = subprocess.DEVNULL
verbose = sys.stdout.fileno()
cwd = os.getcwd()
pip = ['pip3','install',]


# begin parsing
def parse ():
	root = load(stream)
	return (root['project']['requires'].split(','),
			root['project']['name'],
			root['project']['standalone'])

try: 
	requires, name, standalone = parse()
	print('installing %s' % name)
	path = input('path? ')
	if path == '': sys.path.append(cwd)
	else:
		sys.path.append(path)

	if not standalone:
		pip += requires
		subprocess.call(pip, stdout=verbose)

except Exception:
	print('installation error')