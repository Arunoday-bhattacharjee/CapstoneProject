from flask import Flask
flaskapp = Flask(__name__)

@app.route("/")

def hello():
    return "Hello World"
