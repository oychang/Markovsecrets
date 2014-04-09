import os
import json
from random import randrange, seed, sample

from condense import DATA_DIR

MAX_LEN = 75
words = None


def shift(s, new):
    space = s.find(' ')
    if space == -1:
        raise Exception('bad shift string ' + s)
    return s[space+1:] + ' ' + new


def get_word(arr):
    return sample(arr, 1)[0]


def secret_me_bro():
    global words
    if words is None:
        seed()
        with open('{0}/mapping.json'.format(DATA_DIR)) as f:
            words = json.load(f)

    wordlen = 1
    sparse = words.get('sparse').get('data')
    dense = words.get('dense').get('data')

    word = get_word(sparse)
    associated = sparse[word]
    secret = word + ' ' + get_word(associated)
    word = secret

    while wordlen < MAX_LEN:
        associated = dense.get(word, [])
        if len(associated) == 0:
            break
        tmp = get_word(associated)
        secret += ' ' + tmp

        word = shift(word, tmp)
        wordlen += 1

    return secret
