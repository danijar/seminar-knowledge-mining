import re
from functools import wraps
import matplotlib.pyplot as plt
import numpy as np


def listify(fn=None, wrapper=list):
    """
    Decorator to make generator functions return a list.
    """
    def listify_return(fn):
        @wraps(fn)
        def listify_helper(*args, **kw):
            return wrapper(fn(*args, **kw))
        return listify_helper
    if fn is None:
        return listify_return
    return listify_return(fn)

def plot_image(image):
    plt.figure()
    plt.imshow(image, interpolation='none')
    plt.show()

def print_headline(text, symbol='-'):
    assert len(symbol) == 1
    underline = symbol * len(text)
    print('\n' + text + '\n' + underline)
