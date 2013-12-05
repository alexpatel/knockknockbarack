import os
from nltk import word_tokenize, pos_tag # natural language toolkit - for part of speech analysis
from conf import connect
import markov

## build db collection with markov Word objects from txt files in speeches folder
def build():
	# path to folder with speeches
	path = "./speeches/"

	# list of files in path
	# w/out D.S_store. darn osx.
	files = [file for file in os.listdir(path) if file is not ".DS_Store"]

	# connect to db, collection
	words = connect('words')

	# wipe previous documents
	words.remove()

	# insert contents of each file in path in form of Word objects into db.collection
	for file in files:
		try:
			f = open(path + file, 'r')
			try:
				text = f.read()
				text = [clean(word) for word in text.split() if clean(word) is not '']
				insert(text, words)
			finally:
				f.close()
		except IOError:
			pass

## remove punctuation from before/after word
def clean(word):
	punct = [' ','/', '?', '!', '"', ':', ';', '-']
	for char in punct:
		word = word.strip(char)
	return word

## checks if word is at the end of the sentence
def sent_end(word):
	return True if word.find('.', len(word) - 1) is not -1 and word is not 'U.S.' else False

## insert words in text into collect as markov Word objects
def insert(text, collection):
	length = len(text)
	for index in range(length):
		# mongo utf encoding was trying to read \x00. bad juju
		if text[index] is not None and text[index].find('\x00') is -1:
			Word = {
				'1': text[index]
			}
			# get part of speech
			# http://nltk.org/book/ch05.html
			Word['pos'] = pos_tag(word_tokenize(text[index]))[0][1]
			# end of sentence
			Word['end'] = sent_end(text[index])
			# beginning of sentence
			Word['start'] = True if sent_end(text[index - 1]) else False
			# proceeding word
			if index + 1 < length and text[index + 1].find('\x00') is -1:
				Word['2'] = text[index + 1]
			# words 2 after
			if index + 2 < length and text[index + 2].find('\x00') is -1:
				Word['3'] = text[index + 2]
			collection.insert(Word)
			print Word

## for when I do something stupid and want to quickly rebuild the cached jokes
def rebuild_jokes():
	jokes = connect('jokes')
	jokes.remove()

	# insert 10 new jokes
	for i in range(10):
		new_joke = { 'joke': markov.rand_joke()}
		jokes.insert(new_joke)

