import flask
from markov import joke
from build import build
from werkzeug.contrib.fixers import ProxyFix

 
app = flask.Flask(__name__)
 
@app.route('/')
def main():
	return joke() 

app.wsgi_app = ProxyFix(app.wsgi_app)
     
if __name__ == '__main__':
	app.run()
