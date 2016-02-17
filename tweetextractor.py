# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 19:12:34 2015

@author: Alexander
"""

import sys
import re

infile = open(sys.argv[1],'r')
#Alternate method will automatically generate name
#outfile = open(sys.argv[2],'w')
start = sys.argv[2]
end = sys.argv[3]


#PRINTING OUT ALL UP TO BASE
def printOut(base,max):

	outfile = open(sys.argv[1]+"extracted"+str(base)+"--"+str(max)+".txt", 'w')
	lineCount = 1

	for line in infile:
		print lineCount >= base
		print lineCount <= max
		print base
		if(lineCount >= base):
			print >>outfile, line
			if (lineCount == max):
				break
		lineCount += 1

printOut(int(start),int(end))