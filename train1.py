#!/usr/bin/env python

import random

words = [	('bonjour', 'goddag'),
			('avoir', 'att ha'),
			('etre', 'att vara'),
			('coucher', 'att ligga'),
			('voir', 'att se'),
			('la voiture', 'bilen')]

random.seed()

i1 = random.randint(0,len(words)-1)

i2 = [];
for j in range(1,6):
	i2.append(random.randint(0,len(words)-1))

j = random.randint(0,5)
i2[j] = i1

print words[i1][0]


for j in range(0,6):
	print "(", j, ") ", words[i2[j]][1]

print("Done")

