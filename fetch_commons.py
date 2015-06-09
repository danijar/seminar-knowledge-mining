import os
import json
import uuid
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from helper.download import ensure_directory, get_filename, download_file
from helper.dbpedia import fetch_uris, fetch_metadata


def read_uris(filename):
    with open(filename) as uris:
        return [uri.rstrip('\n') for uri in uris]

def images_and_metadata(uris, directory):
    amount = len(uris)
    for index, uri in enumerate(uris):
        name = remove_prefix(os.path.basename(uri), 'File:')
        print('Image {index}/{amount}: {name}'.format(**locals()))
        metadata = fetch_metadata(uri)
        if not metadata or not metadata['description']:
            print('Skip image without description')
            continue
        try:
            identifier = str(uuid.uuid4())
            store_metadata(metadata, directory, identifier)
            store_image(metadata['url'], directory, identifier)
        except:
            print('Error downloading image')

def store_metadata(metadata, directory, identifier):
    filename = os.path.join(directory, identifier + '.json')
    with open(filename, 'w') as file_:
        json.dump(metadata, file_)

def store_image(url, directory, identifier):
    extension = url.split('.')[-1].lower()
    filename = os.path.join(directory, identifier + '.' + extension)
    download_file(url, directory, filename, log=False)

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


if __name__ == '__main__':
    parser = ArgumentParser(description='Download Wikimedia Commons images \
        their DBpedia metadata.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-q', '--query',
        help='Search term')
    parser.add_argument('-c', '--count', type=int, default=20,
        help='Amount of result images to fetch')
    parser.add_argument('-u', '--uris',
        help='Download images and metadata from existing list of Wikimedia \
        Commons uris; ignores --query and --count')
    parser.add_argument('-d', '--directory', default='data/commons/<name>',
        help='Directory to download images into; gets created if not exists; \
        <name> gets replaced with query or filename or uris list')
    args = parser.parse_args()


    uris = []
    if args.uris:
        basename = os.path.basename(args.uris)
        args.directory = args.directory.replace('<name>', basename)
        uris = read_uris(args.uris)
    elif args.query:
        args.directory = args.directory.replace('<name>', args.query)
        uris = fetch_uris([args.query], args.count)
    else:
        print('One of parameters --uris and --query is required')
    ensure_directory(args.directory)
    images_and_metadata(uris, args.directory)
