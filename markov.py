from config import connect
from random import randint	

## generate a markov
def generate(start_word=None, pos=None):
	words = connect()

	if start_word:
		# pick a random beginning with start_word as first word
		word = words.find({'1': start_word})[randint(0, words.find({'1': start_word}).count() - 1)]
	elif pos:
		# pick a random beginning with pos as part of speech
		word = words.find({'pos': pos})[randint(0, words.find({'pos': pos}).count() - 1)]
	else:
		# get random sentence beginning
		word = words.find({'start': True})[randint(0, words.find({'start': True}).count() - 1)]

	phrase = word['1']+' '

	# build word until natural sentence end is reached
	while not word['end']:	
		count =  words.find({'1': word['2'],  '2': word['3']}).count()
		if count != 0:
			word = words.find({'1': word['2'], '2': word['3']})[randint(0, count - 1)]
		else:
			# no order-2 match. try order-1
			count =  words.find({'1': word['2']}).count()
			if count != 0:
				word = words.find({'1': word['2']})[randint(0, count - 1)]
			else:
				# last resort = random word
				count =  words.find().count()
				word = words.find()[randint(0, count - 1)]
	
		# add word to chain
		phrase += word['1']+' '

	print phrase
	return phrase

generate()