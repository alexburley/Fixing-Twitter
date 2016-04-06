
import pyter


def naiveInput():
	return 0

def jsonInput():
	return 0

def ter(source,target):
	source = source.split(" ")
	target = target.split(" ")
	return '%.3f' % pyter.ter(source, target)

def bleu(source, target):
	return 0
