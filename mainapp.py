# -*- coding: utf-8 -*-

import sys
import re
import RegexFinder as reg
import unittest
import spellchecker as sc
import TweetComparison as tc
import enchant
import Tkinter
import os
import json
from tkFileDialog import askopenfilename

"""

Main App constructs the GUI and the controls for which to access the program

"""

class mainApp(Tkinter.Tk):

	#top = Tkinter.Tk()
	# Code to add widgets will go here...
	#top.mainloop()


	#Initialise the class with the parent being the TKinter initialisation
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.filePath = "test_tweets.txt"
		self.inputJSON = "OutputJSON.txt"
		self.initialize()

	#Initialise GUI with all the controls we will be using
	def initialize(self):
		#Use a grid layout for our TKinter widgets
		self.grid()

		#First row of widgets
		y = 0

		#Button from which we will run our code
		self.runCode = Tkinter.Button(self,text=u"Run Code", command = self.onButtonClick)
		self.runCode.grid(column=0,row=y)

		#Bring up a window to open a file we want to use
		self.fileOpen = Tkinter.Button(self,text="File",command=self.onFileClick)
		self.fileOpen.grid(column=1,row=y)

		#Label containing the name of the current uploaded file in the system
		self.uploadedFile = Tkinter.Label(self,text="No File Uploaded")
		self.uploadedFile.grid(column=2,row=y)

		self.minValue = Tkinter.StringVar()
		self.minEntry = Tkinter.Entry(self,textvariable=self.minValue)
		self.minEntry.grid(column=3, row=y)

		self.maxValue = Tkinter.StringVar()
		self.maxEntry = Tkinter.Entry(self, textvariable=self.maxValue)
		self.maxEntry.grid(column=4, row=y)

		self.extractButton = Tkinter.Button(self, text="Extract", command=self.extractTweets())
		self.extractButton.grid(column=5,row=y)

		#self.cwd = Tkinter.Label(self,text=os.getcwd())
		#self.cwd.grid(column=3,row=0)

		#row 1
		y += 1

		#If we want to search tweets containing only a specific tags
		self.searchTags = Tkinter.Label(self,text="Output tweets with:")
		self.searchTags.grid(column=0,row=y)

		self.minLine = Tkinter.Label(self,text="Min Line")
		self.minLine.grid(column=3,row=y)		

		self.maxLine = Tkinter.Label(self,text="Max Line")
		self.maxLine.grid(column=4,row=y)				

		#row 2
		y += 1

		#All tags
		self.all = Tkinter.IntVar()
		self.all.set(1)
		self.allbox = Tkinter.Checkbutton(self, text="All",variable = self.all)
		self.allbox.grid(column=0,row=y)
		
		#Joined Word Tags
		self.jwtag = Tkinter.IntVar()
		self.jwbox = Tkinter.Checkbutton(self, text="JW Tag",variable = self.jwtag)
		self.jwbox.grid(column=1,row=y)

		#Excess letter tags
		self.excesstag = Tkinter.IntVar()
		self.excessbox = Tkinter.Checkbutton(self, text="Excess Tag",variable=self.excesstag)
		self.excessbox.grid(column=2,row=y)

		#Hash Tags
		self.htag = Tkinter.IntVar()
		self.hbox = Tkinter.Checkbutton(self, text="Hash Tag",variable=self.htag)
		self.hbox.grid(column=3,row=y)

		#Time/Date Tags
		self.timetag = Tkinter.IntVar()
		self.timebox = Tkinter.Checkbutton(self, text="Time Tag",variable = self.timetag)
		self.timebox.grid(column=4,row=y)

		#URL Tags
		self.urltag = Tkinter.IntVar()
		self.urlbox = Tkinter.Checkbutton(self, text="URL tag",variable = self.urltag)
		self.urlbox.grid(column=5,row=y)

		#y = 3

		#Below we will list all the normalisation methods that we will use
		#useNormalisationMethods = Tkinter.Label(self,text="Use Normalisation Methods")
		#useNormalisationMethods.grid(column=0,row=y)

		#row 3
		y += 1

		self.num_htags = Tkinter.Label(self,text="HTags: 0")
		self.num_htags.grid(column=0,row=y)

		self.num_jwtags = Tkinter.Label(self,text="JWTags: 0")
		self.num_jwtags.grid(column=1,row=y)

		self.num_excesstags = Tkinter.Label(self,text="ExcessTags: 0")
		self.num_excesstags.grid(column=2,row=y)

		self.num_URLtags = Tkinter.Label(self,text="URLTags: 0")
		self.num_URLtags.grid(column=3,row=y)


		#row4
		y += 1

		self.normalizationTitle = Tkinter.Label(self,text="Normalization Technique Selection")
		self.normalizationTitle.grid(column=0,row=y)

		#row5
		y += 1

		self.hashTagN = Tkinter.IntVar()
		self.hashTagB = Tkinter.Checkbutton(self, text="Hashtags", variable = self.hashTagN)
		self.hashTagN.set(1)
		self.hashTagB.grid(column=0,row=y)

		self.joinedWordsN = Tkinter.IntVar()
		self.joinedWordsN.set(1)
		self.joinedWordsB = Tkinter.Checkbutton(self, text="JoinedWords", variable =self.joinedWordsN)
		self.joinedWordsB.grid(column=1,row=y)

		self.accTagN = Tkinter.IntVar()
		self.accTagN.set(1)
		self.accTagB = Tkinter.Checkbutton(self,text="AccountTags",variable = self.accTagN)
		self.accTagB.grid(column=2,row=y)

		self.urlTagN = Tkinter.IntVar()
		self.urlTagN.set(1)
		self.urlTagB =Tkinter.Checkbutton(self,text="URLs",variable=self.urlTagN)
		self.urlTagB.grid(column=3,row=y)

		self.timeTagN = Tkinter.IntVar()
		self.timeTagN.set(0)
		self.timeTagB = Tkinter.Checkbutton(self,text="Timestamps", variable=self.timeTagN)
		self.timeTagB.grid(column=4,row=y)

		self.spellcheckN =Tkinter.IntVar()
		self.spellcheckN.set(1)
		self.spellcheckB = Tkinter.Checkbutton(self,text="Spellcheck",variable=self.spellcheckN)
		self.spellcheckB.grid(column=5,row=y)

		self.excessTagN = Tkinter.IntVar()
		self.excessTagN.set(1)
		self.excessTagB = Tkinter.Checkbutton(self, text= "ExcessLetters",variable=self.excessTagN)
		self.excessTagB.grid(column=6,row=y)

		#row6
		y += 1

		self.translationLabelAuto = Tkinter.Label(self,text="Evaluation (Auto")
		self.translationLabelAuto.grid(column=0,row=y)

		#row7
		y += 1

		self.translatedFileOpen = Tkinter.Button(self,text="Data File",command=self.uploadTranslatedFile)
		self.translatedFileOpen.grid(column=0,row=y)

		self.translatedFileLabel = Tkinter.Label(self,text="No File")
		self.translatedFileLabel.grid(column=1,row=y)

		self.evaluateAuto = Tkinter.Button(self,text="Evaluate",command=self.evaluateAuto)
		self.evaluateAuto.grid(column=2,row=y)

		self.origAutoLabel = Tkinter.Label(self,text="Original")
		self.origAutoLabel.grid(column=3,row=y)


		self.bleuLabelOrigAuto = Tkinter.Label(self,text="BLEU: ")
		self.bleuLabelOrigAuto.grid(column=4,row=y)

		self.terLabelOrigAuto = Tkinter.Label(self,text="TER: ")
		self.terLabelOrigAuto.grid(column=5,row=y)


		y += 1

		self.normAutoLabel = Tkinter.Label(self,text="Normalized")
		self.normAutoLabel.grid(column=3,row=y)

		self.bleuLabelNormAuto = Tkinter.Label(self,text="BLEU: ")
		self.bleuLabelNormAuto.grid(column = 4, row =y)

		self.terLabelNormAuto = Tkinter.Label(self,text="TER: ")
		self.terLabelNormAuto.grid(column=5, row=y)

		#row8
		y += 1

		self.translationlabelMan = Tkinter.Label(self,text="Evaluation (Manual)")
		self.translationlabelMan.grid(column=0,row=y)

		#row9
		y += 1

		self.origTweetLabel = Tkinter.Label(self,text="Enter Tweet")
		self.origTweetLabel.grid(column=0,row=y)

		self.origTweet = Tkinter.StringVar()
		self.origTweetEntry = Tkinter.Entry(self,textvariable=self.origTweet)
		self.origTweetEntry.grid(column=1, row=y)
		
		self.normTweetLabel = Tkinter.Label(self,text="Normalized")
		self.normTweetLabel.grid(column=2,row=y)

		self.normTweet = Tkinter.StringVar()
		self.normTweetEntry = Tkinter.Entry(self,textvariable=self.normTweet)
		#self.normTweetEntry.insert(0,"Hello")
		self.normTweetEntry.grid(column=3,row=y)

		self.perfTweetLabel = Tkinter.Label(self,text="Perfect English")
		self.perfTweetLabel.grid(column=4,row=y)

		self.perfTweet = Tkinter.StringVar()
		self.perfTweetEntry = Tkinter.Entry(self,textvariable=self.perfTweet)
		self.perfTweetEntry.grid(column=5,row=y)

		self.numSubsLabelText = Tkinter.Label(self,text="#Substitutions: ")
		self.numSubsLabelText.grid(column=6,row=y)

		self.numSubsLabel = Tkinter.Label(self,text="-")
		self.numSubsLabel.grid(column=7,row=y)

		#row10
		y += 1

		self.translatedOrigLabel = Tkinter.Label(self,text="Translated Original")
		self.translatedOrigLabel.grid(column=0,row=y)

		self.translatedOrig = Tkinter.StringVar()
		self.translatedOrigEntry = Tkinter.Entry(self,textvariable=self.translatedOrig)
		self.translatedOrigEntry.grid(column=1,row=y)
		self.translatedOrigEntry.insert(0,"Sommes-nous #winers enfin? #LFC")

		self.translatedNormalizedLabel = Tkinter.Label(self,text="Translated Normalized")
		self.translatedNormalizedLabel.grid(column=2,row=y)

		self.translatedNormalized = Tkinter.StringVar()
		self.translatedNormalizedEntry = Tkinter.Entry(self,textvariable=self.translatedNormalized)
		self.translatedNormalizedEntry.grid(column=3,row=y)
		self.translatedNormalizedEntry.insert(0,"sommes-nous gagnants enfin bla bla don simon is my dad")

		self.translatedPerfLabel = Tkinter.Label(self,text="Translated Perfect")
		self.translatedPerfLabel.grid(column=4,row=y)

		self.translatedPerf = Tkinter.StringVar()
		self.translatedPerfEntry = Tkinter.Entry(self,textvariable=self.translatedPerf)
		self.translatedPerfEntry.grid(column=5,row=y)
		self.translatedPerfEntry.insert(0,"sommes-nous gagnants enfin")

		#row 11
		y += 1

		#Bring up a window to open a file we want to use
		

		#row 12
		y += 1

		self.normalize = Tkinter.Button(self,text="Normalize",command=self.normalize)
		self.normalize.grid(column=2,row=y)

		self.eval = Tkinter.Button(self,text="Evaluate",command=self.evaluateMan)
		self.eval.grid(column=3,row=y)

		#row13

		y += 1

		self.metricLabel = Tkinter.Label(self,text="Metrics")
		self.metricLabel.grid(column=3,row=y)

		#row14
		y += 1

		self.bleuLabelOriginal = Tkinter.Label(self,text="Bleu: ")
		self.bleuLabelOriginal.grid(column=1,row=y)

		self.bleuLabelNormalised = Tkinter.Label(self,text="Bleu: ")
		self.bleuLabelNormalised.grid(column=3,row=y)

		self.bleuLabelPerf = Tkinter.Label(self,text = "Bleu: ")
		self.bleuLabelPerf.grid(column = 5, row=y)

		#row15
		y += 1

		self.terLabelOriginal = Tkinter.Label(self,text="TER: ")
		self.terLabelOriginal.grid(column=1,row=y)

		self.terLabelNormalised = Tkinter.Label(self, text="TER: ")
		self.terLabelNormalised.grid(column=3,row=y)

		self.terLabelPerf = Tkinter.Label(self, text="TER: ")
		self.terLabelPerf.grid(column=5,row=y)




		#Configure grid and display
		self.grid_columnconfigure(0,weight=1)



		#Options to resize window
		#resizingallowed(x,y)
		#self.resizable(True,False)

	def onButtonClick(self):
		self.mainCode()

	def onFileClick(self):
		self.filePath = askopenfilename()
		self.uploadedFile = Tkinter.Label(self,text=self.filePath)
		self.uploadedFile.grid(column=2,row=0)

	def uploadTranslatedFile(self):
		self.filePath = askopenfilename()

	def evaluateMan(self):

		original = self.translatedOrig.get()
		normalized = self.translatedNormalized.get()
		perfect = self.translatedPerf.get()

		terOriginal = tc.ter(original, perfect)
		terNormalized = tc.ter(normalized,perfect)
		terPerf = tc.ter(perfect,perfect)

		print "Translated Original = "+original+" -TER- "+str(terOriginal)
		print "Translated Normalized = "+normalized+" -TER- "+str(terNormalized)
		print "Translated Perfect = "+perfect+" -TER- "+str(terPerf)

		self.terLabelOriginal.config(text="TER: "+str(terOriginal))
		self.terLabelNormalised.config(text="TER: "+str(terNormalized))
		self.terLabelPerf.config(text="TER: "+str(terPerf))

		print "\n"

		bleuOriginal = tc.bleu(original,perfect)
		bleuNormalized = tc.bleu(normalized,perfect)
		bleuPerfect = tc.bleu(perfect,perfect)

		print "Translated Original = "+original+" -BLEU- "+str(bleuOriginal)
		print "Translated Normalized = "+normalized+" -BLEU- "+str(bleuNormalized)
		print "Translated Perfect = "+perfect+" -BLEU- "+str(bleuPerfect)

		self.bleuLabelOriginal.config(text="BLEU: "+str(bleuOriginal))
		self.bleuLabelNormalised.config(text="BLEU: "+str(bleuNormalized))
		self.bleuLabelPerf.config(text="BLEU: "+str(bleuPerfect))

	def evaluateAuto(self):
		jsonFile = open(self.inputJSON)
		jsonStr = jsonFile.read()
		jsonData = json.loads(jsonStr)['data']

		size = len(jsonData)
		avgOrigBleu= 0
		avgNormBleu = 0
		avgOrigTER = 0
		avgNormTER = 0


		for key in jsonData:

			original = jsonData[key]['transOrig']
			normalized = jsonData[key]['transNorm']
			perfect = jsonData[key]['transPerf']

			terOriginal = tc.ter(original, perfect)
			terNormalized = tc.ter(normalized,perfect)
			terPerf = tc.ter(perfect,perfect)

			"""
			print "Translated Original = "+original+" -TER- "+str(terOriginal)
			print "Translated Normalized = "+normalized+" -TER- "+str(terNormalized)
			print "Translated Perfect = "+perfect+" -TER- "+str(terPerf)
			"""

			#print "\n"

			bleuOriginal = tc.bleu(original,perfect)
			bleuNormalized = tc.bleu(normalized,perfect)
			bleuPerfect = tc.bleu(perfect,perfect)


			"""
			print "Translated Original = "+original+" -BLEU- "+str(bleuOriginal)
			print "Translated Normalized = "+normalized+" -BLEU- "+str(bleuNormalized)
			print "Translated Perfect = "+perfect+" -BLEU- "+str(bleuPerfect)
			"""

			avgOrigBleu += bleuOriginal
			avgNormBleu += bleuNormalized
			avgOrigTER += terOriginal
			avgNormTER += terNormalized

		avgOrigBleu = avgOrigBleu/size
		avgNormBleu = avgNormBleu/size
		avgOrigTER = avgOrigTER/size
		avgNormTER = avgNormTER/size

		self.terLabelOrigAuto.config(text="TER: "+str(avgOrigTER))
		self.bleuLabelOrigAuto.config(text="BLEU: "+str(avgOrigBleu))

		self.terLabelNormAuto.config(text="TER: "+str(avgNormTER))
		self.bleuLabelNormAuto.config(text="BLEU: "+str(avgNormBleu))


		#print jsonData

	def normalize(self):
		regexFinder = reg.RegexFinder()
		tweet = self.origTweet.get()
		options = self.returnOptions()
		normTweet = regexFinder.returnNormTweet(tweet,options)
		if(len(self.normTweetEntry.get()) > 0):
			self.normTweetEntry.delete(0,len(normTweet))
		self.normTweetEntry.insert(0,normTweet)


	def extractTweets(self):
		min = self.minValue.get()
		max = self.maxValue.get()

		def printOut(base,max):

			outfile = open("tweets--"+str(base)+"--"+str(max)+".txt", 'w')
			infile = open("tweetsforanalysis.en",'r')
			lineCount = 1

			for line in infile:
				if(lineCount >= base):
					print >>outfile, line
					if (lineCount == max):
						break
				lineCount += 1

			return os.getcwd()+outfile

		#filepath = printOut(min,max)
		#print filepath

	def returnOptions(self):
		options = {}
		options['hasJW'] = self.jwtag.get()
		options['hasExcess'] = self.excesstag.get()
		options['hasH'] = self.htag.get()
		options['hasTime'] = self.timetag.get()
		options['hasURL'] = self.urltag.get()
		options['all'] = self.all.get()
		options['normHTag'] = self.hashTagN.get()
		options['normATag'] = self.accTagN.get()
		options['normURLTag'] = self.urlTagN.get()
		options['normTimeTag'] = self.timeTagN.get()
		options['normSpellcheck'] = self.spellcheckN.get()
		options['normJWTag'] = self.joinedWordsN.get()
		options['normExcessTag'] = self.excessTagN.get()
		return options


	def mainCode(self):

		infile = open(self.filePath,'r')
		regexFinder = reg.RegexFinder()
		options = self.returnOptions()
		print "\n \n \nFinding and substituting regular expressions on filepath \n \n \n"
		regexFinder.outputLines(infile,options)

		self.num_htags.config(text="HTags: "+str(regexFinder.num_htags))
		self.num_jwtags.config(text="JWTags: "+str(regexFinder.num_jwtags))
		self.num_excesstags.config(text="ExcessTags: "+str(regexFinder.num_excesstags))
		self.num_URLtags.config(text="URLTags: "+str(regexFinder.num_urltags))
		self.numSubsLabel.config(text=str(regexFinder.total_subs))



if __name__ == "__main__":

	app = mainApp(None)
	app.title('Fixing-Twitter by Alex Burley')
	app.mainloop()