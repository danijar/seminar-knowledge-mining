import shutil
import os
import re
from urllib.request import urlopen
from urllib.parse import urlsplit, urlunsplit, quote


def get_filename(url):
    return safe_characters(url.split('/')[-1])

def encode_uri(uri):
    chunks = list(urlsplit(uri))
    chunks[2] = quote(chunks[2])
    uri = urlunsplit(chunks)
    return uri

def download_file(url, directory, log=True):
    ensure_directory(directory)
    basename = get_filename(url)
    filename = os.path.join(directory, basename)
    url = encode_uri(url)
    if log:
        print('Download image:', basename)
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
