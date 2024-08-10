from flask import request
from flask import Flask

from aisearch import aisearch

cache = {}
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/search')
def search():
    query = request.args.get('query')
    return aisearch(query)


if __name__ == '__main__':
    app.run()
