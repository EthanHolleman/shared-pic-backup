# checks size of all files in a directory. If total size is greater than
# specified max size removes oldest (by last modification date) files until
# directory is less than max size. Does not explore target directory recursively.

import argparse
from pathlib import Path
import os


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='Path to directory to check file sizes')
    parser.add_argument('max_size', default=100, type=float,
                        help='Max allowed size of all files in directory \
                                    in gigabytes.'
                        )
    return parser.parse_args()


def bytes_to_gigabytes(num_bytes):
    return num_bytes * 10e-9


def make_filesize_dict(target_dir):
    '''Make a dictionary mapping a filepath to its size in gigabytes.

    Args:
        target_dir (str): Path to non-recursively seaarch for files.

    Returns:
        dict: Dictionary with filepaths found in target_dir as keys and their
        sizes in gb as values.
    '''
    return {
        filepath: bytes_to_gigabytes(filepath.stat().st_size)
        for filepath in Path(target_dir).iterdir() if filepath.is_file()
    }


def dir_is_above_max_size(dir_path, max_size):
    filesize_dict = make_filesize_dict(dir_path)
    if sum(filesize_dict.values()) > max_size:
        return True
    else:
        return False


def prune_files(dir_path, max_size):
    '''If the top level of dir_path directory is larger (in gb) than the value 
    set by max_size delete files in order of oldest to newest until it 
    dir_path is less than max_size.

    Args:
        dir_path (str): Path to directory to check size / remove files from.
        max_size (float): Max size of files in top level of directory.
    '''
    if dir_is_above_max_size(dir_path, max_size):
        filesize_dict = make_filesize_dict(dir_path)
        print(filesize_dict)
        files_by_ctime = sorted(filesize_dict.keys(),
                                key=lambda f: f.stat().st_ctime)
        os.remove(files_by_ctime[0])
        prune_files(dir_path, max_size)


def main():

    args = get_args()
    prune_files(args.dir, args.max_size)

if __name__ == '__main__':
    main()
