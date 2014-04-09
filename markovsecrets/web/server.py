from flask import Flask, render_template
from process.get_secret import secret_me_bro

app = Flask(__name__)


@app.route('/secret')
def get_secret():
    return secret_me_bro()


@app.route('/')
def index():
    return render_template('index.html', secret=get_secret())
