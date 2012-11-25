#!/usr/bin/env python

import sys
import random

words = [	('bonjour', 'goddag'),
			('avoir', 'att ha'),
			('etre', 'att vara'),
			('coucher', 'att ligga'),
			('voir', 'att se'),
			('la voiture', 'bilen')]

num_choises = 5

random.seed()

# Word to train
wordindex = random.randint(0,len(words)-1)

indexarray = range(len(words))
indexarray.pop(wordindex)
wordchoises = random.sample(indexarray, num_choises-1)

i = random.randint(0,num_choises)
wordchoises.insert(i, wordindex)

print "\n", words[wordindex][0]

i = 1
for wi in wordchoises:
	print "(", i, ") ", words[wi][1]
	i += 1

answer = sys.stdin.readline()
answer = int(answer[0:-1])

if(wordchoises[answer-1] == wordindex):
	print "Correct"
else:
		print "Wrong (", words[wordindex][1], ")"



