#!/usr/bin/env python

#
# Login here:
# http://www.forvo.com/login/ (post: login, password)
#
# "Login incorrect." if login is bad
#
# Open the page http://www.forvo.com/word/russian_word_here/
#
# "Oops! There is no word." is written if the word doesn't exist
#
# mp3-links are found in the following form:
# /download/mp3/%s/ru/%d
# the first one has the highest ranking
#
# import urllib
#
# t = urllib.urlopen("http://google.com")
# text = t.read()
#
# urllib.urlretrieve ("http://www.example.com/songs/mp3.mp3", "mp3.mp3")
#

import os
import sys
import getpass
import urllib
import urllib2
import cookielib
import csv
import re

if(len(sys.argv) < 2):
	print 'Usage: %s <word-file.csv>' % sys.argv[0]
	exit()

csvfile = open(sys.argv[1], 'rb')
csvobject = csv.reader(csvfile, delimiter='\t', quotechar='"')

user = raw_input('User: ')
password = getpass.getpass()

cookies = cookielib.LWPCookieJar()
handlers = [
	urllib2.HTTPHandler(),
	urllib2.HTTPSHandler(),
	urllib2.HTTPCookieProcessor(cookies)
	]

url_opener = urllib2.build_opener(*handlers)

page = url_opener.open('http://www.forvo.com/login/', urllib.urlencode({'login':user, 'password':password}))

if(page.read().find('Login incorrect.') != -1):
	print "Error logging in"
	exit()

# Needs to check if it exists already
#os.mkdir('audio/')

num_downloaded = 0
num_failed = 0

for row in csvobject:
	word = row[0]
	word = word.replace("&#39;", "'")
	word = word.replace("!", "")

	if(os.path.isfile('audio/' + word + '.mp3')):
		continue
	
	page = url_opener.open('http://www.forvo.com/word/%s/' % urllib.quote(word))
	text = page.read()

	if(text.find('Oops! There is no word.') != -1):
		print "Word not found: " + word
		num_failed += 1
		continue

	regex = re.search('download/mp3/[%0-9A-Za-z_-]*/[a-z]*/[0-9]*', text)
	path = regex.group(0)

	print 'Fetching word: ' + word
	data = url_opener.open('http://www.forvo.com/' + path)
	f = open('audio/' + word + '.mp3', 'wb')
	f.write(data.read())
	f.close()

	num_downloaded += 1

print "Downloaded %d files" % num_downloaded
print "Failed to download %d files" % num_failed

