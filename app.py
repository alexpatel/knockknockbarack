import flask
from markov import joke, rand_joke
from werkzeug.contrib.fixers import ProxyFix

app = flask.Flask(__name__)
 
@app.route('/')
def main():
	return flask.render_template('index.html', joke=joke()) 

@app.route('/_get_joke')
def get_joke():
	return joke()

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
	# for deployment
	app.run(host='0.0.0.0', port=80)

	# dev server
	#app.run(debug=True)

