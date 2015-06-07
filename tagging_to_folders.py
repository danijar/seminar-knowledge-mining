import os, shutil, re
from argparse import ArgumentParser
from helper.download import ensure_directory


def read_tagging(filename):
    with open(filename) as tagging:
        columns = [line.strip().split(',') for line in tagging]
        tagging = {image: tag for image, tag in columns}
        for image, tag in tagging.items():
            tagging[image] = re.sub('[^a-z]+', '-', tag)
        return tagging

def distinct_tags(tagging):
    return set(tag for tag in tagging.values())

def ensure_folders(tags, output):
    for tag in tags:
        directory = os.path.join(output, tag)
        ensure_directory(directory)

def move_into_folders(tagging, images, output):
    for image, tag in tagging.items():
            source = os.path.join(images, image)
            destination = os.path.join(output, tag, image)
            try:
                shutil.move(source, destination)
                print(destination)
            except:
                print('Cannot move file', source)


if __name__ == '__main__':
    parser = ArgumentParser(description='Move tagged images into folders of\
        their tags.')
    parser.add_argument('-i', '--images', required=True,
        help='Directory containing the image files')
    parser.add_argument('-t', '--tagging', required=True,
        help='Filename of mapping from image names to tags')
    parser.add_argument('-o', '--output', default='data/class',
        help='Directory the tag directories and images should be places in')
    args = parser.parse_args()

    tagging = read_tagging(args.tagging)
    tags = distinct_tags(tagging)
    ensure_folders(tags, args.output)
    move_into_folders(tagging, args.images, args.output)
