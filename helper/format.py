import math
import re


def safe_characters(text):
    if not text:
        return 'unknown'
    return re.sub('[^A-Za-z0-9.]+', '-', text)

# def strip_digits(text):
#     return ''.join([i for i in text if not i.isdigit()])

# def is_nan(x):
#     return isinstance(x, float) and math.isnan(x)
