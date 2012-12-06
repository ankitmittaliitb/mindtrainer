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

APP_NAME = 'memtrainer'

class TrainingFrame(wx.Frame):
	def __init__(self, parent, ID, title, pos=wx.DefaultPosition,
				size = wx.DefaultSize, style = wx.DEFAULT_FRAME_STYLE):

		wx.Frame.__init__(self, parent, ID, title, pos, size, style)

		self.trainerpanel = TrainerPanel(self, wx.ID_ANY)

		self.multiplechoice = MultipleChoicePanel(self, wx.ID_ANY)
		self.multiplechoice.Hide()
		self.spelling = SpellingPanel(self, wx.ID_ANY)
		self.spelling.Hide()

		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.trainerpanel, 1, wx.EXPAND)
		self.sizer.Add(self.multiplechoice, 1, wx.EXPAND)
		self.sizer.Add(self.spelling, 1, wx.EXPAND)
		self.SetSizer(self.sizer)

		# Menu
		filemenu = wx.Menu()

		openmenuitem = filemenu.Append(wx.ID_OPEN, "&Open", "Open word list")
		exitmenuitem = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate program")

		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File")

		self.SetMenuBar(menuBar)

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

	def LoadWordList(self, path):
		self.words = WordList(path)
		return self.words

	def Stop(self):
		self.trainerpanel.Show()
		self.multiplechoice.Hide()
		self.spelling.Hide()
		self.Layout()

	def StartMultipleChoice(self, trainlist):
		self.words.SetTrainList(trainlist)
		self.multiplechoice.SetWordList(self.words)
		self.multiplechoice.PickNewWords()

		self.trainerpanel.Hide()
		self.multiplechoice.Show()
		self.Layout()

	def StartSpelling(self, trainlist):
		self.words.SetTrainList(trainlist)
		self.spelling.SetWordList(self.words)
		self.spelling.PickNewWord()

		self.trainerpanel.Hide()
		self.spelling.Show()
		self.Layout()

	def OnClose(self, event):
		self.Close(True)

	def OnCloseWindow(self, event):
		self.Destroy()

class TrainerPanel(wx.Panel):
	def __init__(self, parent, ID):
		wx.Panel.__init__(self, parent, ID)

		self.text_word = wx.StaticText(self, label="Choose a word list", pos=(40,30))
		self.wordlistlistbox = wx.ListBox(self, pos=(40,70), size=(200,200), style=wx.LB_SINGLE)
		button_add = wx.Button(self, label="Add word list", size=(150, 40), pos=(250, 70))
		button_rm = wx.Button(self, label="Remove word list", size=(150, 40), pos=(250, 130))
		button_mult_choice = wx.Button(self, label="Multiple choice", size=(150, 40), pos=(250, 190))
		button_spelling = wx.Button(self, label="Spelling", size=(150, 40), pos=(250, 250))

		self.cfg = wx.Config(APP_NAME)

		lists = self.cfg.Read('wordlists')
		if(lists == ''):
			self.wordlists = []
		else:
			self.wordlists = lists.split('\t')
		self.UpdateListBox()

		self.Bind(wx.EVT_BUTTON, self.OnAddWordList, button_add)
		self.Bind(wx.EVT_BUTTON, self.OnRemoveWordList, button_rm)
		self.Bind(wx.EVT_BUTTON, self.OnMultipleChoice, button_mult_choice)
		self.Bind(wx.EVT_BUTTON, self.OnSpelling, button_spelling)
		self.Bind(wx.EVT_LISTBOX, self.OnWordListListBox, self.wordlistlistbox)

	def UpdateListBox(self):
		self.wordlistlistbox.Clear()
		
		for wl in self.wordlists:
			self.wordlistlistbox.Append(os.path.basename(wl))

	def OnAddWordList(self, event):
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

		lists = self.cfg.Read('wordlists')
		if(lists != ''):
			self.cfg.Write('wordlists', lists + '\t' + path)
		else:
			self.cfg.Write('wordlists', path)
		self.wordlists.append(path)
		self.UpdateListBox()
		

	def OnRemoveWordList(self, event):
		listi = self.wordlistlistbox.GetSelection()

		if(listi == wx.NOT_FOUND):
			return

		self.wordlists.pop(listi)
		self.UpdateListBox()
		
	def OnWordListListBox(self, event):
		# Load wordlist update choices
		listi = self.wordlistlistbox.GetSelection()
		wordlist = self.wordlists[listi]
		self.wordlist = self.GetParent().LoadWordList(wordlist)

	def OnMultipleChoice(self, event):
		trainlist = []
		for i in range(0, self.wordlist.Length()):
			trainlist += [[i,1]]

		self.GetParent().StartMultipleChoice(trainlist)

	def OnSpelling(self, event):
		trainlist = []
		for i in range(0, self.wordlist.Length()):
			trainlist += [[i,1]]

		self.GetParent().StartSpelling(trainlist)


