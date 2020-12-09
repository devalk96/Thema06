import sys
import os

DIRECTORIES = {"FASTQC": "fastqc",
               "FSQReports": "fastqc/reports"}


def create_dirs(subdirs, file_root):
    """Create dirs from nested directory"""
    for key, val in subdirs.items():
        dir_name = os.path.join(file_root, key)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        if type(val) == dict:
            create_dirs(val, os.path.join(file_root, key))
    return file_root


if __name__ == '__main__':
    sys.exit(create_dirs())
