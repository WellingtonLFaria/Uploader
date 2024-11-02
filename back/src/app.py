from flask import Flask, make_response
from json import loads, dumps

app = Flask(__name__)

@app.route("/")
def index():
    return dumps("Index endpoint")