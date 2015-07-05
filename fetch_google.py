import json
from urllib.request import Request, urlopen
from urllib.parse import quote_plus
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from helper.download import ensure_directory, download_files


def google_images_request(query, page):
    assert 0 <= page <= 7
    # Prepare url
    api = 'https://ajax.googleapis.com/ajax/services/search/images'
    query = quote_plus(query)
    userip = '85.182.0.136'
    start = int(8 * page)
    url = '{api}?v=1.0&q={query}&userip={userip}&rsz=8&start={start}'.format(
        **locals())
    # Prepare request
    request = Request(url)
    service = 'http://{}/'.format(userip)
    request.add_header('Referer', service)
    return request


def google_images(query, pages):
    for page in range(pages):
        request = google_images_request(query, page)
        print('Query page', page + 1)
        # Fetch results
        response = urlopen(request).readall().decode('utf-8')
        content = json.loads(response)
        results = content['responseData']['results']
        # Return urls
        for result in results:
            yield result['url']


if __name__ == '__main__':
    parser = ArgumentParser(description='Download Google image search \
        results.', formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-q', '--query', required=True,
        help='Search term')
    parser.add_argument('-p', '--pages', type=int, default=8,
        help='Amount of result pages to fetch; up to 8')
    parser.add_argument('-d', '--directory', default='data/google/<query>',
        help='Directory to download images into; gets created if not exists')
    args = parser.parse_args()

    args.directory = args.directory.replace('<query>', args.query)

    ensure_directory(args.directory)
    urls = google_images(args.query, args.pages)
    download_files(urls, args.directory)
