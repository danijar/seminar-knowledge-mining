import re
import shutil
import os
from urllib.request import urlopen


def download_file(url, directory):
    basename = safe_characters(url.split('/')[-1])
    print('Download image:', basename)
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
            print('An error occured')
    return count

def safe_characters(text):
    if not text:
        return 'unknown'
    return re.sub('[^A-Za-z0-9.]+', '-', text)

def ensure_directory(directory):
    directory = os.path.join(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)
