from flask import Flask, render_template
from process.get_secret import secret_me_bro

app = Flask(__name__)


@app.route('/secret')
def get_secret():
    secret = secret_me_bro()
    words = secret.count(' ') + 1

    if words < 10:
        secret = 'Confucius says "{0}"'.format(secret)

    return secret


@app.route('/')
def index():
    return render_template('index.html', secret=get_secret())
