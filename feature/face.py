import cv2
from skimage import img_as_ubyte
from .feature import Feature, FeatureExtractionError


class FaceFeature(Feature):

    def __init__(self, classifier, **kwargs):
        """
        Loads the pre-trained face classifier. Additional keyword arguments
        are passed to the OpenCV classifier. Please see the OpenCV
        documentation for configuration parameters.
        http://docs.opencv.org/modules/objdetect/doc/cascade_classification.ht\
        ml#cascadeclassifier-detectmultiscale
        """
        self.params = {
            'scaleFactor': 1.1,
            'minNeighbors': 4,
            'minSize': (50, 50),
            'maxSize': (2000, 2000),
            'flags': cv2.CASCADE_SCALE_IMAGE
        }
        self.params.update(kwargs)
        # Create and load classifier
        self.cascade = cv2.CascadeClassifier()
        try:
            self.cascade.load(classifier)
        except:
            raise FeatureExtractionError(self,
                'Error loading pre-trained classifier.')

    def name(self):
        return 'face'

    def keys(self):
        yield 'amount'

    def extract(self, sample):
        # Detection on the original image is much more precise
        uint8_image = img_as_ubyte(sample.original)
        face_positions = self.cascade.detectMultiScale(uint8_image,
            **self.params)
        amount = len(face_positions)
        yield amount
