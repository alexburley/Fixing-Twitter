
import sys
import codecs
import json

infile = codecs.open(sys.argv[1],'r')
outfile = codecs.open(sys.argv[2],'w',encoding="utf-8")

def outputFile():
	jsonStr = infile.read()
	data =json.loads(jsonStr)['data']

	for key in data:

		transOrig = data[key]['transOrig']
		transNorm = data[key]['transNorm']
		perf = data[key]['perf']


		print >> outfile, "----------------------------------------------------"
		print >> outfile, "English Sentence: "+perf
		print >> outfile, "Translation 1: "+transOrig
		print >> outfile, "Translation 2: "+transNorm
		print >> outfile, "Best Translation: "
		print >> outfile, "----------------------------------------------------"


outputFile()