import os
import json
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

    def generic_sanitize(self, s):
        s = sub(r'[\"\(\)\[\]]', '', s)
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


def main():
    fb = condense_facebook()


if __name__ == '__main__':
    main()
