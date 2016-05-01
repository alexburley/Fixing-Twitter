
import pyter
import nltk
import nltk.translate.bleu_score as bl
import codecs

def naiveInput():
	return 0

def jsonInput():
	return 0

def ter(source,target):
	source = source.split(" ")
	target = target.split(" ")
	val = pyter.ter(source,target)
	if (val == 0):
		return 0
	
	else:
		return '%.3f' % pyter.ter(source, target)
	

def bleu(source, target):
	source = source.encode("utf-8").split(" ")
	target = target.encode("utf-8").split(" ")
	smoothFunc = bl.SmoothingFunction()
	#print source, target
	return bl.sentence_bleu(target,source,weights=[0.25],smoothing_function=smoothFunc.method2)

def retTrue():
	return 1

