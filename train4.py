#!/usr/bin/env python
# coding: utf8

import sys
import random
import xmllib

#words = [	('bonjour', 'goddag'),
#			('avoir', 'att ha'),
#			('etre', 'att vara'),
#			('coucher', 'att ligga'),
#			('voir', 'att se'),
#			('la voiture', 'bilen')]

words = [	('remonter', 'att stiga igen'),
			('pis', 'värre'),
			('nous tombons', 'vi faller'),
			('jetez', 'att kasta'),
			('lest', 'barlast'),
			('vidé', 'tömd'),
			('relèver', 'att höja, att resa'),
			('entendre', 'att höra'),
			('clapotement', 'skvalpande'),
			('vagues', ''),
			('la nacelle', ''),
			('doit', ''),
			('puissante', ''),
			('déchira', ''),
			('retentirent', ''),
			('pèse', ''),
			('telles', ''),
			('éclataient', ''),
			('vaste', ''),
			('doute', ''),
			('coup de vent', ''),
			('déchaîna', ''),
			('équinoxe', ''),
			('lequel, laquelle?', ''),
			('fut', ''),
			('le ouragan', ''),
			('intermittence', ''),
			('ravages', ''),
			('furent', ''),
			('obliquement', ''),
			('parallèle', ''),
			("jusqu'au", ''),
			('renversées', ''),
			('déracinées', ''),
			('rivages', ''),
			('dévastés', ''),
			('précipitaient', ''),
			('mascarets', ''),
			('jetés', ''),
			('relevés', ''),
			('chiffrèrent', ''),
			('nivelés', ''),
			('broyaient', ''),
			('plusieurs', ''),
			('milliers', ''),
			('écrasées', ''),
			('englouties', ''),
			('tels', ''),
			('furent', ''),
			('témoignages', ''),
			('fureur', ''),
			('dépassait', ''),
			('désastres', ''),
			('ceux', ''),
			('ravagèrent', ''),
			('or', ''),
			('tant', ''),
			('saisissant', ''),
			('bouleversés', ''),
			('sommet', ''),
			('pris', ''),
			('giratoire', ''),
			('la colonne', ''),
			('parcourait', ''),
			('tournant', ''),
			('eût', ''),
			('saisi', ''),
			('au-dessous', ''),
			('inférieur', ''),
			('oscillait', ''),
			('contenait', ''),
			('peine', ''),
			('épaisses', ''),
			('vapeurs', ''),
			('mêlées', ''),
			('traînaient', '')
			]

def init():
	random.seed()

def load_word_list(filename):
	pass

def run_word(num_choises):

	# Word to train
	wordindex = random.randint(0,len(words)-1)

	indexarray = range(len(words))
	indexarray.pop(wordindex)
	wordchoises = random.sample(indexarray, num_choises-1)

	i = random.randint(0,num_choises) # TODO: max to legth of choises
	wordchoises.insert(i, wordindex)

	print "\n", words[wordindex][0]

	i = 1
	for wi in wordchoises:
		print "(", i, ") ", words[wi][1]
		i += 1

	answer = sys.stdin.readline()
	answer = answer[0:-1]

	if(answer.isdigit() == False):
		return False

	answer = int(answer)

	if(wordchoises[answer-1] == wordindex):
		print "Correct"
	else:
		print "Wrong (", words[wordindex][1], ")"

	sys.stdin.readline()

	return True

if __name__ == "__main__":
	print "run"
	init()
	while(run_word(5)):
		pass








