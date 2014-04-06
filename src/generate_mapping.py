import os
import json

PREFIX_LEN = 2


# http://stackoverflow.com/a/8230505/1832800
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
       if isinstance(obj, set):
          return list(obj)
       return json.JSONEncoder.default(self, obj)


def shift(s, new):
    s = s.lstrip()
    space = s.find(' ')
    if space == -1:
        return ' ' + new
    return s[space:].lstrip().rstrip() + ' ' + new



def main():
    ''' This resource, even though for golang, is a trememdously helpful
        resource for implementation.
        http://golang.org/doc/codewalk/markov/
    '''
    chains = {}
    messages = []

    # Load in condensed down secrets
    with open('../data/condensed.json') as f:
        j = json.load(f)
        messages = j.get('data')

    # Generate mappings
    # TODO: I'm sure there's a much more clever way of doing this,
    # perhaps with a sliding window of three words?
    for msg in messages:
        words = msg.split(' ')
        msg = []

        # Do some sanitation
        # Take out all URLs
        for w in words:
            w = w.lstrip().rstrip()
            if w.startswith('http') or w.startswith('https'):
                continue
            w = w.replace('(', '').replace(')', '').replace('"', '')
            msg.append(w)

        msg_len = len(msg)
        prefix = ''

        for i, word in enumerate(msg):
            if i in (0, 1):
                prefix = prefix.lstrip().rstrip() + ' ' + word
            else:
                prefix = shift(prefix, word)

            if not chains.has_key(prefix):
                chains[prefix] = set()

            if (i + 1) < msg_len:
                suffix = msg[i+1]
                chains[prefix].add(suffix)

    # Write out our mapping (not in typical json reponse format though)
    with open('../data/mapping.json', 'w') as f:
        json.dump(chains, f, cls=SetEncoder)


if __name__ == '__main__':
    main()
