import os
import json
import uuid
from datetime import datetime
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from helper.download import ensure_directory, download_file
from helper.dbpedia import (fetch_uris_from_metadata, fetch_uris_from_articles,
    fetch_metadata)


def read_lines(filename):
    with open(filename) as file_:
        return file_.read().splitlines()


def images_and_metadata(uris, directory):
    """
    For each uri fetch metadata from DBpedia and their image files from
    Wikimedia Commons. Uris can be either Wikimedia Commons or DBpedia Commons
    resources.
    """
    uris = list(set(uris))
    overall = len(uris)
    for index, uri in enumerate(uris):
        name = remove_prefix(os.path.basename(uri), 'File:')
        print('Image {index}/{overall}: {name}'.format(**locals()))
        uri = ensure_dbpedia_resource(uri)
        metadata = fetch_metadata(uri)
        if not metadata or not metadata['description']:
            print('Skip image without description')
            continue
        try:
            identifier = str(uuid.uuid4())
            store_image(metadata['url'], directory, identifier)
            store_metadata(metadata, directory, identifier)
        except:
            print('Error downloading image')


def ensure_dbpedia_resource(uri):
    wikimedia = '//commons.wikimedia.org/wiki'
    dbpedia = '//commons.dbpedia.org/resource'
    if dbpedia in uri:
        return uri
    elif wikimedia in uri:
        return dbpedia.replace(wikimedia, dbpedia)
    else:
        raise RuntimeError('Resource identifier ' + uri +
            ' cannot be converted to DBpedia identifier')


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
    parser.add_argument('-m', '--metadata-query', nargs='*',
        help='Keywords to look for in the image description')
    parser.add_argument('-a', '--article-query', nargs='*',
        help='Keywords to look for in names of articles containing the images')
    parser.add_argument('-c', '--count', type=int, default=100,
        help='Amount of query result images to fetch; images without \
        metadata will be skipped so fewer images may be downloaded')
    parser.add_argument('-u', '--uris',
        help='Download images and metadata from existing list of Wikimedia \
        Commons uris rather than querying them first')
    parser.add_argument('-d', '--directory',
        default='data/fetch/<timestamp>-commons',
        help='Directory to download images into; gets created if not exists')
    args = parser.parse_args()

    timestamp = str(datetime.now().strftime('%y-%m-%d-%H-%M'))
    directory = args.directory.replace('<timestamp>', timestamp)
    uris = []
    if args.uris:
        name = os.path.basename(args.uris)
        uris = read_lines(args.uris)
    elif args.metadata_query:
        name = args.metadata_query[0]
        uris = fetch_uris_from_metadata(args.metadata_query, args.count)
    elif args.article_query:
        name = args.article_query[0]
        uris = fetch_uris_from_articles(args.article_query, args.count)
    else:
        assert False, ('One of parameters --uris, --metadata-query and ' +
            '--article-query is required')

    ensure_directory(directory)
    print('Download', len(uris), 'images and metadata into', directory)
    images_and_metadata(uris, directory)
