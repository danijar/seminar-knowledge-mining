import os
import json
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from helper.download import ensure_directory, get_filename, download_file
from helper.dbpedia import fetch_uris, fetch_metadata


def images_and_metadata(query, amount):
    uris = fetch_uris([query], amount)
    for uri in uris:
        metadata = fetch_metadata(uri)
        if not metadata or not metadata['description']:
            print('Skip image without description')
            continue
        store_metadata(metadata, args.directory)
        download_file(metadata['url'], args.directory)

def store_metadata(metadata, directory):
    url = metadata['url']
    filename = get_filename(url) + '.json'
    filename = os.path.join(directory, filename)
    with open(filename, 'w') as file_:
        json.dump(metadata, file_)


if __name__ == '__main__':
    parser = ArgumentParser(description='Download Wikimedia Commons images \
        their DBpedia metadata.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-q', '--query', required=True,
        help='Search term')
    parser.add_argument('-c', '--count', type=int, default=20,
        help='Amount of result images to fetch')
    parser.add_argument('-d', '--directory', default='data/commons/<query>',
        help='Directory to download images into; gets created if not exists')
    args = parser.parse_args()

    args.directory = args.directory.replace('<query>', args.query)

    ensure_directory(args.directory)
    images_and_metadata(args.query, args.count)
