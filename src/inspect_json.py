from sys import argv
from os.path import isfile
import json
from pprint import pprint


def main():
    if len(argv) < 2 or not isfile(argv[1]):
        print('Provide a valid file as argument.')
        return False

    with open(argv[1]) as f:
        j = json.load(f)
        try:
            pprint(j)
        except IOError:
            # Some issue with a broken pipe
            pass
    return True


if __name__ == '__main__':
    main()
