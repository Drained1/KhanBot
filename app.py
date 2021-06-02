from flask import Flask, render_template, request, session, redirect, jsonify
from threading import Thread

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

def run():
    app.run(host = '0.0.0.0', port=8000)

def start():
    server = Thread(target = run)
    server.start()