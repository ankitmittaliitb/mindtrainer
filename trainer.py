#!/usr/bin/env python
# coding: utf8

# Skapa panels för skriva ord/välja ord?
# Överst, välja håll för språk samt multiple choise/stavning?

import sys
import os
import wx
import random
import xml.dom.minidom
import csv

class TrainingFrame(wx.Frame):
	def __init__(self, parent, ID, title, pos=wx.DefaultPosition,
				size = wx.DefaultSize, style = wx.DEFAULT_FRAME_STYLE):

		wx.Frame.__init__(self, parent, ID, title, pos, size, style)
		self.main_panel = wx.Panel(self, wx.ID_ANY)

		self.multiplechoice = MultipleChoicePanel(self, wx.ID_ANY)
		self.multiplechoice.Hide()

		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.main_panel, 1, wx.EXPAND)
		self.sizer.Add(self.multiplechoice, 1, wx.EXPAND)
		self.SetSizer(self.sizer)

		# Menu
		filemenu = wx.Menu()

		openmenuitem = filemenu.Append(wx.ID_OPEN, "&Open", "Open word list")
		exitmenuitem = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate program")

		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File")

		self.SetMenuBar(menuBar)

		# Text and buttons
		
		self.text_word = wx.StaticText(self.main_panel, label="Choose a word list", pos=(40,30))

		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
		self.Bind(wx.EVT_MENU, self.OnClose, exitmenuitem)
		self.Bind(wx.EVT_MENU, self.OnOpen, openmenuitem)

		self.words = None

	def OnOpen(self, event):
		wildcard = 	"XML word list (*.xhtml)|*.xhtml|" \
					"CSV word list (*.csv)|*.csv|" \
					"All files (*.*)|*.*|"

		dlg = wx.FileDialog(
	            self, message="Choose a file",
	            defaultDir=os.getcwd(), 
	            defaultFile="",
	            wildcard=wildcard,
	            style=wx.OPEN | wx.CHANGE_DIR
	            )

		if(dlg.ShowModal() == wx.ID_OK):
			path = dlg.GetPath()
		else:
			print("Canceled open file")
			return

		self.words = WordList(path)

		# Only multiple choice for now
		self.multiplechoice.SetWordList(self.words)
		self.multiplechoice.PickNewWords()

		self.main_panel.Hide()
		self.multiplechoice.Show()
		self.Layout()

	def OnClose(self, event):
		self.Close(True)

	def OnCloseWindow(self, event):
		self.Destroy()

