from vocabulary import vocabulary
from argparse import ArgumentParser
from helper.download import get_data_path, download_metadata, download_file, file_exists, download_all
from helper.sparql import get_filenames, FILE_URL
from helper.plot import print_report
from features.archive_title import ArchiveTitleFeature
from features.label import LabelFeature


def get_predicates():
    return [
        FILE_URL,
        LabelFeature.predicate,
        ArchiveTitleFeature.predicate
    ]

def create_dataset(vocabulary, size):
    for category, keywords in vocabulary.items():
        print('Fetching filenames for:', category)
        directory = get_data_path(category + '/')
        filenames = get_filenames(keywords, size)
        if not filenames:
            continue
        download_all(filenames, get_predicates(), directory)

if __name__ == '__main__':
    parser = ArgumentParser(
        description='Creates a new dataset from dbpedia commons by querying for keywords.')
    parser.add_argument('-s', '--size', required=True,
                        help='Number of files per category to be downloaded (maximum)')
    parser.add_argument('-c', '--categories', nargs='+',
                        help='List of categories to be downloaded.')
    args = parser.parse_args()

    if not args.categories:
        create_dataset(vocabulary, args.size)
    else:
        selection = {}
        for category in args.categories:
            if category in vocabulary:
                selection[category] = vocabulary[category]
        create_dataset(selection, args.size)
