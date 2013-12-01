import flask
from markov import joke
from build import build
 
application = flask.Flask(__name__)

application.debug=True
 
@application.route('/')
def main():
    return joke() 
     
if __name__ == '__main__':
	build()
    application.run(host='0.0.0.0', debug=True)