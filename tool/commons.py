from argparse import ArgumentParser
from helper.download import get_filename, download_file
from helper.dbpedia import fetch_filenames


def dbpedia_images(query, amount):
    uris = fetch_filenames([query], amount)
    metadata = [fetch_metadata(uri) for uri in uris]
    return list(metadata)

def store_metadata(dictionary, directory):
    url = dictionary['url']
    filename = get_filename(url) + '.meta'
    filename = os.path.join(directory, filename)
    with open(filename, 'w') as file_:
        json.dump(dictionary, file_)


if __name__ == '__main__':
    parser = ArgumentParser(description='Download Wikimedia Commons images ' \
        'and their DBpedia metadata.')
    parser.add_argument('-q', '--query', required=True,
        help='Search term')
    parser.add_argument('-c', '--count', type=int, default=100,
        help='Amount of result images to fetch')
    parser.add_argument('-d', '--directory', default='data/dbpedia/<query>',
        help='Directory to download images into; gets created if not exists')
    args = parser.parse_args()

    args.directory = args.directory.replace('<query>', args.query)

    ensure_directory(args.directory)
    metadata = dbpedia_images(args.query, args.count)
    for dictionary in metadata:
        store_metadata(dictionary, args.directory)
        download_file(dictionary['url'], args.directory)
