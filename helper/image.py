import skimage.io
import skimage.transform
import skimage.exposure
import numpy as np
from PIL import Image
from helper.plot import plot_image


def ensure_rgb(image):
    """
    Ensure consistent color format with three color channels
    """
    if image.mode == 'RGBA':
        image = fill_alpha(image)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    return image

def fill_alpha(image, color=(255, 255, 255)):
    data = np.array(image)
    r, g, b, a = np.rollaxis(data, axis=-1)
    r[a == 0] = color[0]
    g[a == 0] = color[1]
    b[a == 0] = color[2]
    data = np.dstack([r, g, b, a])
    return Image.fromarray(data, 'RGBA')

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
    assert image.shape == (128, 128, 3)
    # Scale contrast range
    ignore_extrema = (np.percentile(image, 2), np.percentile(image, 98))
    # Auto contrast if more than one color
    if len(np.unique(image)) > 1:
        image = skimage.exposure.rescale_intensity(image, in_range=ignore_extrema)
    return image

def get_supported():
    return ('jpg', 'jpeg', 'bmp', 'png', 'gif', 'svg', 'ico')

def is_supported(filename):
    supported = tuple('.' + x for x in get_supported())
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
        max_size = 512, 512
        image.thumbnail(max_size)
        image = convert_to_array(image)
        return image
    except:
        print('Error opening image')
        return None
