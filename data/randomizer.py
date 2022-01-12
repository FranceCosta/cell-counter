#!/usr/bin/python3

import argparse
from typing import NamedTuple
import os
import shutil
import random

class Args(NamedTuple):
    '''Command-line arguments'''
    input_dir:str
    test_dir:str
    train_dir:str
    perc:float
    seed:int
    
def get_args() -> Args:
    '''Get command-line arguments'''
    parser = argparse.ArgumentParser(
        description='Split images into train and test datasets',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    required = parser.add_argument_group('required arguments')
    required.add_argument('-input_dir',
                        metavar='--Input-directory', 
                        help='Directory where images to be splitted are. It must contain only images',
                        type=dir_path,
                        required=True,
                        )
    required.add_argument('-test_dir',
                        metavar='--Test-directory', 
                        help='Output test directory',
                        type=dir_path,
                        required=True,
                        )
    required.add_argument('-train_dir',
                        metavar='--Train-directory', 
                        help='Output train directory',
                        type=dir_path,
                        required=True,
                        )
    parser.add_argument('-perc',
                        metavar='--Percentage', 
                        help='Percentage of images to be allocated in test directory',
                        default=0.2,
                        type=float,
                        )
    parser.add_argument('-seed',
                        metavar='--Seed', 
                        help='Seed to ensure splitting reproducibility',
                        default=1,
                        type=int,
                        )
    args = parser.parse_args()
    return Args(args.input_dir, args.test_dir, args.train_dir, args.perc, args.seed)
def dir_path(path):
    '''Path validator'''
    if os.path.isdir(path):
        print(f'Directory {path} already exists and contains {len(os.listdir(path))} elements')
    else:
        os.mkdir(path)
    return path
        #aise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")
def main() -> None:
    args = get_args()
    # get random filenames to be placed in test directory
    Test_number=int(float(len(os.listdir(args.input_dir)))*float(args.perc))
    Test_filenames = os.listdir(args.input_dir)
    random.seed(args.seed)
    random.shuffle(Test_filenames)
    Test_filenames = Test_filenames[:Test_number]
    #Test_filenames = random.sample(os.listdir(args.input_dir), Test_number)
    # the remaining files are directed to training dir
    Train_filenames = [filename for filename in os.listdir(args.input_dir) if filename not in Test_filenames]
    # allocate the files
    for list_, outdir_ in zip([Test_filenames, Train_filenames], [args.test_dir, args.train_dir]):
        for fname in list_:
            srcpath = os.path.join(args.input_dir, fname)
            desPath = os.path.join(outdir_, fname)
            shutil.copyfile(srcpath, desPath)
    print(f'{len(Test_filenames)} images copied in {args.test_dir} directory')
    print(f'{len(Train_filenames)} images copied in {args.train_dir} directory')
if __name__ == "__main__":
    main()
