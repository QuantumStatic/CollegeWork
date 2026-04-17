import cv2
import numpy
import os

from image_reader import gallery_images, query_images, get_query_image_uncropped
from CONSTANTS import FEATURES, orb, sift
import concurrent.futures

from feature_extraction import harris_corner_detector

done = 0


def compute_and_save(img_path, img_name, img):
    kp_gallery, des_gallery = sift.detectAndCompute(img, None)
    numpy.save(f"{img_path}{img_name}", des_gallery)


def extract_and_store_gallery_features():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for img_name, img in gallery_images():
            executor.submit(compute_and_save, f"gallery_store/sift_store/{FEATURES}_store/des_gallery", img_name, img)


def extract_and_store_uncropped_query_img(query_img_name: str):
    compute_and_save(f"query_store/{FEATURES}_store/des_query", query_img_name,
                     get_query_image_uncropped(query_img_name))


def extract_and_store_query_features():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        [executor.submit(compute_and_save, f"query_store/sift_store/{FEATURES}_store/des_query", img_name, img) for
         img_name, img
         in
         query_images()]


def save_corner(img_path, img_name, img):
    if not os.path.exists(f"{img_path}{img_name}.npy"):
        corners = harris_corner_detector(img)
        numpy.save(f"{img_path}{img_name}", corners)


def save_corners_gallery():
    for idx, (img_name, img) in enumerate(gallery_images(load_flag=cv2.IMREAD_GRAYSCALE)):
        save_corner(f"gallery_store/corner_store/corners", img_name, img)
        print(idx, img_name)


def save_corners_query():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        [executor.submit(save_corner, f"query_store/corner_store/corners", img_name, img) for img_name, img in
         query_images(load_flag=cv2.IMREAD_GRAYSCALE)]

