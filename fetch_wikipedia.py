from urllib.request import urlopen
from bs4 import BeautifulSoup
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from helper.download import ensure_directory, download_files, safe_characters


def random_article():
    return 'http://en.wikipedia.org/wiki/Special:Random'

def images_in_article(url):
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html)
    title = safe_characters(soup.find('h1', id='firstHeading').string)
    print('Parse article:', title)
    for wrapper in soup.find_all('a', class_='image'):
        img = wrapper.find('img', recursive=False)
        yield 'http:' + img.get('src')


if __name__ == '__main__':
    parser = ArgumentParser(description='Download random images from random \
        Wikipedia articles.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-n', '--count', type=int, default=20,
        help='Rough amount of images to download')
    parser.add_argument('-d', '--directory', default='data/wikipedia',
        help='Directory to download images into; gets created if not exists')
    args = parser.parse_args()

    ensure_directory(args.directory)
    count = 0
    while count < args.count:
        urls = images_in_article(random_article())
        count += download_files(urls, args.directory)
