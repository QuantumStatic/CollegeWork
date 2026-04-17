import cv2
import numpy as np

from image_reader import get_gallery_image


def extract_colours(img: np.ndarray):
    feature_matrix = np.zeros((img.shape[0], img.shape[1]))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            feature_matrix[i, j] = round((float(img[i, j, 0]) + float(img[i, j, 1]) + float(img[i, j, 2])) / 3, 0)

    print(feature_matrix)
    cv2.imshow('feature_matrix', feature_matrix)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()
