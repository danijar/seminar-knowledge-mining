import os
import shutil
import re
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from argparse import ArgumentParser


def random_article():
    return 'http://en.wikipedia.org/wiki/Special:Random'

def images_from_url(url):
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html)
    title = soup.find('h1', id='firstHeading').string
    print('Parse article:', title)
    for wrapper in soup.find_all('a', class_='image'):
        img = wrapper.find('img', recursive=False)
        yield img.get('src')

def download_file(url, folder):
    basename = re.sub('[^A-Za-z0-9.]+', '-', url.split('/')[-1])
    print('Download image:', basename)
    filename = os.path.join(folder, basename)
    with urlopen(url) as response, open(filename, 'wb') as file_:
        shutil.copyfileobj(response, file_)

def download_images_from_url(url, directory):
    count = 0
    try:
        for image in images_from_url(url):
            download_file('http:' + image, directory)
            count += 1
    except:
        print('An error occured')
    finally:
        return count


if __name__ == '__main__':
    parser = ArgumentParser(description='Download random images from ' \
        'Wikipedia articles.')
    parser.add_argument('-n', '--count', type=int, default=20,
        help='Amount of images to download')
    parser.add_argument('-d', '--directory', default='download',
        help='Directory to download images into; gets created if not exists')
    args = parser.parse_args()

    if not os.path.exists(args.directory):
        os.makedirs(args.directory)

    count = 0
    while count < args.count:
        count += download_images_from_url(random_article(), args.directory)
