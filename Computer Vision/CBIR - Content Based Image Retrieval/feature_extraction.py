import numpy
from skimage.feature import corner_harris, corner_peaks, corner_subpix
import cv2
from scipy import signal as sig
import scipy
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import filters
import math


def harris_corner_detector(img_bw: numpy.ndarray) -> numpy.ndarray:
    kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    kernel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

    I_x = sig.convolve2d(img_bw, kernel_x, mode='same')
    I_y = sig.convolve2d(img_bw, kernel_y, mode='same')

    Ixx = scipy.ndimage.gaussian_filter(I_x ** 2, sigma=1)
    Ixy = scipy.ndimage.gaussian_filter(I_y * I_x, sigma=1)
    Iyy = scipy.ndimage.gaussian_filter(I_y ** 2, sigma=1)

    # k = 0.2
    #
    # # determinant
    # detA = Ixx * Iyy - Ixy ** 2
    # # trace
    # traceA = Ixx + Iyy
    #
    # harris_response = detA - (k * traceA ** 2)
    # print(type(harris_response))
    #
    # img_copy_for_corners = np.copy(img_colour)
    # img_copy_for_edges = np.copy(img_colour)

    k = 0.02
    height, width, offset = Ixx.shape[0], Ixx.shape[1], 1
    harris_response = np.zeros((height, width))
    for y in range(offset, height - offset):
        for x in range(offset, width - offset):
            Sxx = np.sum(Ixx[y - offset:y + 1 + offset, x - offset:x + 1 + offset])
            Syy = np.sum(Iyy[y - offset:y + 1 + offset, x - offset:x + 1 + offset])
            Sxy = np.sum(Ixy[y - offset:y + 1 + offset, x - offset:x + 1 + offset])

            det = (Sxx * Syy) - (Sxy ** 2)
            trace = Sxx + Syy
            r = det - k * (trace ** 2)

            harris_response[y, x] = r

    non_max_corners = corner_peaks(harris_response, threshold_abs=0.01, threshold_rel=0.01)
    # single-tone image to pass to corner_subpix
    # corners_subpix = corner_subpix(img, non_max_corners, window_size=3)

    # fig, ax = plt.subplots()
    # ax.imshow(img, interpolation='nearest', cmap=plt.cm.gray)
    # ax.plot(non_max_corners[:, 1], non_max_corners[:, 0], '.r', markersize=3)
    # # ax.plot(corners_subpix[:, 1], corners_subpix[:, 0], color='red', markersize=3)
    # fig.savefig('corners.png')

    return non_max_corners


