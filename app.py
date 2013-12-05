import flask
from markov import joke

app = flask.Flask(__name__)
 
@app.route('/')
def main():
	return flask.render_template('index.html', joke=joke()) 

@app.route('/_joke')
def get_joke():
	return joke()

if __name__ == '__main__':
	app.run()
