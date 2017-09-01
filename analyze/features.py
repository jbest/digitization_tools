import cv2
import numpy as np

# modified from http://www.pyimagesearch.com/2014/01/27/hobbits-and-histograms-a-how-to-guide-to-building-your-first-image-search-engine-in-python/
def describe(image, bins = [8, 8, 8]):
    # compute a 3D histogram in the RGB colorspace,
    # then normalize the histogram so that images
    # with the same content, but either scaled larger
    # or smaller will have (roughly) the same histogram
    hist = cv2.calcHist([image], [0, 1, 2], None, bins, [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist)

    # return out 3D histogram as a flattened array
    return hist.flatten()

# from http://www.pyimagesearch.com/2014/01/27/hobbits-and-histograms-a-how-to-guide-to-building-your-first-image-search-engine-in-python/
def chi2_distance(histA, histB, eps = 1e-10):
    # compute the chi-squared distance
    d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
        for (a, b) in zip(histA, histB)])
    # return the chi-squared distance
    return d