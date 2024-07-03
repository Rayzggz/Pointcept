#This is a simple script that reads a NPY file and prints its content.

import numpy as np

def read_npy_file(file_path):
    return np.load(file_path)

def ask_and_read_npy_file():
    file_path = input("Enter the path of the NPY file: ")
    print(read_npy_file(file_path))

ask_and_read_npy_file()

