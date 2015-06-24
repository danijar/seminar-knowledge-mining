import os
import io
import numpy as np
import skimage.io
import skimage.transform
import skimage.exposure
import cairosvg
from PIL import Image
from helper.plot import plot_image


class UnsupportedImageError(Exception):
    pass


class ImageLoadingError(Exception):
    pass


def ensure_rgb(image):
    """
    Ensure consistent color format with three color channels. Expects PIL
    Image as input.
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

def clamp_size(image, width=512, height=512):
    """
    Ensure that the image is not larger than the specifier dimensions. If
    needed, the image will be scaled down in place.
    """
    size = (width, height)
    image.thumbnail(size)

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
    return ('jpg', 'jpeg', 'png', 'gif', 'svg')

def is_supported(filename):
    supported = tuple('.' + x for x in get_supported())
    if not filename.lower().endswith(supported):
        return False
    return True

def convert_svg(filename):
    """
    Converts a SVG image to PNG format and returns it as a file object.
    """
    assert filename.endswith('.svg')
    basename, extension = os.path.splitext(filename)
    png = cairosvg.svg2png(url=filename)
    return io.BytesIO(png)

def open_image(filename):
    if filename.lower().endswith('.svg'):
        png = convert_svg(filename)
        return Image.open(png)
    else:
        return Image.open(filename)

def load(filename, clamp_size=True):
    if not is_supported(filename):
        raise UnsupportedImageError
    try:
        image = open_image(filename)
        image = ensure_rgb(image)
        size = image.size
        if clamp_size:
            max_size = (512, 512)
            image.thumbnail(max_size)
        image = convert_to_array(image)
        return image, size if clamp_size else image
    except:
        raise ImageLoadingError
