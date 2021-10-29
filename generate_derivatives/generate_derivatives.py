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
# regex
catalog_number_regex = "(?P<catNum>(?P<instID>BRIT)(-(?P<collID>XX)-)*(?P<numerical>\\d+))"
web_jpg_regex = "(_(?P<suffix>a-z|0-9))*(\\.)(?i)(?P<ext>jpg|jpeg)"
web_jpg_med_regex ="(_(?P<suffix>a-z|0-9))*(_)(?P<size>med)(\\.)(?i)(?P<ext>jpg|jpeg)"
web_jpg_thumb_regex = "(_(?P<suffix>a-z|0-9))*(_)(?P<size>thumb)(\\.)(?i)(?P<ext>jpg|jpeg)"

web_jpg_pattern = re.compile(catalog_number_regex + web_jpg_regex)
web_jpg_med_pattern = re.compile(catalog_number_regex + web_jpg_med_regex)
web_jpg_thumb_pattern = re.compile(catalog_number_regex + web_jpg_thumb_regex)

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
   file_stem = source_file.stem
   thumb_filename = file_stem + THUMB_EXT + source_file.suffix
   med_filename = file_stem + MED_EXT + source_file.suffix
   image_directory = source_file.parent
   print(image_directory)


   try:
        image = Image.open(source_file)
        image.thumbnail((900,900))
        image.save(image_directory.joinpath(med_filename))
   except IOError:
        pass
   try:
        image = Image.open(source_file)
        image.thumbnail((390,390))
        image.save(image_directory.joinpath(thumb_filename))
   except IOError:
        pass
def scan_files(path=None):
    """
    Scan the directory for files matching JPEG files.
    Determine file type based on ending qualifier (thumb, med, etc)
    """
    matches = []
    image_sets = []
    pattern = '([^\\s]+(\\.(?i)(jpe?g))$)'
    scan_path = Path(path)
    #print('pattern:', pattern)
    file_pattern = re.compile(pattern)
    for root, dirs, files in os.walk(path):
        for file in files:
            #print(os.path.join(root, file))
            m = file_pattern.match(file)
            if m:
                file_dict = m.groupdict()
                #file_path = os.path.join(root, file)
                file_path = scan_path.joinpath(file)
                file_stem = file_path.stem
                file_name = file
                file_dict['file_name'] = file_name
                file_dict['file_stem'] = file_stem
                file_dict['file_path'] = str(file_path)
                # Evaluate file stem
                if file_stem.endswith(THUMB_EXT):
                    file_type = 'thumb'
                elif file_stem.endswith(MED_EXT):
                    file_type = 'medium'
                else:
                    file_type = 'full'
                    print('generate derivatives')
                    generate_derivatives(source_file=file_path)
                file_dict['file_type'] = file_type
                matches.append(file_dict)
    return matches

if __name__ == '__main__':
    # set up argparse
    args = arg_setup()
        #print(args)
    dry_run = args['dry_run']
    verbose = args['verbose']
    force_overwrite = args['force']
    input_path = args['input_path']
    print(input_path)
    files = scan_files(path=input_path)
    #print(files)








