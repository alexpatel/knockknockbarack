from conf import connect
from random import randint	
from nltk import word_tokenize, pos_tag
import thread

markov_length = 100

## generate a markov
def generate(start_word=None):
	words = connect('words')

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
			count = words.find({'1': word['2']}).count()
			#count = words.find({'1': word['2'],  '2': word['3']}).count()
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

		# let's make sure thesentence is getting too long.
		# (only as long as we don't end on a non-sentence ending word)
		bad_ending = pos_tag(word_tokenize(word['1']))[0][1] in ['RB', 'CC', 'IN', 'JJ'] or word['1'] is 'U.S.' or word['1'] is 'that'

		if len(phrase) > markov_length and phrase[len(phrase) - 1] is not '.' and not bad_ending:
			return phrase + word['1'] + '.'

		# add word to chain
		phrase += word['1']+' '

	return phrase

## generate a yo mama joke
def yo_mama():
	words = connect('words')

	# pick a random adjective
	# remove possible residual period from end
	adj = words.find({'pos': 'JJ'})[randint(0, words.find({'pos': 'JJ'}).count() - 1)]['1'].strip('.')
	
	# 'own' is bad...
	while adj is 'own':
		adj = words.find({'pos': 'JJ'})[randint(0, words.find({'pos': 'JJ'}).count() - 1)]['1'].strip('.')

	# generate a phrase starting with a 'that' that proceeds an adjective
	docs = words.find({'pos': 'JJ', '2':'that'})
	start = docs[randint(0, docs.count() - 1)]['3']
	phrase = generate(start)

	return u"Your mama is so {0} that {1}".format(adj, phrase)

# generate knock_knock joke
def knock_knock():	
	words = connect('words')

	# pick a random knock-knock lead
	lead = words.find({'pos': 'NN'})[randint(0, words.find({'pos': 'NN'}).count() - 1)]['1'].strip('.')

	# generate phrase from lead
	phrase = generate(lead) 

	# format for knock-knock format
 	lead = lead.capitalize().strip(',').strip('.')
 	phrase = phrase.capitalize()

	return u"Knock Knock... <br>Who's There? <br>{0}. <br>{0} who? <br>{1} <br>".format(lead, phrase)

## why did the chicken cross the road?
def chicken():
	words = connect('words')

	start = words.find({'1': 'to'})[randint(0, words.find({'1': 'to'}).count() - 1)]['2'].strip('.')
	# we want to find 'to' --> verb
	while not pos_tag(word_tokenize(start))[0][1].startswith('V') or 'ing' in start:
		start = words.find({'1': 'to'})[randint(0, words.find({'1': 'to'}).count() - 1)]['2'].strip('.')

	phrase = generate(start)

	return u"Why did the chicken cross the road?<br>To {0}".format(phrase)

## generate a random joke
def joke():
	jokes = connect('jokes')

	# get first joke from jokes collection
	joke = jokes.find_one()

	# async broke. just give them a damn joke.
	if joke is None:
		joke = rand_joke()

	# asyncronously do the stuff that we don't need to accomplish to give the user a joke
	thread.start_new_thread ( async, (jokes, joke) )

	return joke['joke'].strip('/')

## start a new thread to remove returned joke from the jokes collection / make a new one
def async(coll, joke):
	
	# remove used joke
	coll.remove(joke)

	text = rand_joke()

	# create mongo document
	new_joke = {
		'joke': text
	}

	# insert into collection
	coll.insert(new_joke)

	# i feel like this is necessary for async. no idea why. probably isn't. 
	return

def rand_joke():
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

for i in range(10):
	print rand_joke() +"\n"
