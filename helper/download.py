import shutil
import os
import json
from urllib.request import urlopen
from helper.sparql import to_resource_uri, get_resource, FILE_URL
from helper.format import to_filename


def get_filename(url):
    return safe_characters(url.split('/')[-1])

def download_file(url, directory):
    basename = get_filename(url)
    print('Download:', basename)
    filename = os.path.join(directory, basename)
    with urlopen(url) as response, open(filename, 'wb') as file_:
        shutil.copyfileobj(response, file_)

def download_files(urls, directory):
    count = 0
    for url in urls:
        try:
            download_file(url, directory)
            count += 1
        except:
            print('Error downloading', url)
    return count

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
