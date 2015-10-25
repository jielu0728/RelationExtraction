#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
convert all the chapters of a novel

Usage:
  convert <name>
  convert -h | --help
"""
import os
from string import maketrans
from docopt import docopt

if __name__ == '__main__':
	arguments = docopt(__doc__)
	name = arguments['<name>']
	location = './GameOfThrones/'+name+'/OEBPS/Text'


	for subdir, dirs, files in os.walk(location):
		for f in files:
			novel = open('./'+name+'/'+f.split('.htm')[0],'w')
			f = open(location+'/'+f,'r')
			start = 0
			sign = 0
			replacements = {'&nbsp;':'','’':'\'','“':'"','”':'"','…':'...','—':'-','``':'"','‘':'\'','–':'-','©':''}
			for line in f:
				if '<body>' in line:
					start = 1
				if start == 1:
					for src, target in replacements.iteritems():
						line = line.replace(src, target)
					for c in line:
						if c == '<':
							sign = 1
						if sign == 0:
							novel.write(c)
						if c == '>':
							sign = 0
		f.close()
		novel.close()
