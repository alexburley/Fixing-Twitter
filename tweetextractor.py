# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 19:12:34 2015

@author: Alexander
"""

import sys
import re
import os.path

#infile = open(sys.argv[1],'r')
#Alternate method will automatically generate name
#outfile = open(sys.argv[2],'w')
#start = sys.argv[2]
#end = sys.argv[3]


#PRINTING OUT ALL UP TO BASE
def output(base,max,infile_path):

	infile = open(str(infile_path),'r')
	outfile_path = os.path.join('/originaltweets/',str(infile_path)+"extracted"+str(base)+"--"+str(max)+".txt")
	outfile = open(outfile_path, 'w')
	lineCount = 1

	for line in infile:
		if(lineCount >= base):
			print >>outfile, line
			if (lineCount == max):
				break
		lineCount += 1

#printOut(int(start),int(end))