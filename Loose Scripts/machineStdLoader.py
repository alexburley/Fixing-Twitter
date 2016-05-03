
import json
import codecs

def loadData():

	infile = codecs.open("data.en-ru.json",'r',encoding="utf-8")
	outfile = codecs.open("E4_T2.txt", 'w', encoding="utf-8")

	counter = 0
	#minimum = 250
	#maximum = 350

	minimum = 0
	maximum = 2050
	jsonDict = {}

	for line in infile:
		
		if ((counter < maximum) & (counter >= minimum)):

			data = json.loads(line)

			#CHANGE FOR RUS OR CHIN
			orig = data["source"]
			transPerf = data["target"]
			jsonDict[counter] = {'orig':orig, 'norm':" ", 'perf:':" ", 'transOrig':" ", 'transNorm':" ", 'transPerf':transPerf};
		
		counter += 1

		if (counter>maximum):
			break

	print >> outfile, json.dumps({'data': jsonDict},ensure_ascii=False, indent=4, separators=(',', ': '))
	outfile.close()

loadData()