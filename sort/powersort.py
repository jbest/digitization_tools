import configparser
from pathlib import Path
import argparse
import re
#import glob
#import os
import shutil

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
ap.add_argument("-n", "--dry_run", action="store_true", \
    help="Simulate the sort process without moving files or creating directories.")
args = vars(ap.parse_args())

config = configparser.ConfigParser()
config_file = args["config"]
config.read(config_file)
# see for lists: https://stackoverflow.com/a/8048529/560798
#print(config.sections())
#print(config['Files']['web_image_destination_path'])

dry_run = args["dry_run"]
verbose = args["verbose"]
PAD = DEFAULT_NUMBER_PAD

def move_file(source=None, destination_directory=None, filename=None):
    destination = destination_directory.joinpath(filename)
    if destination.exists():
        if dry_run:
            print('DRY-RUN: Filename exists, cannot move:', destination)
        if verbose:
            print('Filename exists, cannot move:', destination)
        #TODO change to exception
        move_success = False
        status = 'Filename exists'
        return move_success, status
    else:
        if dry_run:
            print('DRY-RUN: Moved:', destination)
            status = 'DRY-RUN - simulated move'
        else:
            # Create directory path if it doesn't exist
            destination_directory.mkdir(parents=True, exist_ok=True)
            #TODO Log creation of directory? If so, will need to force exception and only log when no exception
            # Temporarily disabled move
            shutil.move(source, destination)
            status = 'File moved'
            if verbose:
                print('Moved:', destination)
        # files_sorted += 1
        move_success = True       
        return move_success, status

def sort_files(path_matches=None, output_path=None):
    for matching_path in path_matches:
        #print(matching_path)
        basename = matching_path.name
        file_name = matching_path.stem
        file_extension = matching_path.suffix
        accession_match = accession_id_pattern.match(file_name)
        if accession_match:
            # Extract accession number
            accession_number = int(accession_match.group(1))
            folder_number = int(accession_number//folder_increment*folder_increment)
            padded_folder_number = str(folder_number).zfill(PAD)
            # zfill may be deprecated in future? Look into string formatting with fill
            # https://stackoverflow.com/a/339013
            destination_folder_name = collection_prefix + padded_folder_number
            # destination path
            destination_path = output_path.joinpath(destination_folder_name)
            move_success, move_status = move_file(source=matching_path, destination_directory=destination_path, filename=basename)
        else:
            print(f'Unable to match: {basename}')

# Get collection parameters and defaults
collection_prefix = config['Collection']['collection_prefix']
folder_increment = config['Files']['folder_increment']
print(f'folder_increment: {folder_increment}')
# TODO Get number pad

try:
    folder_increment = int(folder_increment)
except:
    print(f'folder_increment: {folder_increment} can not be converted to integer.')
    quit()


# Institution code?

# Set up paths and patterns
source_directory_path = Path(config['Files']['staging_path'])
archive_ext = config['Files']['archive_extension']
archive_ext_pattern = '*.' + archive_ext
# Testing multiple patterns
archive_patterns = config.items("Archive_patterns")
for key, pattern in archive_patterns:
    print(f'key: {key}, pattern: {pattern}')
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

# TODO Check ability to write to web directory
# TODO Check ability to write to archive directory

# Start scanning source directory
recurse_subdirectories = True

# TODO make regex pattern for extracting accession_id, make configurable in config file
#accession_id_pattern = re.compile('BRIT(\d*)')
pattern_string = collection_prefix + '(\d*)'
accession_id_pattern = re.compile(pattern_string)

# Scan for archival files
print('Scanning directory:', source_directory_path, 'for archival files matching', archive_ext_pattern)
if recurse_subdirectories:
    # Using rglob
    archive_path_matches = source_directory_path.rglob(archive_ext_pattern)
else:
    # Using glob
    archive_path_matches = source_directory_path.glob(archive_ext_pattern)

# sort archive files
sort_files(path_matches=archive_path_matches, output_path=archive_output_path)

# Scan for web files
print('Scanning directory:', source_directory_path, 'for web files matching', web_ext_pattern)
if recurse_subdirectories:
    web_path_matches = source_directory_path.rglob(web_ext_pattern)
else:
    web_path_matches = source_directory_path.glob(web_ext_pattern)

# sort web files
sort_files(path_matches=web_path_matches, output_path=web_output_path)



