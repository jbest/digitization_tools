import configparser
from pathlib import Path
import argparse
#import glob
#import os
#import shutil

#DEFAULT_HERBARIUM_PREFIX = 'BRIT'
DEFAULT_FOLDER_INCREMENT = 1000
DEFAULT_NUMBER_PAD = 7
files_analyzed = 0
files_sorted = 0
verbose = False

# set up argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", required=True, \
    help="Path to the configuration file to be used for processing images.")
ap.add_argument("-v", "--verbose", action="store_true", \
    help="Detailed output.")
args = vars(ap.parse_args())

#HERBARIUM_PREFIX = args["catalog_prefix"]
#FOLDER_INCREMENT = int(args["increment"])
#PAD = int(args["length"])


config = configparser.ConfigParser()
config.read('TEST.ini')
# see for lists: https://stackoverflow.com/a/8048529/560798
#print(config.sections())
#print(config['Files']['web_image_destination_path'])


source_directory_path = Path(config['Files']['staging_path'])
archive_ext_pattern = config['Files']['archive_extension']
web_ext_pattern = config['Files']['web_extension']
archive_output_path = Path(config['Files']['archive_image_destination_path'])
#web_output_path = Path(config['Files']['web_image_destination_path'])
if archive_output_path:
    # test to ensure output_directory exists
    if archive_output_path.is_dir():
        print('archive_output_path:', archive_output_path)
    else:
        print(f'ERROR: directory {archive_output_path} does not exist.')
        print('Terminating script.')
        quit()
print('Scanning directory:', archive_output_path, 'for files matching', archive_ext_pattern)

#testing
recurse_subdirectories = True
if recurse_subdirectories:
    path_matches = archive_output_path.rglob(archive_ext_pattern)
else:
    path_matches = archive_output_path.glob(archive_ext_pattern)

for matching_path in path_matches:
    print(matching_path)

