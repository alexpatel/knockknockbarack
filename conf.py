from pymongo import MongoClient

## connect to mongo database
def connect(coll):
	host = 'localhost'
	port = 27017
	db_name = 'kkb'

	client = MongoClient(host, port)
	db = client[db_name]
	coll = db[coll]
	return coll