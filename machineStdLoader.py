
import json
import codecs

def loadData():

	infile = codecs.open("data.cn-en.json",'r',encoding="utf-8")
	outfile = codecs.open("parallel_data_machine.json", 'w', encoding="utf-8")

	counter = 0
	minimum = 250
	maximum = 350
	jsonDict = {}

	for line in infile:
		
		if ((counter < maximum) & (counter >= minimum)):

			data = json.loads(line)

			orig = data["target"]
			transPerf = data["source"]
			jsonDict[counter] = {'orig':orig, 'norm':" ", 'perf:':" ", 'transOrig':" ", 'transNorm':" ", 'transPerf':transPerf};
		
		counter += 1

		if (counter>maximum):
			break

	print >> outfile, json.dumps({'data': jsonDict},ensure_ascii=False, indent=4, separators=(',', ': '))
	outfile.close()

loadData()