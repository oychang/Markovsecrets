import os
import json
import codecs
from re import sub
from glob import glob

from unidecode import unidecode
from fetch_facebook import SAVE_DIRECTORY as FB_DIR

DATA_DIR = '../../data'


class StringSanitizer(object):
    def whitespace_sanitize(self, s):
        return sub(r'\s+', ' ', s)

    def link_sanitize(self, s):
        return s if not s.startswith(('http', 'https')) else ''

    def generic_sanitize(self, s, blacklist=r'[\"\(\)\[\]]'):
        s = sub(blacklist, '', s)
        return sub(r'\n| - | -- ', ' ', s)

    def sanitize(self, s):
        s = unidecode(s)
        s = self.link_sanitize(s)
        s = self.generic_sanitize(s)
        s = self.whitespace_sanitize(s)
        s = s.strip()

        if s in ('', ' '):
            return None
        return s


class FacebookSanitizer(StringSanitizer):
    # Strip off leading "#n: ""
    def sanitize(self, s):
        s = super(FacebookSanitizer, self).sanitize(s)
        if s is None:
            return None
        return sub(r'#[0-9]+:? ', '', s)


class RapGeniusSanitizer(StringSanitizer):
    # Get rid of annotations, e.g. [Chorus], [Verse 1: artist]
    def sanitize(self, s):
        s = sub(r'\[[\w: ]+\]', ' ', s)
        return super(RapGeniusSanitizer, self).sanitize(s)


class PoetrySanitizer(StringSanitizer):
    pass


def condense_facebook():
    sanitizer = FacebookSanitizer()
    files = glob('{0}/[0-9]*.json'.format(FB_DIR))
    messages = []

    for filename in files:
        with open(filename) as f:
            j = json.load(f)
        for msg in j.get('data'):
            message = msg.get('message')
            if message is None:
                continue

            message = sanitizer.sanitize(message)
            if message is not None:
                messages.append(message)

    return messages


def condense_rapgenius():
    sanitizer = RapGeniusSanitizer()
    fn = '{0}/rapgenius/lyrics.json'.format(DATA_DIR)
    messages = []

    with open(fn) as f:
        j = json.load(f)
    for artist in j:
        lines = j.get(artist)
        for line in lines:
            for subline in line.split('\n'):
                lyric = sanitizer.sanitize(subline)
                if lyric is not None:
                    messages.append(lyric)

    return messages


def condense_poetry():
    sanitizer = PoetrySanitizer()
    files = glob('{0}/poetry/*.txt'.format(DATA_DIR))
    cleaned_lines = []

    for fn in files:
        with codecs.open(fn, 'r', 'utf-8') as f:
            txt = f.readlines()
        for line in txt:
            line = sanitizer.sanitize(line)
            if line is not None:
                cleaned_lines.append(line)

    return cleaned_lines


def save_json(**kwargs):
    fn = '{0}/condensed.json'.format(DATA_DIR)
    with open(fn, 'w') as f:
        json.dump(kwargs, f)


def main():
    fb = condense_facebook()
    rg = condense_rapgenius()
    poetry = condense_poetry()
    save_json(fb=fb, rg=rg, poetry=poetry)


if __name__ == '__main__':
    main()
