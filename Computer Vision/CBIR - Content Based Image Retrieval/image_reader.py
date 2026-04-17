import os
from string import Template
from typing import Iterator, Union

import cv2
import numpy

path = Template("/Users/utkarsh/Desktop/Utkarsh/College/Year 3/Semester 2/Computer Vision/Assignments/Assignment " \
                f"1/datasets_4186/$folder/$name")

files_to_ignore = {".DS_Store"}


def get_query_image(name: str, load_flag: int = cv2.IMREAD_COLOR) -> numpy.ndarray:
    query_image_path = path.substitute(folder="query_4186", name=name)

    if not os.path.exists(query_image_path):
        raise FileNotFoundError(f"No {query_image_path.split('/')[-1]} found in gallery")

    query_img = cv2.imread(query_image_path, load_flag)

    if query_img is None:
        return None

    object_location_file = open(path.substitute(folder="query_txt_4186", name=name.split('.')[0] + '.txt'), 'r')

    query_image_box_deets = tuple(map(int, object_location_file.readline().strip().split()))

    query_img = query_img[query_image_box_deets[1]:query_image_box_deets[1] + query_image_box_deets[3],
                query_image_box_deets[0]:query_image_box_deets[0] + query_image_box_deets[2]]

    return query_img


def get_query_image_uncropped(name: str, load_flag: int = cv2.IMREAD_COLOR) -> numpy.ndarray:
    query_image_path = path.substitute(folder="query_4186", name=name)

    if not os.path.exists(query_image_path):
        raise FileNotFoundError(f"No {query_image_path.split('/')[-1]} found in gallery")

    query_img = cv2.imread(query_image_path, load_flag)

    if query_img is None:
        return None

    return query_img


def get_gallery_image(name: str, load_flag: int = cv2.IMREAD_COLOR) -> numpy.ndarray:
    gallery_image_path = path.substitute(folder="gallery_4186", name=name)

    if not os.path.exists(gallery_image_path):
        raise FileNotFoundError(f"No {gallery_image_path.split('/')[-1]} found in gallery")

    gallery_img = cv2.imread(gallery_image_path, load_flag)

    return gallery_img


def gallery_images(load_flag: int = cv2.IMREAD_COLOR) -> Iterator[tuple[Union[str, numpy.ndarray]]]:
    directory = '/'.join(path.safe_substitute(folder="gallery_4186").split('/')[:-1])

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename not in files_to_ignore:
                yield filename, get_gallery_image(filename, load_flag=load_flag)


def gallery_images_names() -> Iterator[str]:
    directory = '/'.join(path.safe_substitute(folder="gallery_4186").split('/')[:-1])

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename not in files_to_ignore:
                yield filename


def query_images(load_flag: int = cv2.IMREAD_COLOR) -> Iterator[tuple[Union[str, numpy.ndarray]]]:
    directory = '/'.join(path.safe_substitute(folder="query_4186").split('/')[:-1])

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename not in files_to_ignore:
                yield filename, get_query_image(filename, load_flag=load_flag)


def query_images_names() -> Iterator[str]:
    directory = '/'.join(path.safe_substitute(folder="query_4186").split('/')[:-1])

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename not in files_to_ignore:
                yield filename
