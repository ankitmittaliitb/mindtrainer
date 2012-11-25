#!/usr/bin/env python
# coding: utf8

# Skapa panels för skriva ord/välja ord?
# Överst, välja håll för språk samt multiple choise/stavning?

import sys
import os
import wx
import random
import xml.dom.minidom

class TrainingFrame(wx.Frame):
	def __init__(self, parent, ID, title, pos=wx.DefaultPosition,
				size = wx.DefaultSize, style = wx.DEFAULT_FRAME_STYLE):

		wx.Frame.__init__(self, parent, ID, title, pos, size, style)
		panel = wx.Panel(self, -1)

		# Menu
		filemenu = wx.Menu()

		openmenuitem = filemenu.Append(wx.ID_OPEN, "&Open", "Open word list")
		exitmenuitem = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate program")

		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File")

		self.SetMenuBar(menuBar)

		# Text and buttons
		
		self.text_word = wx.StaticText(panel, label="Choose a word list", pos=(40,30))

		self.buttonchoices = []
		self.buttonchoices.append(wx.Button(panel, label="choise1", size=(250,40), pos=(20,70)))
		self.buttonchoices.append(wx.Button(panel, label="choise2", size=(250,40), pos=(20,120)))
		self.buttonchoices.append(wx.Button(panel, label="choise3", size=(250,40), pos=(20,170)))
		self.buttonchoices.append(wx.Button(panel, label="choise4", size=(250,40), pos=(20,220)))
		self.buttonchoices.append(wx.Button(panel, label="choise5", size=(250,40), pos=(280,70)))
		self.buttonchoices.append(wx.Button(panel, label="choise6", size=(250,40), pos=(280,120)))
		self.buttonchoices.append(wx.Button(panel, label="choise7", size=(250,40), pos=(280,170)))
		self.buttonchoices.append(wx.Button(panel, label="choise8", size=(250,40), pos=(280,220)))

		self.Bind(wx.EVT_BUTTON, self.OnChoiceButton0, self.buttonchoices[0])
		self.Bind(wx.EVT_BUTTON, self.OnChoiceButton1, self.buttonchoices[1])
		self.Bind(wx.EVT_BUTTON, self.OnChoiceButton2, self.buttonchoices[2])
		self.Bind(wx.EVT_BUTTON, self.OnChoiceButton3, self.buttonchoices[3])
		self.Bind(wx.EVT_BUTTON, self.OnChoiceButton4, self.buttonchoices[4])
		self.Bind(wx.EVT_BUTTON, self.OnChoiceButton5, self.buttonchoices[5])
		self.Bind(wx.EVT_BUTTON, self.OnChoiceButton6, self.buttonchoices[6])
		self.Bind(wx.EVT_BUTTON, self.OnChoiceButton7, self.buttonchoices[7])
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
		self.Bind(wx.EVT_MENU, self.OnClose, exitmenuitem)
		self.Bind(wx.EVT_MENU, self.OnOpen, openmenuitem)

		self.words = None


	def SetWord(self, word):
		self.text_word.SetLabel(word)

	def SetChoices(self, choices, answer):
		self.answer = answer
		self.answered = False
		for i in range(0,8):
			self.buttonchoices[i].SetLabel(choices[i])
			self.buttonchoices[i].SetBackgroundColour("WHITE")
			self.buttonchoices[i].SetForegroundColour("BLACK")

	def OnOpen(self, event):
		wildcard = 	"XML word list (*.xhtml)|*.xhtml|" \
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
		self.words.NewWords(self, 8)
			

	def OnClose(self, event):
		self.Close(True)

	def OnCloseWindow(self, event):
		self.Destroy()

	def ChoiceButton(self, number):
		if(self.words == None):
			return

		if(self.answered):
			if(number == self.answer):
				self.words.NewWords(self, 8)
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

		self.LoadXML(path)

	def LoadXML(self, path):
		doc = xml.dom.minidom.parse(path)
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

	def NewWords(self, frame, num_choices):

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

		
		frame.SetWord(self.words[wordindex][0])
		frame.SetChoices(newwords, i)

if __name__ == "__main__":

	app = wx.App()

	win = TrainingFrame(None, wx.ID_ANY, "Title", size=(550, 320))
	win.Show(True)

	app.MainLoop()

