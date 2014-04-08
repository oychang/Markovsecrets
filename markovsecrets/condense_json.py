import os
import json
from glob import glob

from unidecode import unidecode


def save_messages(ls):
    d = {
        'data': ls,
        'count': len(ls)
    }

    with open('../data/condensed.json', 'w') as f:
        json.dump(d, f)

    return True


def condense():
    files = glob('../data/[0-9]*.json')
    messages = []

    for filename in files:
        with open(filename) as f:
            j = json.load(f)
            for msg in j.get('data'):
                # Here, we strip off the leading number,
                # any newlines, and leading/trailing whitespace
                message = msg.get('message')

                if message is None:
                    continue
                elif message.startswith('#'):
                    message = message[message.find(' '):]

                message = message.lstrip().rstrip().replace('\n', ' ')
                message = unidecode(message)

                messages.append(message)
    else:
        save_messages(messages)
        return True

    return False


def main():
    condense()

if __name__ == '__main__':
    main()
