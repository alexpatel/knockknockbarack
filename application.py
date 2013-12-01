from flask import Flask
from markov import joke

application = Flask(__name__)
application.config.from_object(__name__)

@application.route('/')
def main():
	return joke()

if __name__ == '__main__':
	application.run(host='0.0.0.0', debug=True)