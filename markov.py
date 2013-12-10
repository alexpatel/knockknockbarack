from conf import connect
from random import randint	
from nltk import word_tokenize, pos_tag
from threading import Thread
import build

markov_length = 125

# connect to db, get relevant collections
words = connect('words')
jokes = connect('jokes')

## generate a markov
def generate(start_word=None):
	word = '-'
	try:
		if start_word:
			# pick a random beginning with start_word as first word
			while word is '-':
				curs = words.find({'1': start_word})
				word = curs[randint(0, curs.count() - 1)]
		else:
			# get random sentence beginning
			while word is '-':
				curs = words.find({'start': True})
				word = curs[randint(0, curs.count() - 1)]
	except ValueError:
		# try again
		if start_word: generate(start_word)
		else: generate()

	phrase = word['1']+' '

	# build word until natural sentence end is reached
	while not word['end']:
		try:
			curs = words.find({'1': word['2'],  '2': word['3']})
			count = curs.count()
			#count = words.find({'1': word['2']}).count()
			if count is not 0:
				word = curs[randint(0, count - 1)]
				#word = words.find({'1': word['2']})[randint(0, words.find({'1': word['2']}).count() - 1)]
			else: raise KeyError # pretty janky
		except KeyError:
			# word at end of file - no '2'/'3' string created
			try:
				curs = words.find({'1': word['2']})
				count =  curs.count()
				if count is not 0:
					word = words.find({'1': word['2']})[randint(0, count - 1)]
				else: raise KeyError
			except KeyError:
				# last resort = random word
				word = words.find()[randint(0, words.find().count() - 1)]

		# let's make sure thesentence is getting too long.
		# (only as long as we don't end on a non-sentence ending word)
		bad_ending = pos_tag(word_tokenize(word['1']))[0][1] in ['RB', 'CC', 'IN', 'JJ'] \
			or word['1'] in ['U.S.', 'that', 'the', 'a']

		if len(phrase) > markov_length and phrase[len(phrase) - 1] is not '.' and not bad_ending:
			return phrase + word['1'].strip('/') + '.'

		# add word to chain
		phrase += word['1']+' '

	return phrase

## generate a yo mama joke
def yo_mama():
	# pick a random adjective
	# remove possible residual period from end
	adj = words.find({'pos': 'JJ'})[randint(0, words.find({'pos': 'JJ'}).count() - 1)]['1'].strip('.')
	
	# these are just one's that nltk doesn't pick up on. no idea why.
	while adj in ['own', "don't", "wasn't", "didn't", "won't"]:
		poss = words.find({'pos': 'JJ'})
		adj = poss[randint(0, poss.count() - 1)]['1'].strip('.')

	# generate a phrase starting with a 'that' that proceeds an adjective
	docs = words.find({'pos': 'JJ', '2':'that'})
	start = docs[randint(0, docs.count() - 1)]['3']
	phrase = generate(start)

	return u"Your mama is so {0} that {1}".format(adj, phrase)

# generate knock_knock joke
def knock_knock():	
	# pick a random knock-knock lead
	lead = words.find({'pos': 'NN'})[randint(0, words.find({'pos': 'NN'}).count() - 1)]['1'].strip('.')

	# generate phrase from lead
	phrase = generate(lead) 

	# format for knock-knock format
 	lead = lead.capitalize().strip(',').strip('.')
 	phrase = phrase.capitalize()

	return u"Knock Knock... <br><em>Who's There?</em><br>{0}. <br><em>{0} who?</em><br>{1} \n".format(lead, phrase)

## why did the chicken cross the road?
def chicken():
	start = words.find({'1': 'to'})[randint(0, words.find({'1': 'to'}).count() - 1)]['2'].strip('.')
	# we want to find 'to' --> verb
	while not pos_tag(word_tokenize(start))[0][1].startswith('V') or 'ing' in start:
		curs = words.find({'1': 'to'})
		start = curs[randint(0, curs.count() - 1)]['2'].strip('.')

	phrase = generate(start)

	return u"<em>Why did the chicken cross the road?</em><br>To {0}".format(phrase)

## generate a joke
def joke():
	if jokes.count() is 0:
		# just build user a new joke
		# asynchronous queue insert isn't working 
		# let's just put two more jokes in and let the user deal with the lag
		# the problem is, because we're getting jokes w/ ajax, they won't know it's loading 
		# 'patience, young grasshopper'	
		async()
		async()
		return rand_joke()

	# get first joke from jokes collection
	joke = jokes.find_one()

	# asyncronously do the stuff that we don't need to accomplish to give the user a joke
	# aka put a joke in the jokes queue
	Thread(target=async).start()
	
	# remove used joke
	jokes.remove(joke)

	return joke['joke']

## start a new thread to remove returned joke from the jokes collection / make a new one
def async():	
	# mongo insert
	new_joke = { 'joke': rand_joke()}
	jokes.insert(new_joke)

## generate a random joke from list of types
def rand_joke():\
		# generate random type of joke and insert into coll
	types = ['yo mama', 'knock knock', 'chicken']
	ind = randint(0, len(types) - 1)

	if ind is 0:
		joke = yo_mama()
	elif ind is 1:
		joke = knock_knock()
	else:
		joke = chicken()

	return joke