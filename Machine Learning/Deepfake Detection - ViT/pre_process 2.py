import shutil
import os
import random

DATA_FOLDER_PATH: str = "/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Machine Learning/Group Project/data"

all_files = []
def get_all_files():
    """Run this function if you change the size of the images. It will reduce the size of the images from 299x299 to 224x224"""

    for folder in (('original', 'manipulated')):

        *_, files = next(os.walk(f"{DATA_FOLDER_PATH}/{folder}"))
        all_files.extend([*files])


def shift_images():
    total_files_len = len(all_files)
    train_files = set(random.sample(all_files, int(total_files_len*0.8)))
    total_files_set = set(all_files)

    total_test = total_files_set - train_files
    test_set = set(random.sample(list(total_test), int(len(total_test)*0.6)))
    validation_set = total_test - test_set
    
    try:
        os.mkdir(f"{DATA_FOLDER_PATH}/GAN_train")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"{DATA_FOLDER_PATH}/GAN_test")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"{DATA_FOLDER_PATH}/GAN_validation")
    except FileExistsError:
        pass
    

    for file in train_files:
        try:
            shutil.copy(f"{DATA_FOLDER_PATH}/original/{file}", f"{DATA_FOLDER_PATH}/GAN_train/{file}")
        except FileNotFoundError:
            shutil.copy(f"{DATA_FOLDER_PATH}/manipulated/{file}", f"{DATA_FOLDER_PATH}/GAN_train/{file}")

    for file in test_set:
        try:
            shutil.copy(f"{DATA_FOLDER_PATH}/original/{file}", f"{DATA_FOLDER_PATH}/GAN_test/{file}")
        except FileNotFoundError:
            shutil.copy(f"{DATA_FOLDER_PATH}/manipulated/{file}", f"{DATA_FOLDER_PATH}/GAN_test/{file}")
    
    for file in validation_set:
        try:
            shutil.copy(f"{DATA_FOLDER_PATH}/original/{file}", f"{DATA_FOLDER_PATH}/GAN_validation/{file}")
        except FileNotFoundError:
            shutil.copy(f"{DATA_FOLDER_PATH}/manipulated/{file}", f"{DATA_FOLDER_PATH}/GAN_validation/{file}")



if __name__ == "__main__":
    get_all_files()
    shift_images()







