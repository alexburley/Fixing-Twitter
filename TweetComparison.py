
import pyter
import nltk


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
	#source = source.split(" ")
	#target = target.split(" ")
	weights = [0.25]
	return nltk.bleu(source,[target],weights)


