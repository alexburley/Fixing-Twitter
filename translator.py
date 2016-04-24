
from microsofttranslator import Translator
import json
import sys
import codecs

infile = codecs.open(sys.argv[1],'r',encoding="utf-8")
outfile = codecs.open(sys.argv[2],'w+',encoding="utf-8")
language = sys.argv[3]
devSet = sys.argv[4]
jsonData = {}

def translatorFunc():
	translator = Translator('fixingtwitter', 'QzR2/Cu4NoaPwnXNuQ5Eknk0uR58ZrWAtcDdjaM+dDM=')

	jsonStr = infile.read()
	jsonData = json.loads(jsonStr)['data']
	

	counter = 1
	size = len(jsonData)

	for key in jsonData:
		id_ = jsonData[key]
		orig = id_['orig']
		norm = id_['norm']
		if(devSet == "y"):
			perf = id_['perf']

		transOrig = translator.translate(orig,language)
		transNorm = translator.translate(norm,language)

		id_['transOrig'] = transOrig
		id_['transNorm'] = transNorm

		print "-----------------------------------------------"
		print str(counter)+" of "+str(size)
		counter += 1
		
		if (devSet == "y"):
			id_['transPerf'] = translator.translate(perf,language)
		

	print >> outfile, json.dumps({'data': jsonData},ensure_ascii=False, indent=4, separators=(',', ': '))
	outfile.close
	print "translation done"


translatorFunc()

