#!/usr/bin/python3
"""
Parse project.yml, syncronize local
source tree with GitHub repository
using .gitignore

@auhtor chairs
"""
from yaml import load
import subprocess, sys

# subprocess globals
silent = subprocess.DEVNULL
verbose = sys.stdout.fileno()
add = ['git', 'add','.']
commit = ['git','commit','-a','-m',]
push = ['git', 'push']


# check file
try: 
	stream = open('project.yml')
except (OSError, Exception):
	print('project file not found')
	exit()

# begin parsing
root = load(stream)
gh = (root['author'], root['project']['name'])
url = 'https://github.com/%s/%s' % gh

# deployment calls
try:
	subprocess.call(add, stdout=silent)
	msg = input('note? ')


	# use supplied commit message
	if msg == '': commit.append('update')
	else: 
		commit.append(str(msg))

	subprocess.call(commit, stdout=silent)
	subprocess.call(push, stdout=verbose)

	print('successful deployment')

except (subprocess.CalledProcessError, OSError, Exception):
	print('deployment error')
	exit()

