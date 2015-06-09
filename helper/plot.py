from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np


def plot_image(image):
    plt.figure()
    plt.imshow(image, interpolation='none')
    plt.show()

def plot_confusion_matrix(labels, predicted, classes):
    confusion = confusion_matrix(labels, predicted)
    # Normalize range
    confusion = confusion.astype('float') / confusion.sum(axis=1)[:, np.newaxis]
    # Create figure
    plt.figure()
    plt.imshow(confusion, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion matrix')
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()
