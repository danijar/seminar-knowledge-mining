import math


def strip_digits(text):
    return ''.join([i for i in text if not i.isdigit()])

def strip_extension(text):
    return ''.join([i for i in text.split('.')[:-1]])

def is_nan(x):
    return isinstance(x, float) and math.isnan(x)
