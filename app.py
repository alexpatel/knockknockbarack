import flask
from markov import joke

app = flask.Flask(__name__)
 
@app.route('/')
def main():
	return joke() 
     
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)
