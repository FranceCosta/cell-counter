#!/usr/bin/python3

import os
import argparse
import pandas as pd
from typing import NamedTuple
from fastai.vision.all import *
from tabulate import tabulate

class Args(NamedTuple):
    '''Command-line arguments'''
    analysis_path:str
    model_path:str
    output_filename:str
    resize:int
    
def get_args() -> Args:
    '''Get command-line arguments'''
    parser = argparse.ArgumentParser(
        description='Run model predictions',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    required = parser.add_argument_group('required arguments')
    required.add_argument('-analysis_path',
                        metavar='--Analysis-path', 
                        help='Directory where images to be evaluated are',
                        type=dir_path,
                        required=True,
                        )
    required.add_argument('-model_path',
                        metavar='--Model-path', 
                        help='Path to trained model. Do not use .pth extension',
                        type=str,
                        required=True,
                        )
    required.add_argument('-output_filename',
                        metavar='--Output-filename', 
                        help='Output .xlsx filename. Avoid .xlsx extension',
                        type=str,
                        required=True,
                        )
    parser.add_argument('-resize',
                        metavar='--Resize', 
                        help='Resize images to indicated size. Use the same resizing factor adopted during training',
                        default=128,
                        type=int,
                        )
    args = parser.parse_args()
    return Args(args.analysis_path, args.model_path, args.output_filename, args.resize)
    
    
def dir_path(path):
    '''Path validator'''
    if os.path.isdir(path) == False:
        raise argparse.ArgumentTypeError(f'{path} is not a valid path')
    return path

def main() -> None:
    args = get_args()
    # function to get label from images
    get_y = lambda x: float(str(x).split('.')[-2])
    # resizes the biggest dimension of an image to max_sz maintaining the aspect ratio
    item_tfms = [RatioResize(args.resize)]
    # transforms applied to the batches once they are formed (need to be identical to training transformations)
    batch_tfms=[*aug_transforms(mult=0, flip_vert=True, 
                max_rotate=45, min_zoom=0, max_zoom=0, max_warp=0, p_affine=0), 
                Normalize.from_stats(*imagenet_stats)]
    # create model datablocks and dataloader
    blocks = (ImageBlock, RegressionBlock)
    block = DataBlock(blocks=blocks,
                      get_items=get_image_files,
                      get_y=get_y,
                      item_tfms=item_tfms,
                      batch_tfms=batch_tfms)
    dls = block.dataloaders(args.analysis_path, bs=32, num_workers=0)
    # create xResNet50
    learn = Learner(dls, xresnet50(pretrained=True, n_out=1), metrics=mae)
    # load pre-trained model weights
    learn.load(f'{os.path.join(os.getcwd(), args.model_path)}')
    # run predictions
    imgs = get_image_files(args.analysis_path)
    listout=[[str(img), int(learn.predict(img)[0][0])] for img in imgs]
    df=pd.DataFrame(listout, columns=['name', 'predicted'] )
    print(f'{tabulate(df, tablefmt="psql")}')
    # export predictions
    df.to_excel(f'{args.output_filename}.xlsx')
    print(f'Results succesfully saved as {args.output_filename}.xlsx')

if __name__ == "__main__":
    main()