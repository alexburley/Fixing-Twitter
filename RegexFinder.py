import re
import unittest
import spellchecker as sc
#NEED PYTHON 32BIT
import enchant

class RegexFinder:

	def __init__(self):
		self.num_htags = 0
		self.num_atags = 0
		self.num_urltags = 0
		self.num_jwtags = 0
		self.num_excesstags = 0
		self.num_timetags = 0

		self.currentline = ""

	
	def hasTags(self, options):

		flag = 1

		#print options

		if(options['all']):
			return 1
		elif (options['hasExcess']):
			if (self.cur_excesstags > 0):
				return 1
		elif (options['hasJW']):
			if (self.cur_jwtags > 0):
				return 1
		elif (options['hasH']):
			if (self.cur_htags > 0):
				return 1
		elif (options['hasTime']):
			if (self.cur_timetags > 0):
				return 1
		elif (options['hasURL']):
			if (self.cur_urltags > 0):
				return 1
		else:
			return 0

	def tokenizeLine(self,line,htags,atags,jwtags,urltags,timetags):


		line = line.rstrip('\r\n').lower()

		if htags:
			line = self.subHashtags(line)
		if atags:
			line = self.subAccountTags(line)
		if urltags:
			line = self.subURLTags(line)
		if timetags:
			line = self.subTimeTags(line)
		if jwtags:
			line = self.subJoinedWordTags(line)

		#WILL NEED TO STRIP PUNCTUATION HERE TO TOKENISE.
		from string import punctuation
		line = ' '.join(filter(None, (word.strip(punctuation) for word in line.split())))

		#line = self.subExcessLetterTags(line)
		tokens = re.split('\s',line)
		tokens = self.insertExcessLetterTags(tokens)
		return tokens

	def subLine(self,line):	

		tokens = self.tokenizeLine(line,1,1,1,1,1)
		return tokens

	def subHashtags(self,line):
		h_tag = re.compile('#+\w+\S*')
		self.cur_htags = len(re.findall(h_tag,line))
		self.num_htags += self.cur_htags
		line = h_tag.sub('0h_tag0', line)
		return line

	def subAccountTags(self,line):
		a_tag = re.compile('@+\w+\S*')
		self.cur_atags = len(re.findall(a_tag,line))
		self.num_atags += self.cur_atags
		line = a_tag.sub('0a_tag0',line)
		return line
	
	def subURLTags(self,line):

		"""MERGE INTO ONE RE"""
		url_tag = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
		num_urltags1 = len(re.findall(url_tag,line))
		line = url_tag.sub('0url_tag0', line)
		#remove all website that are just xyz.com
		url_tag = re.compile('\w+.com')
		num_urltags2 = len(re.findall(url_tag,line))
		line = url_tag.sub('0url_tag0', line)

		self.cur_urltags = num_urltags1 + num_urltags2
		self.num_urltags += self.cur_urltags
		return line

	def subTimeTags(self,line):
		time_tag = re.compile('[0-9]\.[0-9]')
		self.cur_timetags = len(re.findall(time_tag,line))
		self.num_timetags += self.cur_timetags
		line = time_tag.sub('0time_tag0',line)
		return line


	def subJoinedWordTags(self,line):
		jw_tag = re.compile('((\w+)\.(\w+))')
		self.cur_jwtags = len(re.findall(jw_tag,line))
		self.num_jwtags += self.cur_jwtags
		joinedwords=jw_tag.search(line)
		if joinedwords:
				joinedWords = [joinedwords.group(1),joinedwords.group(2)]
		line = jw_tag.sub('0jw_tag0',line)
		return line

	def subExcessLetterTags(self,line):
		excess_tag = re.compile('\w[a-zA-Z]2+\w?')
		self.cur_excesstags = len(re.findall(excess_tag,line))
		self.num_excesstags += self.cur_excesstags
		line = excess_tag.sub('0el_tag0',line)
		return line

	def insertExcessLetterTags(self,tokens):
		count = 1
		tagCount = 0

		for token in xrange(len(tokens)):
			for char in xrange(len(tokens[token])):
				if (char+1 < len(tokens[token])):
					if (tokens[token][char] == tokens[token][char+1]):
						count += 1
						if count>2:
							tokens[token] = "0el_tag0"
							tagCount += 1
					else: count = 1

		self.cur_excesstags = tagCount
		self.num_excesstags += self.cur_excesstags
		return tokens

	def outputLines(self,infile,options):

		print "-------------------------------------------------------------"
		for line in infile:
			self.currentline = line
			if line.strip():
				tokens = self.subLine(line)
				if (self.hasTags(options)):
					print line
					new_line=""
					for token in tokens:
						if new_line == "":
							new_line = new_line+token
						else:
							new_line = new_line+" "+token
					print new_line
					print "-------------------------------------------------------------"



	




