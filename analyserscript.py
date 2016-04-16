import enchant
import sys
import re
infile = open(sys.argv[1],'r')
outfile = open(sys.argv[2],'w')

d = enchant.Dict("en_GB")

for line in infile:
	words = re.findall('\w+',line)
	if(len(words)):
		word = words[0]
	else:
		word = "N/A"
	if (not d.check(word)):
		print >> outfile, word