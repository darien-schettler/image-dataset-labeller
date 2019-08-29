import cv2
import os
import shutil
import pandas as pd

INPUT_DIR = r"C:\Users\Darie\Desktop\D_IMAGES"
OUTPUT_DIR = "./output"
LABELS = ['GOOD_D', 'BAD_D']
DISPLAY_SIZE = 700
USER = "DARIEN"


def rescale_img(bigger_img, width=1200):
    w_to_h_ratio = bigger_img.shape[0]/bigger_img.shape[1]
    height = round(width/w_to_h_ratio)
    dim = (width, height)

    # resize image
    return cv2.resize(bigger_img, dim, interpolation=cv2.INTER_AREA)


def make_labels(img_paths, label_list):

    num_of_labels = len(label_list)
    label_arrays = [[] for _ in range(num_of_labels)]
    for path in img_paths:
        waiting = True
        while waiting:

            cv2.imshow("Please select label", rescale_img(cv2.imread(path), DISPLAY_SIZE))

            wait_key = cv2.waitKey(0)
            if 1 <= int(chr(wait_key)) <= len(label_list):
                label_arrays[int(chr(wait_key))-1].append(path)
                waiting = False
            elif wait_key == 27:  # Esc key to stop
                return label_arrays
            else:
                continue

    cv2.destroyAllWindows()
    return label_arrays


def create_dirs(output_dir_list):
    for dir in output_dir_list:
        path=os.path.join(os.getcwd(), str(dir))
        try:
            os.mkdir(path)
        except OSError as e:
            if "file already exists" in str(e):
                print("Directory for label '{}' already exists !!".format(dir))
            else:
                print("Creation of the directory {}s failed\n\tTraceback:\n\t{}\n\n".format(path, e))
        else:
            print("Successfully created the directory for label '{}'\n\tLocated at path {}\n".format(dir, path))
    return


def move_files(output_dir_list, label_arrays):
    create_dirs(output_dir_list)

    for i, label_array in enumerate(label_arrays):
        for path in label_array:
            shutil.move(path, os.path.join(os.getcwd(), str(output_dir_list[i])))



PATHS = [os.path.join(INPUT_DIR, f_name) for f_name in os.listdir(INPUT_DIR)]
array_list = make_labels(img_paths=PATHS, label_list=LABELS)

move_files(LABELS, array_list)

print("\n\nFINAL COUNTS\n")
for i, label in enumerate(LABELS):
    print(label, " : ", len(array_list[i]))


