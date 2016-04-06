
import pyter


def naiveInput(self):
	return 0

def jsonInput(self):
	return 0

def terComparison(self,source,target):
	source = source.split(" ")
	target = target.split(" ")
	return '%.3f' % pyter.ter(source, target)

def bleuComparison(self):
	return 0
