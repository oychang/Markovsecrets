import os
import json

from condense import DATA_DIR

'''
* Prefix length = 2
* Case-sensitive
* No URLs
* Parentheses & double quotes are stripped (rarely closed properly)

# TODO: update
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


def add_to_dict(dict, prefix, suffix):
    if not dict.has_key(prefix):
        dict[prefix] = set()

    dict[prefix].add(suffix)


def main():
    # Load in condensed down secrets
    with open('{0}/condensed.json'.format(DATA_DIR)) as f:
        j = json.load(f)

    sparse = {}
    dense = {}

    # Generate mappings
    for group in j:
        for msg in j.get(group):
            words = msg.split(' ')
            words_len = len(words)
            initial = True

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
                    if initial:
                        words[0] = words[0][0].lower() + words[0][1:] + ' ' + words[1]
                        add_to_dict(dense, prefix, words[i+2])
                        initial = False

                    prefix = shift(prefix, words[i+2])

    # Write out our mapping
    with open('{0}/mapping.json'.format(DATA_DIR), 'w') as f:
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
