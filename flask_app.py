import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    # This will show 'user1', 'user2', etc. so you know which one you are on
    pa_user = os.environ.get('USER', 'Unknown User')
    return f"<h1>Hello World!</h1><p>Running on PythonAnywhere account: <b>{pa_user}</b></p><p>This is update 6</p>"

@app.route('/pulse')
def pulse():
    return "Alive", 200
