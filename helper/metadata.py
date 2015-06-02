from argparse import ArgumentParser
from SPARQLWrapper import SPARQLWrapper, JSON
from helper.download import ensure_directory
from helper.dataset import read_filenames
from features.geo_location import GeoLocationFeature
from features.file_extension import FileExtensionFeature
from features.archive_title import ArchiveTitleFeature
from features.label import LabelFeature
import constants
import csv

def get_extractors():
    return [
        FileExtensionFeature,
        LabelFeature,
        ArchiveTitleFeature,
        GeoLocationFeature
    ]

def image_uri(name):
    return '<http://commons.dbpedia.org/resource/File:' + name + '>'

def query(resource):
    sparql = SPARQLWrapper('http://commons.dbpedia.org/sparql')
    query = 'SELECT DISTINCT ?s ?p ?o WHERE {{ ?s ?p ?o FILTER (?s = {resource}) }}'.format(**locals())
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    print(query, '\n')
    data = sparql.query().convert()
    return data

def extract_predicates(metadata):
    predicates = {}
    features = get_extractors()
    for predicate in [feature.predicate for feature in features]:
        predicates[predicate] = ''
    for result in metadata['results']['bindings']:
        predicate = result['p']['value']
        for feature in features:
            if predicate == feature.predicate:
                predicates[predicate] = result['o']['value']
    return predicates

def download_metadata(path, filenames):
    try:
        with open(path, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=constants.CSV_DELIMITER,
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['filename'] + [feature.predicate for feature in get_extractors()])
            for filename in filenames:
                try:
                    print('Downloading metadata for', filename, '\n')
                    metadata = query(image_uri(filename))
                    fields = extract_predicates(metadata)
                    row = [filename]
                    for feature in get_extractors():
                        row.append(fields[feature.predicate])
                    writer.writerow(row)
                except:
                    print('Error retrieving metadata for', filename)
    except:
        print('Error creating output file.')

if __name__ == '__main__':
    parser = ArgumentParser(description='Fetch metadata from commons and save to a given location.')
    parser.add_argument('-f', '--file', required=True,
        help='Path to CSV file containing a list of filenames to be fetched.')
    parser.add_argument('-d', '--directory', default='metadata',
        help='Directory to download metadata into; gets created if not exists')
    args = parser.parse_args()

    ensure_directory(args.directory)

    filenames = read_filenames(args.file)
    path = args.directory + '/commons.csv'
    download_metadata(path, filenames)
