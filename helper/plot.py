import matplotlib.pyplot as plt
import numpy as np


def plot_image(image):
    plt.figure()
    plt.imshow(image, interpolation='none')
    plt.show()
