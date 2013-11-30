import os
from pymongo import MongoClient
from nltk import word_tokenize #, pos_tag

## build db collection with markov Word objects from txt files in speeches folder
def build():
	# path to folder with speeches
	path = "./speeches/"

	# list of files in path
	# w/out D.S_store fucking osx.
	files = [file for file in os.listdir(path) if file is not ".DS_Store"]

	# connect to db, collection
	db = connect()
	words = db.words
	words.remove()

	# insert contents of each file in path in form of Word objects into db.collection
	for file in files:
		try:
			f = open(path + file, 'r')
			try:
				text = f.read()
				#part_speech = pos_tag(word_tokenize(text))
				#print part_speech
				text = [clean(word) for word in text.split() if clean(word) is not '']
				insert(text, words)
			finally:
				f.close()
		except IOError:
			pass

## remove punctuation from before/after word
def clean(word):
	punct = [' ', ',', '.', '?', '!', '"', ':', ';', '-']
	for char in punct:
		word = word.strip(char)
	return word

## insert words in text into collect as markov Word objects
def insert(text, collection):
	length = len(text)
	for index in range(length):
		# mongo utf encoding was trying to read \x00. bad juju
		if text[index] is not None and text[index].find('\x00') is -1:
			Word = {
				'1': text[index]
			}
			if index + 1 < length and text[index + 1].find('\x00') is -1:
				Word['2'] = text[index + 1]
	
			if index + 2 < length and text[index + 2].find('\x00') is -1:
				Word['3'] = text[index + 2]
			
			collection.insert(Word)
			print Word

## connect to mongo database
def connect():
	host = 'localhost'
	port = 27017
	db_name = 'kkb'

	client = MongoClient(host, port)
	return client[db_name]

build()