import os
import json
from random import randrange, seed, sample

MAX_LEN = 50


def shift(s, new):
    s = s.lstrip()
    space = s.find(' ')
    if space == -1:
        return ' ' + new
    return s[space:].lstrip().rstrip() + ' ' + new


def main():
    getw = lambda arr: '' if len(arr) == 0 else sample(arr, 1)[0]

    words = {}
    starters = 0
    wordlen = 1
    with open('../data/mapping.json') as f:
        words = json.load(f)
    keys = words.keys()

    starters = []
    for i, k in enumerate(keys):
        if k[0] == ' ':
            starters.append(k)
            keys[i] = None
    suffixes = [w for w in keys if w is not None]

    seed()
    secret = ""

    word = getw(starters)
    associated = words[word]
    secret = word.lstrip() + ' ' + getw(words[word])

    while wordlen < MAX_LEN:
        associated = words[word]
        if len(associated) == 0:
            break
        tmp = getw(associated)
        secret += ' ' + tmp

        word = shift(word, tmp)

    print secret

if __name__ == '__main__':
    main()
