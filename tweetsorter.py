# -*- coding: utf-8 -*-

import sys
import re
import RegexFinder as reg
import unittest
import spellchecker as sc
#import enchant

infile = open(sys.argv[1],'r')
#dictionary = enchant.Dict("en_US")
words_tuple = []
#outfile = open(sys.argv[2],'w')


regexFinder = reg.RegexFinder()

for line in infile:
	
	if line.strip():
			
			tokens = regexFinder.subLine(line)
			#testTag = "excesstag"
			testTag = "jwtag"
			if (regexFinder.numTags(testTag)):
				print line
				new_line=""
				for token in tokens:
					if new_line == "":
						new_line = new_line+token
					else:
						new_line = new_line+" "+token
				print new_line
				print "\n"
			
print regexFinder.num_htags
print regexFinder.num_atags
print regexFinder.num_urltags
print regexFinder.num_jwtags
print regexFinder.num_excesstags

print "\n"
print sc.correct("btwn")


