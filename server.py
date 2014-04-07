import os
import json
from random import randrange, seed, sample

from flask import Flask, render_template

MAX_LEN = 50

app = Flask(__name__)
words = {}
with open('data/mapping.json') as f:
    words = json.load(f)


def shift(s, new):
    space = s.find(' ')
    if space == -1:
        raise Exception('bad shift string ' + s)
    return s[space+1:] + ' ' + new


@app.route('/secret')
def get_secret():
    getw = lambda arr: sample(arr, 1)[0]

    starters = 0
    wordlen = 1
    seed()

    sparse = words.get('sparse').get('data')
    dense = words.get('dense').get('data')

    word = getw(sparse)
    associated = sparse[word]
    secret = word + ' ' + getw(associated)
    word = secret

    while wordlen < MAX_LEN:
        associated = dense.get(word, [])
        if len(associated) == 0:
            break
        tmp = getw(associated)
        secret += ' ' + tmp

        word = shift(word, tmp)
        wordlen += 1

    return secret


@app.route('/')
def index():
    return render_template('index.html', secret=get_secret())
