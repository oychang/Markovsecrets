import os
import json
import requests

TOKEN = 'XXX'
BASE_SECRETS_URL = 'https://graph.facebook.com/490886417614994/posts?'
API_URL = '{0}access_token={1}'.format(BASE_SECRETS_URL, TOKEN)
SAVE_DIRECTORY = '../../data'


def url_builder(until=None, limit=100):
    url = '{api}&limit={limit}'.format(api=API_URL, limit=limit)
    if until is not None:
        url = '{limited_url}&until={time}'.format(limited_url=url, time=until)
    return url


def fetch_corpus():
    url = url_builder()
    cycle = 1
    # Have a hard limit in case loop maintenance fails
    max_cycles = 75

    if not os.path.isdir(SAVE_DIRECTORY):
        os.mkdir(SAVE_DIRECTORY)
    else:
        print('WARN: potential overwriting...<enter to continue>')
        raw_input()

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
        paging = d.get('paging', {})
        data = d.get('data', [])

        if 0 == len(data):
            print('Got 0 results...assuming done.')
            return True

        # Dump object to disk
        fn = '{1}/{0}.json'.format(cycle, SAVE_DIRECTORY)
        with open(fn, 'w') as f:
            json.dump(d, f)

        # Get next value of paging
        url = paging.get('next')
        # This case will probably never be hit...we should get 0 results before
        # ever running out of pages, but an even split might happen.
        if url is None:
            print('No more pages.')
            break

        cycle += 1
    else:
        return True

    return False


def main():
    fetch_corpus()

if __name__ == '__main__':
    main()
