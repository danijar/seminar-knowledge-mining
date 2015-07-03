import os
import json
import helper.image as image


class Sample:
    """
    Represents a sample of the dataset. From the image filename, all supported
    attributes are lazy-loaded on access. To add attributes to this class, just
    provide a new _load_<key>() method and make sure to call _ensure() on all
    attributes this method relies on, so that those can be lazy-loaded as well.
    """

    def __init__(self, filename, label=None):
        self.filename = filename
        self.label = label

    def __getattr__(self, key):
        """
        Try to lazy-load attributes that do not exist.
        """
        self._ensure(key)
        return object.__getattribute__(self, key)

    def __setattr__(self, key, value):
        """
        Avoid overriding existing attributes. All attributes are read-only.
        """
        assert not self._has_attr(key), ('Sample attributes are readonly, '
            'cannot write {key}'.format(**locals()))
        object.__setattr__(self, key, value)

    def _ensure(self, key):
        """
        Calls self._load_<key>() to load the requested attribute. If the
        loading method is not found, an AttributeError is raised.
        """
        if self._has_attr(key):
            return
        loader_name = '_load_' + key
        loader = object.__getattribute__(self, loader_name)
        loader()
        assert self._has_attr(key), ('Loader {loader_name} did not load '
            '{key}'.format(**locals()))

    def _has_attr(self, key):
        try:
            object.__getattribute__(self, key)
            return True
        except AttributeError:
            return False

    def _load_original(self):
        self._ensure('filename')
        # Size must be set here as well since even the original image may be
        # scaled down a little bit inside image.load() for performance reasons.
        self.original, self.size = image.load(self.filename)

    def _load_size(self):
        self._ensure('original')

    def _load_width(self):
        self._ensure('size')
        self.width = self.size[0]

    def _load_height(self):
        self._ensure('size')
        self.height = self.size[1]

    def _load_image(self):
        self._ensure('original')
        self.image = image.preprocess(self.original)

    def _load_hsv(self):
        self._ensure('image')
        self.hsv = image.convert_to_hsv(self.image)

    def _load_gray(self):
        self._ensure('image')
        self.gray = image.convert_to_gray(self.image)

    def _load_metadata(self):
        self._ensure('filename')
        keys = ('url', 'title', 'description', 'extension', 'lat', 'long')
        filename = self._replace_extension(self.filename, 'json')
        try:
            with open(filename) as file_:
                dictionary = json.load(file_)
                assert set(dictionary.keys()) == set(keys), 'Invalid metadata'
                self.metadata = True
        except IOError:
            self.metadata = False
            dictionary = {key: '' for key in keys}
            dictionary['extension'] = os.path.splitext(self.filename)[1][1:]
        # Update attributes from dictionary
        for key, value in dictionary.items():
            setattr(self, key, value)

    def _replace_extension(self, filename, extension):
        basename, _ = os.path.splitext(filename)
        return basename + '.' + extension

    def _load_url(self):
        self._ensure('metadata')

    def _load_title(self):
        self._ensure('metadata')

    def _load_description(self):
        self._ensure('metadata')

    def _load_extension(self):
        self._ensure('metadata')

    def _load_lat(self):
        self._ensure('metadata')

    def _load_long(self):
        self._ensure('metadata')
