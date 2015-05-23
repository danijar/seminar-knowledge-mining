from PIL import Image, ImageOps


def load(filename, size=64, ignore_extrema=5):
    """
    Loads an image and returns both the original as well as a
    preprocessed version.
    """
    original = Image.open(filename)
    resized = original.resize((size, size), Image.LANCZOS)
    normalized = ImageOps.autocontrast(resized, ignore_extrema)
    return original, normalized
