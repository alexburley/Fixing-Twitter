# -*- coding: utf-8 -*-

import sys
import re
import RegexFinder as reg
import unittest
import spellchecker as sc
import enchant
import Tkinter
from tkFileDialog import askopenfilename

class mainApp(Tkinter.Tk):

	#top = Tkinter.Tk()
	# Code to add widgets will go here...
	#top.mainloop()

	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.filePath = ""
		self.initialize()

	def initialize(self):
		self.grid()
		button = Tkinter.Button(self,text=u"Run Code", command = self.onButtonClick)
		button.grid(column=0,row=0)

		fileOpen = Tkinter.Button(self,text="File",command=self.onFileClick)
		fileOpen.grid(column=1,row=0)

		uploadedFile = Tkinter.Label(self,text="No File Uploaded")
		uploadedFile.grid(column=2,row=0)
		
		jwbox = Tkinter.Checkbutton(self, text="JW Tag")
		jwbox.grid(column=0,row=1)

		excessbox = Tkinter.Checkbutton(self, text="Excess Tag")
		excessbox.grid(column=1,row=1)

		hbox = Tkinter.Checkbutton(self, text="Hash Tag")
		hbox.grid(column=2,row=1)

		timebox = Tkinter.Checkbutton(self, text="Time Tag")
		timebox.grid(column=3,row=1)

		self.grid_columnconfigure(0,weight=1)

		#resizingallowed(x,y)
		#self.resizable(True,False)

	def onButtonClick(self):
		self.mainCode()

	def onFileClick(self):
		uploadedFilePath = askopenfilename()
		uploadedFile = Tkinter.Label(self,text=uploadedFilePath)
		uploadedFile.grid(column=2,row=0)



	def mainCode(self):

		infile = open(sys.argv[1],'r')
		regexFinder = reg.RegexFinder()


		print "-------------------------------------------------------------"
		for line in infile:
			if line.strip():
				tokens = regexFinder.subLine(line)
				#testTag = "excesstag"
				testTag = "jwtag"
				if (regexFinder.numTags(testTag)):
					print line
					new_line=""
					for token in tokens:
						if new_line == "":
							new_line = new_line+token
						else:
							new_line = new_line+" "+token
					print new_line
					print "-------------------------------------------------------------"

"""
	CODE EXPLANATION

	Radio buttons for what regex tags to look for.

"""

#outfile = open(sys.argv[2],'w')
#MAIN INITALIZER CODE


if __name__ == "__main__":

	app = mainApp(None)
	app.title('Fixing-Twitter')
	app.mainloop()

#print "\n"
#print regexFinder.num_htags
#print regexFinder.num_atags
#print regexFinder.num_urltags
#print regexFinder.num_jwtags
#print regexFinder.num_excesstags