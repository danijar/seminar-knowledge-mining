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

def print_headline(text):
    underline = '-' * len(text)
    print('\n' + text + '\n' + underline)

def print_bars():
    bars = '='.join(['' for i in range(0, 20)])
    print('\n' + bars + '\n')

def dumpclean(obj):
    if type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                dumpclean(v)
            else:
                print(v)
    elif type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print(k + '\n')
                print_bars()
                dumpclean(v)
            else:
                print('%s : %s' % (k, v))
    else:
        print(obj)

def print_report(stats):
    print_bars()
    print('Report')
    print_bars()
    dumpclean(stats)
    print_bars()