def blob_detector(img_bw: numpy.ndarray) -> numpy.ndarray:
    k = 2 ** 0.5
    sig = 1.0
    img = img_bw / 255.0

    def LoG(sig):
        n = math.ceil(sig * 6)
        y, x = np.ogrid[-n // 2:n // 2 + 1, -n // 2:n // 2 + 1]
        y_filter = np.exp(-(y * y / (2. * sig * sig)))
        x_filter = np.exp(-(x * x / (2. * sig * sig)))
        final_filter = (-(2 * sig ** 2) + (x * x + y * y)) * (x_filter * y_filter) * (1 / (2 * math.pi * sig ** 4))
        return final_filter

    log_images = []
    for i in range(0, 9):
        y = k ** i
        sigma_1 = sig * y
        filter_log = LoG(sigma_1)
        image = cv2.filter2D(img, -1, filter_log)
        image = np.pad(image, ((1, 1), (1, 1)), 'constant')
        image = np.square(image)
        log_images.append(image)
    log_image_np = np.array(log_images)

    # Get co-ordinates for the blobs
    co_ordinates = []
    (h, w) = img.shape
    for i in range(1, h):
        for j in range(1, w):
            slice_img = log_image_np[:, i - 1:i + 2, j - 1:j + 2]
            result = np.amax(slice_img)
            if result >= 0.0705:
                z, x, y = np.unravel_index(slice_img.argmax(), slice_img.shape)
                co_ordinates.append((i + x - 1, j + y - 1, k ** z * sig))

    co_ordinates = np.array(tuple(set(co_ordinates)))

    def blob_overlap(blob1, blob2):
        n_dim = len(blob1) - 1
        root_ndim = n_dim ** 0.5

        radius1 = blob1[-1] * root_ndim
        radius2 = blob2[-1] * root_ndim

        dist = np.sum((blob1[:-1] - blob2[:-1]) ** 2) ** 0.5

        if dist > radius1 + radius2:
            return 0
        elif dist <= abs(radius1 - radius2):
            return 1
        else:
            ratio_1 = (dist ** 2 + radius1 ** 2 - radius2 ** 2) / (2 * dist * radius1)
            ratio_1 = np.clip(ratio_1, -1, 1)
            acos_1 = math.acos(ratio_1)

            ratio_2 = (dist ** 2 + radius2 ** 2 - radius1 ** 2) / (2 * dist * radius2)
            ratio_2 = np.clip(ratio_2, -1, 1)
            acos_2 = math.acos(ratio_2)

            a = -dist + radius2 + radius1
            b = dist - radius2 + radius1
            c = dist + radius2 - radius1
            dist = dist + radius2 + radius1

            area = (radius1 ** 2 * acos_1 + radius2 ** 2 * acos_2 - 0.5 * math.sqrt(abs(a * b * c * dist)))
            return area / (math.pi * (min(radius1, radius2) ** 2))

    overlap = 0.5
    # Removing blobs that overlap with each other
    sig = co_ordinates[:, -1].max()
    distance = 2 * sig * math.sqrt(co_ordinates.shape[1] - 1)
    tree = scipy.spatial.cKDTree(co_ordinates[:, :-1])
    pairs = np.array(tuple(tree.query_pairs(distance)))
    if len(pairs) == 0:
        return co_ordinates
    else:
        for (i, j) in pairs:
            blob_1, blob_2 = co_ordinates[i], co_ordinates[j]
            if blob_overlap(blob_1, blob_2) > overlap:
                if blob_1[-1] > blob_2[-1]:
                    blob_2[-1] = 0
                else:
                    blob_1[-1] = 0

    co_ordinates = np.array([b for b in co_ordinates if b[-1] > 0])

    return co_ordinates


def unequal_diemension_matching(corners1: numpy.ndarray, corners2: numpy.ndarray, slide_modifier: int = 0.1) -> float:
    img1_area = corners1.shape[0] * corners1.shape[1]
    img2_area = corners2.shape[0] * corners2.shape[1]

    if img1_area == img2_area:
        return 1 - scipy.spatial.distance.cosine(corners1.flatten(), corners2.flatten())

    if img1_area < img2_area:
        smaller_img = corners1
        bigger_img = corners2
    else:
        smaller_img = corners2
        bigger_img = corners1

    if smaller_img.shape[0] <= bigger_img.shape[0] and smaller_img.shape[1] <= bigger_img.shape[1]:
        pass
    elif smaller_img.shape[1] <= bigger_img.shape[0] and smaller_img.shape[0] <= bigger_img.shape[1]:
        smaller_img = smaller_img.transpose()
    else:
        raise ValueError("Unequal dimension matching is not possible")

    max_similarity = float("-inf")
    for i in range(smaller_img.shape[0], bigger_img.shape[0] + 1, math.ceil(slide_modifier * smaller_img.shape[0])):
        big_img_portion = []
        for j in range(smaller_img.shape[1], bigger_img.shape[1] + 1, math.ceil(slide_modifier * smaller_img.shape[1])):
            for x in range(i - smaller_img.shape[0], i):
                big_img_portion.append(bigger_img[x][j - smaller_img.shape[1]:j])

        big_img_part = np.array(big_img_portion)
        if (similarity := 1 - scipy.spatial.distance.cosine(smaller_img.flatten(),
                                                            big_img_part.flatten())) > max_similarity:
            max_similarity = similarity

    return max_similarity
