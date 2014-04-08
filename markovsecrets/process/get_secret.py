import os
import json
from random import randrange, seed, sample

MAX_LEN = 75


def shift(s, new):
    space = s.find(' ')
    if space == -1:
        raise Exception('bad shift string ' + s)
    return s[space+1:] + ' ' + new


def main():
    getw = lambda arr: sample(arr, 1)[0]

    words = {}
    starters = 0
    wordlen = 1
    seed()

    with open('../data/mapping.json') as f:
        words = json.load(f)
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

    print secret

if __name__ == '__main__':
    main()
