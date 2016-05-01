
from microsofttranslator import Translator
import json
import sys
import codecs

infile = codecs.open(sys.argv[1],'r',encoding="utf-8")
outfile = codecs.open(sys.argv[2],'w+',encoding="utf-8")
midway = codecs.open("midway.json",'w+',encoding="utf-8")
language = sys.argv[3]
devSet = sys.argv[4]
jsonData = {}

def translatorFunc():
	translator = Translator('fixingtwitter', 'QzR2/Cu4NoaPwnXNuQ5Eknk0uR58ZrWAtcDdjaM+dDM=')

	jsonStr = infile.read()
	jsonData = json.loads(jsonStr)['data']
	

	#[u'ar', u'bg', u'ca', u'zh-CHS', u'zh-CHT', u'cs', u'da', u'nl', u'en', u'et', u'fi', u'fr', u'de', u'el', u'ht', u'he', u'hi', u'mww', u'hu', u'id', u'it', u'ja', u'tlh', u'tlh-Qaak', u'ko', u'lv', u'lt', u'ms', u'mt', u'no', u'fa', u'pl', u'pt', u'ro', u'ru', u'sk', u'sl', u'es', u'sv', u'th', u'tr', u'uk', u'ur', u'vi', u'cy']
	counter = 1
	size = len(jsonData)

	for key in jsonData:

		id_ = jsonData[key]
		orig = id_['orig']
		norm = id_['norm']
		if(devSet == "y"):
			perf = id_['perf']

		print "-----------------------------------------------"
		print str(counter)+" of "+str(size)+" ("+str(key)+")"
		counter += 1

		transOrig = id_['transOrig']
		transNorm = id_['transNorm']

		if (transOrig == u" " or transNorm == u" "):

			try: 
				transOrig = translator.translate(orig,language)
				transNorm = translator.translate(norm,language)
			except translator.ConnectionError:
				pass

			id_['transOrig'] = transOrig
			id_['transNorm'] = transNorm

		
		if (devSet == "y"):
			id_['transPerf'] = translator.translate(perf,language)

		print >> midway, json.dumps({str(key) : id_ },ensure_ascii=False,indent=4,separators=(',', ': '))
		

	print >> outfile, json.dumps({'data': jsonData},ensure_ascii=False, indent=4, separators=(',', ': '))
	outfile.close
	print "translation done"


translatorFunc()

