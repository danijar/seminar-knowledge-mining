import shutil
import os
import json
import constants
from urllib.request import urlopen
from helper.sparql import to_resource_uri, get_resource
from helper.format import to_filename

METADATA_EXTENSION = '.meta'
DATA_FOLDER = 'data/'

def get_data_path(path):
    return constants.DATA_FOLDER + path

def download_metadata(url, properties, directory):
    try:
        ensure_directory(directory)
        uri = to_resource_uri(url)
        filename = to_filename(url) + METADATA_EXTENSION
        print('Download metadata:', uri)
        metadata = get_resource(uri, properties)
        path = os.path.join(directory, filename)
        print('Dumping metadata to:', path, '\n')
        dump(metadata, path)
        return metadata
    except:
        print('Could not download metadata from', url)

def download_file(url, directory):
    success = False
    try:
        ensure_directory(directory)
        basename = to_filename(url)
        print('Download image:', basename)
        filename = os.path.join(directory, basename)
        with urlopen(url) as response, open(filename, 'wb') as file_:
            shutil.copyfileobj(response, file_)
        success = True
    except:
        print('Could not download file from', url)
    return success

def download_files(urls, directory):
    count = 0
    for url in urls:
        download_file(url, directory)
        count += 1
    return count

def file_exists(url, directory):
    basename = to_filename(url)
    path = os.path.join(directory, basename)
    return os.path.exists(path)

def safe_characters(text):
    if not text:
        return 'unknown'
    return re.sub('[^A-Za-z0-9.]+', '-', text)

def ensure_directory(directory):
    directory = os.path.join(directory)
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except:
        print('Could not create', directory)

def dump(dictionary, file):
    try:
        json.dump(dictionary, open(file, 'w+'))
    except:
        print('Could not write to' + file)

