import re
import unittest
import spellchecker as sc
#NEED PYTHON 32BIT
import enchant
from string import punctuation
import json

"""

Notes: Date lengthening from sep to september is present in google translate

"""


class RegexFinder:

	def __init__(self):
		self.num_htags = 0
		self.num_atags = 0
		self.num_urltags = 0
		self.num_jwtags = 0
		self.num_excesstags = 0
		self.num_timetags = 0
		self.num_rttags = 0
		self.total_subs = 0
		self.total_chars = 0
		self.slang_dict = {}
		self.corpus_loaded = 0
		self.outfile = "output.txt"

		self.currentline = ""
		self.d = enchant.Dict("en_GB")

	def initializeSlang(self):

		self.slang_dict["lol"] = "laugh out loud"
		self.slang_dict["g2g"] = "got to go"
		self.slang_dict["b4"] = "before"
		self.slang_dict["gr8"] = "great"
		self.slang_dict["2morrow"] = "tomorrow"
		self.slang_dict["2geva"] = "together"
		self.slang_dict["r"] = "are"
		self.slang_dict["u"] = "you"

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

	def tokenizeLine(self,line,htags,atags,jwtags,urltags,excesstags,timetags,spellcheck):

		line = line.rstrip('\r\n').lower()

		if (self.outfile[len(self.outfile)-1] != "."):
			self.outfile = self.outfile+"."

		if htags:
			line = self.subHashtags(line)
			self.outfile = self.outfile+"h"
		if atags:
			line = self.subAccountTags(line)
			self.outfile = self.outfile+"a"
		if urltags:
			line = self.subURLTags(line)
			self.outfile = self.outfile+"u"
		if timetags:
			line = self.subTimeTags(line)
			self.outfile = self.outfile+"t"
		if jwtags:
			line = self.subJoinedWordTags(line)
			self.outfile = self.outfile+"j"
		if excesstags:
			line = self.subExcessLetterTags(line)
			self.outfile = self.outfile+"e"
		#if excesstags:
			#line = self.subExcessLetterTags(line)

		line = self.subUniCode(line)
		line = self.subRetweet(line)
		
		self.total_chars += len(line)
		line = ' '.join(filter(None, (word.strip(punctuation) for word in line.split())))

		#line = self.subExcessLetterTags(line)
		tokens = re.split('\s',line)

		if spellcheck:
			tokens = self.sub_spelling(tokens)

		if (self.outfile[len(self.outfile)-1] != "."):
			self.outfile = self.outfile+"."
		
		self.outfile = self.outfile+"txt"
		return tokens

	def subLine(self,line):	
		tokens = self.tokenizeLine(line,self.options['normHTag'],self.options['normATag'],
			self.options['normJWTag'],self.options['normURLTag'],self.options['normExcessTag'],
				self.options['normTimeTag'],self.options['normSpellcheck'])
		return tokens

	def sub_abbreviations(self,tokens):

		def abbrevReplace(m):
			self.total_subs += 1
			if (m == "u"):
				return "you"
			

	"""Use regex for dont and arent to turn into do not and are"""
	def sub_spelling(self,tokens):

		self.outfile = self.outfile+"s"

		def spellReplace(m):
			self.total_subs += 1
			if (not self.d.check(m)):
				if (len(self.d.suggest(m))>0):
					#print self.d.suggest(m)
					return self.d.suggest(m)[0]
				else:
					return m
			else:
				return m

		return map(spellReplace,tokens)

	"""
	Approach 1: Sub in the index of the token (in the original substitution then track back)
	Approach 2: 


	"""

	""" WHAT ABOUT punctuation hashtags like #l'pool

		We want to check if the hashtag is part of the sentence of the tweet. If not we can remove it
		if it is at the end of the tweet. Or we can insert a placeholder. Use a list with a tuple of a (t)

		Approach: for each match we perform operations to determine whether the hashtag is part of the sentence:

		e.g "I hope #LFC #win today" : "I hope 0h_tag0 win today".
		e.g "I hope we win today #LFC #Winners" : "I hope we win today"

		WHAT ABOUT #soso dis.connected CONFLICT between hashtags and joined words


	"""
	def subHashtags(self,line):
		h_tag = re.compile('(#)+(\w+)')
		self.cur_htags = len(re.findall(h_tag,line))
		self.num_htags += self.cur_htags

		def normalizeHashtags(m):
			#RECURSE BACKWARDS
			self.total_subs += 1
			htag = m.group(2)
			end = m.end()
			#IF the hashtag is not the last word in the tweet
			if (end+2<len(line)):
				#if the word after the hashtag is not another hashtag
				if(line[end+2] != '#'):
					#If the word is in the dictionary
					if(self.d.check(htag)):
						return htag
					else:
						"""This may be an opportunity to solve the misspelled hashtags problem or joined words"""
						return '0h_tag0'
				#ELSE if it is another hashtag
				else:
					print "returned group (h_tag)"
					return m.group()
			#ELSE if is is the last word it is likely not part of the tweets meaning
			else:
				return ""

		line = h_tag.sub(normalizeHashtags, line)

		return line

	def subAccountTags(self,line):
		a_tag = re.compile('@+\w+\S*')
		self.cur_atags = len(re.findall(a_tag,line))
		self.num_atags += self.cur_atags

		def normalizeAccountTag(m):
			self.total_subs += 1
			start = m.start()
			if (start == 0):
				return ""
			else:
				return '0acc_tag0'
		line = a_tag.sub(normalizeAccountTag,line)
		return line

	def subURLTags(self,line):

		"""MERGE INTO ONE RE"""
		url_tag = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
		num_urltags1 = len(re.findall(url_tag,line))

		def normalizeURLTag(m):
			self.total_subs += 1
			"""
			end = m.end()
			if (end == len(line)):
				return ""
			else:
				return ''
			"""
			return '0url_tag0'

		line = url_tag.sub(normalizeURLTag, line)

		#remove all website that are just xyz.com
		url_tag = re.compile('\w+\.com')
		num_urltags2 = len(re.findall(url_tag,line))
		line = url_tag.sub(normalizeURLTag, line)

		self.cur_urltags = num_urltags1 + num_urltags2
		self.num_urltags += self.cur_urltags
		return line



	"""IS THIS NECESSARY?"""
	def subTimeTags(self,line):
		time_tag = re.compile('[0-9]\.[0-9]')
		self.cur_timetags = len(re.findall(time_tag,line))
		self.num_timetags += self.cur_timetags
		line = time_tag.sub('0time_tag0',line)
		return line

	"""
		what about elipses
	"""
	def subJoinedWordTags(self,line):
		jw_tag = re.compile('(\w+)\.(\w+)')
		self.cur_jwtags = len(re.findall(jw_tag,line))
		self.num_jwtags += self.cur_jwtags
		joinedwords=re.findall(jw_tag,line)

		"""
			Potentially make a list of common words that we can suggest to, machine learning?

		"""

		def normalizeJoinedWordTags(m):

			self.total_subs += 1

			w1 = m.group(1)
			w2 = m.group(2)

			if (w1.isdigit()):
				self.total_subs = self.total_subs - 1
				return m.group()

			w1Check = self.d.check(w1)
			w2Check = self.d.check(w2)

			if (len(self.d.suggest(w1))>0):
				w1New = self.d.suggest(w1)[0]
			else:
				w1New = ""

			if(len(self.d.suggest(w2))>0):
				w2New = self.d.suggest(w2)[0]
			else:
				w2New = ""
			#check for more than 1 fullstop
			if (not w1Check or not w2Check):
				#print w1+": "+w1New
				#print w2+": "+w2New
				if (self.d.check(w1+w2)):
					return w1+w2
				else:
					return w1+" "+w2
			else:
				return w1+" "+w2

		line = jw_tag.sub(normalizeJoinedWordTags,line)
		return line


	"""
		What about numbers, what about roman numerals.
		MENTION IN DISS ABOUT TESTING GOOGLE TRANSLATE 
		MENTION ABOUT CUTTING DOWN TO SINGLE LETTER
	"""
	def subExcessLetterTags(self,line):
		excess_tag = re.compile(r'(.)\1{2,}')
		self.cur_excesstags = len(re.findall(excess_tag,line))
		self.num_excesstags += self.cur_excesstags

		def normalizeExcessLetterTags(m):
			self.total_subs += 1
			return m.group(1)*1

		line = excess_tag.sub(normalizeExcessLetterTags,line)
		return line

	def subUniCode(self,line):
		unicode_tag = re.compile('\\u[0-9]+[a-zA-Z]*')

		def normalizeUniCode(m):
			self.total_subs += 1
			return ''
		line = unicode_tag.sub(normalizeUniCode,line)
		return line

	def subRetweet(self,line):

		rt_tag = re.compile('\\brt\\b')

		def normalizeRT(m):
			#print "SUB RT"
			self.num_rttags += 1
			self.total_subs += 1
			return ''

		line = rt_tag.sub(normalizeRT,line)

		return line

	def returnLine(self,tokens):

		new_line= ""
		for token in tokens:
			if new_line == "":
				new_line = new_line+token
			else:
				new_line = new_line+" "+token

		return new_line

	def outputLines(self,infile,options):

		self.options = options
		jsonDict = {}
		counter = 0

		print "-------------------------------------------------------------"
		output = open(self.outfile,'w+')
		for line in infile:
			self.currentline = unicode(line)
			if line.strip():
				tokens = self.subLine(line)
				if (self.hasTags(options)):
					counter += 1
					print line
					new_line = self.returnLine(tokens)
					jsonDict[counter] = {'orig':line.strip(), 'norm':new_line, 'perf:':" ", 'transOrig':" ", 'transNorm':" ", 'transPerf':" "};
					print new_line

					
					print "-------------------------------------------------------------"
					"""
					print >> output, "Original: ", line.strip()
					print >> output, "Normalised: ", new_line
					print >> output, "Perfect Normalised: "
					print >> output, "Translated Original: "
					print >> output, "Translated Normalised: "
					print >> output, "Perfect Translation: "
					print >> output, "\n"
					"""
		#print jsonDict
		print >> output, json.dumps({'data': jsonDict},sort_keys=True, indent=4, separators=(',', ': '))
		output.close()

	def returnNormTweet(self,tweet,options):
		self.options = options
		if tweet.strip():
			tokens = self.subLine(unicode(tweet))
			return self.returnLine(tokens)
	




	




