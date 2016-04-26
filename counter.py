import sys
import codecs

infile = codecs.open(sys.argv[1],'r',encoding="utf-8")
json = open(sys.argv[2])

counter = 0

if(str(json) is not "y"):
	for line in infile:
		counter += 1
	print counter
else:
	jsonStr = infile.read()
