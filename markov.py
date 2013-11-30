from config import connect
from random import randint	

def generate(start_word=None, pos=None):
	words = connect()
	try:
		if start_word:
			# pick a random beginning with start_word as first word
			word = words.find({'1': start_word})[randint(0, words.find({'1': start_word}).count())]
		elif pos:
			# pick a random beginning with pos as part of speech
			word = words.find({'pos': pos})[randint(0, words.find({'pos': pos}).count())]
		else:
			# get random sentence beginning
			word = words.find({'start': True})[randint(0, words.find({'start': True}).count())]
	except IndexError:		
		return

	sentence = word['1'].capitalize()+' '
	print sentence

	i = 0

	while True:
		#try: 
		#count =  words.find({'1': word['2'], '2': word['3']}).count()
		#word = words.find({'1': word['2'], '2': word['3']})[randint(0, words.find({'1': word['2'], '2': word['3']}).count())]
		#sentence += ' '+word['1']
	
		count =  words.find({'1': word['2'], '2': word['3']}).count()
		if count != 0:
			word = words.find({'1': word['2'], '2': word['3']})[randint(0, words.find({'1': word['2'], '2': word['3']}).count() - 1)]
		else:
			word = words.find()[randint(0, words.find().count())]
	
		sentence += word['1']+' '
		print sentence

		i += 1
	

		#except IndexError:	
		#	print "error:" +
		#	break


generate()