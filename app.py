import flask
from markov import joke

app = flask.Flask(__name__)
 
@app.route('/')
def main():
	return flask.render_template('index.html', joke=joke()) 
     
if __name__ == '__main__':
	app.run()
