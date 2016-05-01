
import json
import codecs

def loadData():

	infile = codecs.open("parallel.gold.en-ru",'r',encoding="utf-8")
	outfile = codecs.open("E4_T2.txt", 'w', encoding="utf-8")

	jsonDict = {}
	counter = 1
	for line in infile:

		print counter
		
		data = line.split("|||")
		print data[0].strip().encode("utf-8")
		jsonDict[counter] = {'orig':data[0].strip(), 'norm':" ", 'perf:':" ", 'transOrig':" ", 'transNorm':" ", 'transPerf':data[1].strip()};
		counter += 1

	print >> outfile, json.dumps({'data': jsonDict}, ensure_ascii=False, indent=4, separators=(',', ': '))
	outfile.close()

loadData()