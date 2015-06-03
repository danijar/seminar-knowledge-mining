import math
import re


def to_filename(url):
    filename = safe_characters((url.split('/')[-1]).split(':')[-1])
    return filename

def safe_characters(text):
    if not text:
        return 'unknown'
    return re.sub('[^A-Za-z0-9.]+', '-', text)

def strip_digits(text):
    return ''.join([i for i in text if not i.isdigit()])

def strip_extension(text):
    return ''.join([i for i in text.split('.')[:-1]])

def is_nan(x):
    return isinstance(x, float) and math.isnan(x)
