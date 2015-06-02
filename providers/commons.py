import categories
from argparse import ArgumentParser
from helper.download import get_data_path, download_metadata, download_file, file_exists
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
    report = []

    for category, keywords in vocabulary.items():
        print('Fetching for keywords:', keywords)
        directory = get_data_path(category + '/')
        filenames = get_filenames(keywords, size)

        if not filenames:
            continue
        else:
            stats = {}
            stats[category + '_filenames'] = len(filenames)
            stats[category + '_metadata'] = 0
            stats[category + '_images'] = 0
            stats[category + '_fields'] = 0
            stats[category + '_fields_empty'] = 0

        for filename in filenames:
            if file_exists(filename, directory):
                print('Skipping already downloaded file:', filename)
                continue
            metadata = download_metadata(filename, get_predicates(), directory)
            if not metadata:
                continue
            image = download_file(metadata[FILE_URL], directory)
            num_results = len(metadata)
            num_empty = len([k for k,v in metadata.items() if not v])
            stats[category + '_fields'] += num_results
            stats[category + '_fields_empty'] += num_empty
            stats[category + '_metadata'] += 1
            stats[category + '_images'] += 1 if image else 0
        report.append(stats)
    print_report(report)


if __name__ == '__main__':
    parser = ArgumentParser(description='Creates a new dataset from dbpedia commons by querying for keywords.')
    parser.add_argument('-s', '--size', required=True,
        help='Number of files per category to be downloaded (maximum)')
    parser.add_argument('-c', '--categories', nargs='+',
        help='List of categories to be downloaded.')
    args = parser.parse_args()

    vocabulary = {}
    if args.categories:
        for category in args.categories:
            if category in categories.vocabulary:
                vocabulary[category] = categories.vocabulary[category]
    else:
        vocabulary = categories.vocabulary
    create_dataset(vocabulary, args.size)


