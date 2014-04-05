import os
import json
import requests


TOKEN = open('../APP_TOKEN', 'r').read().rstrip()
BASE_SECRETS_URL = 'https://graph.facebook.com/490886417614994/posts?'
API_URL = '{0}access_token={1}'.format(BASE_SECRETS_URL, TOKEN)


def url_builder(until=None, limit=2): # todo: raise
    url = '{api}&limit={limit}'.format(api=API_URL, limit=limit)
    if until is not None:
        url = '{limited_url}&until={time}'.format(limited_url=url, time=until)
    return url


def fetch_corpus():
    url = url_builder()
    cycle = 1
    max_cycles = 1 # todo: raise

    if not os.path.isdir('../data'):
        os.mkdir('../data')
    else:
        print('Overwriting JSON in `../data`...')

    while cycle <= max_cycles:
        print('Cycle #{0}: getting {1}'.format(cycle, url))

        # Do a request & error handling
        try:
            request = requests.get(url)
        except ConnectionError as e:
            print(e)
            return False

        print('Successfully got response in {0} seconds'.format(
            request.elapsed.total_seconds()))
        if not request.ok:
            print('Bad! Request responded with code {0}'.format(
                request.status_code))
            print('Requested URL: {0}'.format(url))
            return False

        d = json.loads(request.text)
        paging = d['paging']
        data = d['data']

        if 0 == len(data):
            print('Got 0 results...assuming done.')
            return True

        # Get next value of paging
        url = paging['next']

        # Dump object to disk
        fn = '../data/{0}.json'.format(cycle)
        with open(fn, 'w') as f:
            json.dump(d, f)

        cycle += 1

    return False


def main():
    fetch_corpus()


main()
