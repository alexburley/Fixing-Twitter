
import pyter
import nltk
import nltk.translate.bleu_score as bl

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
	source = source.split(" ")
	target = target.split(" ")
	smoothFunc = bl.SmoothingFunction()
	print source, target
	return bl.sentence_bleu(target,source,weights=[0.25],smoothing_function=smoothFunc.method5)

def retTrue():
	return 1

