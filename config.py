from pymongo import MongoClient

## connect to mongo database
def connect():
	host = 'localhost'
	port = 27017
	db_name = 'kkb'

	client = MongoClient(host, port)
	db = client[db_name]
	words = db.words
	words.remove()

	return words