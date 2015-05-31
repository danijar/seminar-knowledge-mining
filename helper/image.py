import skimage.io
import skimage.transform
import skimage.exposure
import numpy as np
import matplotlib.pyplot
from PIL import Image


def ensure_rgb(image):
    """
    Ensure consistent color format with three color channels
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')
    return image

def convert_to_array(image):
    """
    Convert Pillow image to Numpy array used by scikit
    """
    image = np.asarray(image, dtype=np.uint8)
    return image

def preprocess(image):
    # Force scale to size
    nearest = 0
    image = skimage.transform.resize(image, (128, 128), order=nearest)
    # Scale contrast range
    ignore_extrema = (np.percentile(image, 2), np.percentile(image, 98))
    image = skimage.exposure.rescale_intensity(image, in_range=ignore_extrema)
    return image

def is_supported(filename):
    supported = ('jpg', 'jpeg', 'bmp', 'png', 'gif', 'svg', 'ico')
    supported = tuple('.' + x for x in supported)
    if not filename.lower().endswith(supported):
        return False
    return True

def load(filename):
    if not is_supported(filename):
        print('Skipped', filename)
        return None
    try:
        # Open with Pillow for color mode conversion
        image = Image.open(filename)
        image = ensure_rgb(image)
        image = convert_to_array(image)
        image = preprocess(image)
        return image
    except:
        print('Error opening image')
        return None

def show(image):
    matplotlib.pyplot.figure()
    skimage.io.imshow(image)
    skimage.io.show()
