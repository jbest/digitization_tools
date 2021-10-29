"""
Generate derivative images for Symbiota collections


"""

import argparse
from PIL import Image 
import re
import os
from pathlib import Path


THUMB_EXT = '_thumb'
MED_EXT = '_med'


def arg_setup():
    # set up argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input_path", required=False, \
        help="Input directory path - overrides input_path in config file")
    ap.add_argument("-v", "--verbose", action="store_true", \
        help="Detailed output.")
    ap.add_argument("-n", "--dry_run", action="store_true", \
        help="Simulate the process without moving files or creating directories.")
    ap.add_argument("-f", "--force", action="store_true", \
        help="Force overwrite of existing files.")
    args = vars(ap.parse_args())
    return args

def generate_derivatives(source_file=None):
   print('Generating derivatives: ', str(source_file.name))
   image_directory = source_file.parent
   file_stem = source_file.stem
   thumb_path = image_directory.joinpath(file_stem + THUMB_EXT + source_file.suffix)
   med_path = image_directory.joinpath(file_stem + MED_EXT + source_file.suffix)

   if not med_path.exists():
       try:
            image = Image.open(source_file)
            image.thumbnail((900,900))
            image.save(med_path)
       except IOError:
            pass
   if not thumb_path.exists():
       try:
            image = Image.open(source_file)
            image.thumbnail((390,390))
            image.save(thumb_path)
       except IOError:
            pass

def scan_files(path=None):
    """
    Scan the directory for files matching JPEG files.
    Determine file type based on ending qualifier (thumb, med, etc)
    """
    #matches = []
    #image_sets = []
    pattern = '([^\\s]+(\\.(?i)(jpe?g))$)'
    scan_path = Path(path)
    #print('pattern:', pattern)
    file_pattern = re.compile(pattern)
    for root, dirs, files in os.walk(path):
        for file in files:
            #print(os.path.join(root, file))
            m = file_pattern.match(file)
            if m:
                file_path = scan_path.joinpath(file)
                file_stem = file_path.stem
                # Evaluate file stem
                if file_stem.endswith(THUMB_EXT):
                    file_type = 'thumb'
                elif file_stem.endswith(MED_EXT):
                    file_type = 'medium'
                else:
                    file_type = 'full'
                    #print('generate derivatives')
                    generate_derivatives(source_file=file_path)

if __name__ == '__main__':
    # set up argparse
    args = arg_setup()
    dry_run = args['dry_run']
    verbose = args['verbose']
    force_overwrite = args['force']
    input_path = args['input_path']
    scan_files(path=input_path)





