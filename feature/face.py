import cv2
from skimage import img_as_ubyte
from .feature import Feature, FeatureExtractionError


class FaceFeature(Feature):

    def __init__(self, classifier, scaleFactor=1.1, minNeighbors=4,
        minSize=(50,50), maxSize=(2000,2000), flags=cv2.CASCADE_SCALE_IMAGE):
        """
        Please refer to the OpenCV documentation for configuration parameters:
            http://docs.opencv.org/modules/objdetect/doc/
            cascade_classification.html#cascadeclassifier-detectmultiscale
        """
        self.scaleFactor = scaleFactor
        self.minNeighbors = minNeighbors
        self.minSize = minSize
        self.maxSize = maxSize
        self.flags = flags
        try:
            # Requires a trained classifier for face detection
            self.cascade = cv2.CascadeClassifier()
            self.cascade.load(classifier)
        except:
            raise FeatureExtractionError(self, 'Error loading classifier.')

    def name(self):
        return 'face'

    def keys(self):
        yield 'num'

    def extract(self, sample):
        # Detection on the original image is much more precise
        uint8_image = img_as_ubyte(sample.original)
        face_positions = self.cascade.detectMultiScale(uint8_image,
            scaleFactor=self.scaleFactor, minNeighbors=self.minNeighbors,
            minSize=self.minSize, maxSize=self.maxSize,
            flags=self.flags)
        num_faces = len(face_positions)
        yield num_faces