class MultipleChoicePanel(wx.Panel):
	def __init__(self, parent, ID):
		wx.Panel.__init__(self, parent, ID)

		self.text_word = wx.StaticText(self, label="word", pos=(40,30))

		self.buttonchoices = []
		self.buttonchoices.append(wx.Button(self, label="choice1", size=(250,40), pos=(20,70)))
		self.buttonchoices.append(wx.Button(self, label="choice2", size=(250,40), pos=(20,120)))
		self.buttonchoices.append(wx.Button(self, label="choice3", size=(250,40), pos=(20,170)))
		self.buttonchoices.append(wx.Button(self, label="choice4", size=(250,40), pos=(20,220)))
		self.buttonchoices.append(wx.Button(self, label="choice5", size=(250,40), pos=(280,70)))
		self.buttonchoices.append(wx.Button(self, label="choice6", size=(250,40), pos=(280,120)))
		self.buttonchoices.append(wx.Button(self, label="choice7", size=(250,40), pos=(280,170)))
		self.buttonchoices.append(wx.Button(self, label="choice8", size=(250,40), pos=(280,220)))

		self.Bind(wx.EVT_BUTTON, self.OnChoiceButton0, self.buttonchoices[0])
		self.Bind(wx.EVT_BUTTON, self.OnChoiceButton1, self.buttonchoices[1])
		self.Bind(wx.EVT_BUTTON, self.OnChoiceButton2, self.buttonchoices[2])
		self.Bind(wx.EVT_BUTTON, self.OnChoiceButton3, self.buttonchoices[3])
		self.Bind(wx.EVT_BUTTON, self.OnChoiceButton4, self.buttonchoices[4])
		self.Bind(wx.EVT_BUTTON, self.OnChoiceButton5, self.buttonchoices[5])
		self.Bind(wx.EVT_BUTTON, self.OnChoiceButton6, self.buttonchoices[6])
		self.Bind(wx.EVT_BUTTON, self.OnChoiceButton7, self.buttonchoices[7])

	def SetWordList(self, word_list):
		self.word_list = word_list

	def SetWord(self, word):
		self.text_word.SetLabel(word)

	def PickNewWords(self):
		newchoices = self.word_list.NewMultipleChoiceWords(8)
		self.SetChoices(newchoices[0], newchoices[1])
		self.SetWord(newchoices[2])
		self.answered = False

	def SetChoices(self, choices, answer):
		self.answer = answer
		self.answered = False
		for i in range(0,8):
			self.buttonchoices[i].SetLabel(choices[i])
			self.buttonchoices[i].SetBackgroundColour("WHITE")
			self.buttonchoices[i].SetForegroundColour("BLACK")

	def ChoiceButton(self, number):

		if(self.answered):
			if(number == self.answer):
				self.PickNewWords()
		else:
			self.answered = True
			for i in range(0,8):
				if(i != self.answer):
					self.buttonchoices[i].SetForegroundColour("GREY")
					if(i == number):
						self.buttonchoices[i].SetBackgroundColour("RED")
				else:
					self.buttonchoices[i].SetBackgroundColour("GREEN")

	def OnChoiceButton0(self, event):
		self.ChoiceButton(0)

	def OnChoiceButton1(self, event):
		self.ChoiceButton(1)

	def OnChoiceButton2(self, event):
		self.ChoiceButton(2)

	def OnChoiceButton3(self, event):
		self.ChoiceButton(3)

	def OnChoiceButton4(self, event):
		self.ChoiceButton(4)

	def OnChoiceButton5(self, event):
		self.ChoiceButton(5)

	def OnChoiceButton6(self, event):
		self.ChoiceButton(6)

	def OnChoiceButton7(self, event):
		self.ChoiceButton(7)

class WordList():
	def __init__(self, path):
		random.seed()

		# Try as XML first, then as CSV, otherwise (throw error?)
		if(self.LoadXML(path)):
			return
		if(self.LoadCSV(path)):
			return
		
		# Throw error?


	# Loads XML file, returns True on success, False if not valid XML file
	def LoadXML(self, path):
		# Check if it's valid XML

		try:
			doc = xml.dom.minidom.parse(path)
		except (IOError, xml.parsers.expat.ExpatError):
			return False


		tables = doc.getElementsByTagName("table")
		table = tables[0]
		# table.childNodes[i].childNodes[j].childNodes[0].childNodes[0].wholeText
		# i: 2,3,4...
		# j: 1 word , 2 explanation
	
		self.words = []
		for node in table.childNodes[2:]:
			word1 = node.childNodes[1].childNodes[0].childNodes[0].nodeValue
			word2 = node.childNodes[2].childNodes[0].childNodes[0].nodeValue
			word1 = word1.replace("&#39;", "'")
			word2 = word2.replace("&#39;", "'")
			self.words.append((word1, word2))

		return True

	def LoadCSV(self, path):
		# Is it possible to test if it's valid CSV?
		csvfile = open(path, 'rb')
		csvobject = csv.reader(csvfile, delimiter='\t', quotechar='"')

		self.words = []
		for row in csvobject:
			self.words.append((row[0], row[1]))

		return True

	def NewMultipleChoiceWords(self, num_choices):

		# Word to train
		wordindex = random.randint(0,len(self.words)-1)

		indexarray = range(len(self.words))
		indexarray.pop(wordindex)
		wordchoices = random.sample(indexarray, num_choices-1)

		i = random.randint(0,num_choices-1) # TODO: max to length of choices
		wordchoices.insert(i, wordindex)

		newwords = []
		for wi in wordchoices:
			newwords.append(self.words[wi][1])
		
		return (newwords, i, self.words[wordindex][0])

if __name__ == "__main__":

	app = wx.App()

	win = TrainingFrame(None, wx.ID_ANY, "Title", size=(550, 320))
	win.Show()

	app.MainLoop()

