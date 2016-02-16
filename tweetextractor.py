# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 19:12:34 2015

@author: Alexander
"""

import sys
import re

infile = open(sys.argv[1],'r')
outfile = open(sys.argv[2],'w')
start = sys.argv[3]
end = sys.argv[4]


def printOut(base,max):
    
    lineCount = 0

    for line in infile:
    	if(lineCount >= start & lineCount <= end):
        	print >>outfile, line
        	if (lineCount == max):
            	break
        lineCount += 1

printOut(start,end)