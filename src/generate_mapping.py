import os
import json


'''
* Prefix length = 2
* Case-sensitive
* No URLs
* Parentheses & double quotes are stripped (rarely closed properly)

Schema:
{
    "sparse": {
        "count": 2,
        "data": {
            "Once": ["upon", "there", ...],
            "I": ["hate", "once", "saw", ...]
        }
    },
    "dense": {
        "count": 3,
        "data": {
            "Once upon": ["a", ...],
            "upon a": ["time", ...],
            "I hate": ["finals", ...]
        }
    }
}
'''


# http://stackoverflow.com/a/8230505/1832800
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
       if isinstance(obj, set):
          return list(obj)
       return json.JSONEncoder.default(self, obj)


def shift(s, new):
    space = s.find(' ')
    if space == -1:
        raise Exception('bad shift string ' + s)
    return s[space+1:] + ' ' + new


def sanitize_message(words):
    for i, w in enumerate(words):
        w = w.lstrip().rstrip()

        if w.startswith('http') or w.startswith('https'):
            # Avoid modifying length during iteration
            words[i] = None
        w = w.replace('(', '').replace(')', '').replace('"', '')

    return [w for w in words if w is not None]


def add_to_dict(dict, prefix, suffix):
    if not dict.has_key(prefix):
        dict[prefix] = set()

    dict[prefix].add(suffix)


def main():
    # Load in condensed down secrets
    messages = []
    with open('../data/condensed.json') as f:
        j = json.load(f)
        messages = j.get('data')

    sparse = {}
    dense = {}
    # Generate mappings
    for msg in messages:
        words = sanitize_message(msg.split(' '))
        words_len = len(words)

        # Check if sanitation left the message blank or with no
        # viable prefixes/suffixes.
        if words_len < 2:
            continue

        # Initial case
        add_to_dict(sparse, words[0], words[1])

        prefix = words[0] + ' ' + words[1]
        for i, word in enumerate(words[1:]):
            # Slice offset (1) & lookahead (1)
            if (i + 1 + 1) < words_len:
                add_to_dict(dense, prefix, words[i+2])
                prefix = shift(prefix, words[i+2])

    # Write out our mapping (not in typical json reponse format though)
    with open('../data/mapping.json', 'w') as f:
        chains = {
            "sparse": {
                "count": len(sparse),
                "data": sparse
            },
            "dense": {
                "count": len(dense),
                "data": dense
            }
        }
        json.dump(chains, f, cls=SetEncoder)


if __name__ == '__main__':
    main()