class SpellingPanel(wx.Panel):
	def __init__(self, parent, ID):
		wx.Panel.__init__(self, parent, ID)

		self.text_word = wx.StaticText(self, label="word", pos=(40,30))
		self.correct_text_word = wx.StaticText(self, label="", pos=(40,60))
		stopbutton = wx.Button(self, label="Stop", size=(100,30), pos=(280, 20))
		self.spelling_box = wx.TextCtrl(self, wx.ID_ANY, size=(200, 30), pos=(30,100))

		self.Bind(wx.EVT_BUTTON, self.OnStop, stopbutton)
		self.Bind(wx.EVT_TEXT, self.OnText, self.spelling_box)
		self.spelling_box.Bind(wx.EVT_CHAR, self.OnChar)

	def SetWordList(self, word_list):
		self.word_list = word_list

	def PickNewWord(self):
		self.checked = False
		new_word = self.word_list.NewSpellWord()

		if(new_word == None):
			self.GetParent().Stop()
			return

		self.correct_text_word.SetLabel('')
		self.spelling_box.SetValue('')
		self.spelling_box.SetBackgroundColour("WHITE")
		self.text_word.SetLabel(new_word[1])
		self.word_to_spell = new_word[0].decode('utf8')

	def OnStop(self, event):
		self.GetParent().Stop()

	def OnText(self, event):
		if(self.checked == True):
			text = self.spelling_box.GetValue()
			if(not isinstance(text, unicode)):
				print "Error, input is not unicode"
			if(not isinstance(self.word_to_spell, unicode)):
				print "Error, word_to_spell is not unicode (%s is object %s)" % (self.word_to_spell, type(self.word_to_spell))
			
			if(self.word_to_spell.startswith(text)):
				self.spelling_box.SetBackgroundColour("WHITE")
				if(self.word_to_spell == text):
					self.spelling_box.SetBackgroundColour("GREEN")
			else:
				self.spelling_box.SetBackgroundColour("RED")

	def OnChar(self, event):
		if(event.GetKeyCode() == 13):
			if(not self.checked):
				self.checked = True
				if(self.spelling_box.GetValue() == self.word_to_spell):
					self.spelling_box.SetBackgroundColour("GREEN")
				else:
					self.spelling_box.SetValue('')
					self.spelling_box.SetBackgroundColour("RED")
					self.correct_text_word.SetLabel(self.word_to_spell)
			else:
				text = self.spelling_box.GetValue()
				if(text == u'' or text == self.word_to_spell):
					self.PickNewWord()
		event.Skip()

class MultipleChoicePanel(wx.Panel):
	def __init__(self, parent, ID):
		wx.Panel.__init__(self, parent, ID)

		self.text_word = wx.StaticText(self, label="word", pos=(40,30))
		stopbutton = wx.Button(self, label="Stop", size=(100,30), pos=(280, 20))
		self.Bind(wx.EVT_BUTTON, self.OnStop, stopbutton)

		font = self.text_word.GetFont()
		font.SetPointSize(14)
		self.text_word.SetFont(font)

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

		if(newchoices == None):
			self.GetParent().Stop()
			return

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

	def OnStop(self, event):
		self.GetParent().Stop()

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
			word1 = row[0]
			word2 = row[1]
			word1 = word1.replace("&#39;", "'")
			word2 = word2.replace("&#39;", "'")
			self.words.append((row[0], row[1]))

		return True

	def SetTrainList(self, trainlist):
		# Trainlist is a list of [wordindex, ntimestotrain]
		self.trainlist = trainlist

	def NewWord(self):
		nwords = len(self.trainlist) - self.trainlist.count(0)
		if(nwords == 0):
			return None

		index = random.randint(0, nwords-1)
		wordindex = self.trainlist[index][0]

		self.trainlist[index][1] -= 1
		if(self.trainlist[index][1] == 0):
			self.trainlist.pop(index)
		
		return wordindex

	def NewSpellWord(self):
		wordindex = self.NewWord()
		if(wordindex == None):
			return None

		return (self.words[wordindex][0], self.words[wordindex][1])

	def NewMultipleChoiceWords(self, num_choices):

		wordindex = self.NewWord()
		if(wordindex == None):
			return None

		indexarray = range(len(self.words))
		indexarray.pop(wordindex)
		wordchoices = random.sample(indexarray, num_choices-1)

		i = random.randint(0,num_choices-1) # TODO: max to length of choices
		wordchoices.insert(i, wordindex)

		newwords = []
		for wi in wordchoices:
			newwords.append(self.words[wi][1])
		
		return (newwords, i, self.words[wordindex][0])

	def Length(self):
		return len(self.words)

if __name__ == "__main__":

	app = wx.App()

	win = TrainingFrame(None, wx.ID_ANY, "Title", size=(550, 320))
	win.Show()

	app.MainLoop()

