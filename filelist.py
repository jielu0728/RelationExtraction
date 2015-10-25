#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
make a filelist

Usage:
  filelist <name>
  filelist -h | --help
"""
import os
from string import maketrans
from docopt import docopt

if __name__ == '__main__':
	arguments = docopt(__doc__)
	name = arguments['<name>']
	location = './'+name

	res = open('./filelist','w')

	for subdir, dirs, files in os.walk(location):
		for f in files:
			res.write('../'+name+'/'+f+'\n')
	res.close()
