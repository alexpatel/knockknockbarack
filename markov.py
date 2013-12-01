from config import connect
from random import randint	
words = connect()

## generate a markov
def generate(start_word=None):
	try:
		if start_word:
			# pick a random beginning with start_word as first word
			word = words.find({'1': start_word})[randint(0, words.find({'1': start_word}).count() - 1)]
		else:
			# get random sentence beginning
			word = words.find({'start': True})[randint(0, words.find({'start': True}).count() - 1)]
	except ValueError:
		# try again
		if start_word: generate(start_word)
		else: generate()

	phrase = word['1']+' '

	# build word until natural sentence end is reached
	while not word['end']:
		try:
			count = words.find({'1': word['2'],  '2': word['3']}).count()
			if count is not 0:
				word = words.find({'1': word['2'], '2': word['3']})[randint(0, words.find({'1': word['2'],  '2': word['3']}).count() - 1)]
			else: raise KeyError # pretty janky
		except KeyError:
			# word at end of file - no '2'/'3' string created
			try:
				count =  words.find({'1': word['2']}).count()
				if count is not 0:
					word = words.find({'1': word['2']})[randint(0, count - 1)]
				else: raise KeyError
			except KeyError:
				# last resort = random word
				word = words.find()[randint(0, words.find().count() - 1)]

		# add word to chain
		phrase += word['1']+' '

	return phrase

## generate a yo mama joke
def your_mama():
	# pick a random adjective
	# remove possible residual period from end
	adj = words.find({'pos': 'JJ'})[randint(0, words.find({'pos': 'JJ'}).count() - 1)]['1'].strip('.')
	
	# 'own' is bad...
	while adj is 'own':
		adj = words.find({'pos': 'JJ'})[randint(0, words.find({'pos': 'JJ'}).count() - 1)]['1'].strip('.')

	# generate a phrase starting with a 'that' that proceeds an adjective
	docs = words.find({'pos': 'JJ', '2':'that'})
	start = docs[randint(0, docs.count() - 1)]['3']
	phrase = generate(start_word=start)

	print u"Your mama is so {0} that {1}".format(adj, phrase)

# generate knock_knock joke
def knock_knock():	
	# pick a random knock-knock lead
	lead = words.find({'pos': 'NN'})[randint(0, words.find({'pos': 'NN'}).count() - 1)]['1'].strip('.')

	# generate phrase from lead
	phrase = generate(start_word=lead) 

	# format for knock-knock format
 	lead = lead.capitalize().strip(',').strip('.')
 	phrase = phrase.capitalize()

	# \n = \u000A. i can't figure out this utf-8 garbage with mongo
	print u"Knock Knock... \u000AWho's There? \u000A{0}. \u000A{0} who? \u000A{1} \u000A".format(lead, phrase)

# why did the chicken cross the road?
def chicken()

