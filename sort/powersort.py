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
ap.add_argument("-n", "--dry-run", action="store_true", \
    help="Simulate the sort process without moving files.")
args = vars(ap.parse_args())

#HERBARIUM_PREFIX = args["catalog_prefix"]
#FOLDER_INCREMENT = int(args["increment"])
#PAD = int(args["length"])


config = configparser.ConfigParser()
config.read('TEST.ini')
# see for lists: https://stackoverflow.com/a/8048529/560798
#print(config.sections())
#print(config['Files']['web_image_destination_path'])

# Set up paths and patterns
source_directory_path = Path(config['Files']['staging_path'])
archive_ext = config['Files']['archive_extension']
archive_ext_pattern = '*.' + archive_ext
archive_output_path = Path(config['Files']['archive_image_destination_path'])
web_ext = config['Files']['web_extension']
web_ext_pattern = '*.' + web_ext
web_output_path = Path(config['Files']['web_image_destination_path'])

# Check existence of source path
if source_directory_path:
    # test to ensure output_directory exists
    if source_directory_path.is_dir():
        print('source_directory_path:', source_directory_path)
    else:
        print(f'ERROR: directory {source_directory_path} does not exist.')
        print('Terminating script.')
        quit()


# Start scanning source directory
#testing
recurse_subdirectories = True

# Scan for archival files
print('Scanning directory:', source_directory_path, 'for archival files matching', archive_ext_pattern)
if recurse_subdirectories:
    archival_path_matches = source_directory_path.rglob(archive_ext_pattern)
else:
    archival_path_matches = source_directory_path.glob(archive_ext_pattern)

for matching_path in archival_path_matches:
    print(matching_path)

# Scan for web files
print('Scanning directory:', source_directory_path, 'for web files matching', web_ext_pattern)
if recurse_subdirectories:
    web_path_matches = source_directory_path.rglob(web_ext_pattern)
else:
    web_path_matches = source_directory_path.glob(web_ext_pattern)


