import flask
from markov import joke, rand_joke

app = flask.Flask(__name__)
 
@app.route('/')
def main():
	return flask.render_template('index.html', joke=joke()) 

@app.route('/_get_joke')
def get_joke():
	return joke()

if __name__ == '__main__':
	# for deployment
	app.run(host='0.0.0.0', port=80)

	# dev server
	#app.run()
