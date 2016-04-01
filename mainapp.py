# -*- coding: utf-8 -*-

import sys
import re
import RegexFinder as reg
import unittest
import spellchecker as sc
import enchant
import Tkinter
import os
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
		self.initialize()

	#Initialise GUI with all the controls we will be using
	def initialize(self):
		#Use a grid layout for our TKinter widgets
		self.grid()

		#First row of widgets
		y = 0

		#Button from which we will run our code
		"""RENAME TO MEANINGFUL VARIABLE"""
		self.button = Tkinter.Button(self,text=u"Run Code", command = self.onButtonClick)
		self.button.grid(column=0,row=y)

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

		y = 1

		#If we want to search tweets containing only a specific tags
		searchTags = Tkinter.Label(self,text="Output tweets with:")
		searchTags.grid(column=0,row=y)		

		y = 2

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

		y = 4

		self.num_htags = Tkinter.Label(self,text="HTags: 0")
		self.num_htags.grid(column=0,row=y)

		self.num_jwtags = Tkinter.Label(self,text="JWTags: 0")
		self.num_jwtags.grid(column=1,row=y)

		self.num_excesstags = Tkinter.Label(self,text="ExcessTags: 0")
		self.num_excesstags.grid(column=2,row=y)

		self.num_URLtags = Tkinter.Label(self,text="URLTags: 0")
		self.num_URLtags.grid(column=3,row=y)



		y = 5

		self.normalizationTitle = Tkinter.Label(self,text="Normalization Technique Selection")
		self.normalizationTitle.grid(column=0,row=y)

		y = 6

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
		self.timeTagN.set(1)
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

	def mainCode(self):

		infile = open(self.filePath,'r')
		regexFinder = reg.RegexFinder()
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
		print "\n \n \nFinding and substituting regular expressions on filepath \n \n \n"
		regexFinder.outputLines(infile,options)
		print regexFinder.total_chars

		y = 4

		self.num_htags = Tkinter.Label(self,text="HTags: "+str(regexFinder.num_htags))
		self.num_htags.grid(column=0,row=y)

		self.num_jwtags = Tkinter.Label(self,text="JWTags: "+str(regexFinder.num_jwtags))
		self.num_jwtags.grid(column=1,row=y)

		self.num_excesstags = Tkinter.Label(self,text="ExcessTags: "+str(regexFinder.num_excesstags))
		self.num_excesstags.grid(column=2,row=y)

		self.num_URLtags = Tkinter.Label(self,text="URLTags: "+str(regexFinder.num_urltags))
		self.num_URLtags.grid(column=3,row=y)

if __name__ == "__main__":

	app = mainApp(None)
	app.title('Fixing-Twitter by Alex Burley')
	app.mainloop()

#print "\n"
#print regexFinder.num_htags
#print regexFinder.num_atags
#print regexFinder.num_urltags
#print regexFinder.num_jwtags
#print regexFinder.num_excesstags