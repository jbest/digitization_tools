# Modified to accept extended characters in derivative JPG file names like _tn etc
# Modified to log actions

import argparse
#import glob
#import os
import shutil
from pathlib import Path
import re
import csv
import datetime

DEFAULT_HERBARIUM_PREFIX = 'BRIT'
DEFAULT_FOLDER_INCREMENT = 1000
DEFAULT_NUMBER_PAD = 7
files_analyzed = 0
files_sorted = 0
verbose = False

# set up argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True, \
    help="Path to the directory that contains the images to be sorted.")
ap.add_argument("-a", "--action_log", required=True, \
    help="Path of file where action log is stored.")
ap.add_argument("-o", "--output_directory", required=True, default=None,\
    help="Path to an existing directory where sorted files and directories will be written.")
ap.add_argument("-p", "--pattern", required=True, \
    help="Pattern of filenames to be sorted - eg '*.jpg'")
ap.add_argument("-r", "--recursive", action="store_true", \
    help="Recurse sub-directories")
ap.add_argument("-c", "--catalog_prefix", default=DEFAULT_HERBARIUM_PREFIX, \
    help="Prefix string for catalog numbers. Default is BRIT.")
ap.add_argument("-i", "--increment", default=DEFAULT_FOLDER_INCREMENT, \
    help="Increment for folder numbers.")
ap.add_argument("-l", "--length", default=DEFAULT_NUMBER_PAD, \
    help="Length for folder numbers, pre-padded with 0.")
ap.add_argument("-v", "--verbose", action="store_true", \
    help="Detailed output.")
ap.add_argument("-n", "--dry_run", action="store_true", \
    help="Detailed output.")
args = vars(ap.parse_args())

HERBARIUM_PREFIX = args["catalog_prefix"]
FOLDER_INCREMENT = int(args["increment"])
PAD = int(args["length"])
recurse_subdirectories = args["recursive"]
dry_run = args["dry_run"]


def sort_file(source=None, destination=None):
    global files_sorted
    if destination.exists():
        logwriter.writerow([datetime.datetime.now(), source, destination, 'ERROR: file exists'])
        if dry_run:
            print('DRY-RUN: Filename exists, cannot move:', destination)
        if verbose:
            print('Filename exists, cannot move:', destination)
        return False
    else:
        if dry_run:
            print('DRY-RUN: Moved:', destination)
            logwriter.writerow([datetime.datetime.now(), source, destination, 'DRY-RUN: moved'])
        else:
            # temporary disable move
            shutil.move(source, destination)
            logwriter.writerow([datetime.datetime.now(), source, destination, 'moved'])
            if verbose:
                print('Moved:', destination)
        files_sorted += 1
        return True

#iterate files matching pattern in directory passed from args
#source_directory_path = os.path.realpath(args["directory"])
source_directory_path = Path(args["directory"])
pattern = args["pattern"]
output_directory = args["output_directory"]
output_directory_path = Path(output_directory)
if output_directory_path:
    # test to ensure output_directory exists
    #if os.path.isdir(output_directory):
    if output_directory_path.is_dir():
        print('output_directory_path:', output_directory_path)
    else:
        print(f'ERROR: directory {output_directory_path} does not exist.')
        print('Terminating script.')
        quit()
if args['verbose']:
    verbose = True
    print("Verbose report...")

if dry_run:
    print('DRY-RUN: starting dry run:')
print('Scanning directory:', source_directory_path, 'for files matching', pattern)

if recurse_subdirectories:
    path_matches = source_directory_path.rglob(pattern)
else:
    path_matches = source_directory_path.glob(pattern)

#for matching_path in source_directory_path.rglob('*.jpg'):
# pattern for derivative files
pattern_string = HERBARIUM_PREFIX + '(\d*)'
accession_id_pattern = re.compile(pattern_string)
# Create log file
# TODO Make sure log file can be written and is unique
log_file_path = args["action_log"]
with open(log_file_path, 'w', newline='') as csvfile:
    logwriter = csv.writer(csvfile)
    # write header
    logwriter.writerow(['timestamp', 'source', 'destination', 'action'])
    #logwriter.writerow(['test_time', 'test_source', 'test_destination', 'test_action'])
    for matching_path in path_matches:
        files_analyzed += 1
        #basename = os.path.basename(source_path)
        basename = matching_path.name
        if basename.startswith(HERBARIUM_PREFIX):
            file_name = matching_path.stem
            file_extension = matching_path.suffix
            #print('file_name:', file_name)
            #print('file_extension:', file_extension)
            #accession_id = file_name[len(HERBARIUM_PREFIX):]
            accession_match = accession_id_pattern.match(file_name)
            try:
                #accession_number = int(accession_id)
                accession_number = int(accession_match.group(1))
                folder_number = int(accession_number//FOLDER_INCREMENT*FOLDER_INCREMENT)
                padded_folder_number = str(folder_number).zfill(PAD)
                # zfill may be deprecated in future? Look into string formatting with fill
                # https://stackoverflow.com/a/339013
                #destination_folder_name = HERBARIUM_PREFIX + str(int(accession_number//FOLDER_INCREMENT*FOLDER_INCREMENT))
                destination_folder_name = HERBARIUM_PREFIX + padded_folder_number
                if output_directory:
                    output_directory_path = Path(output_directory)
                    destination_directory_path = output_directory_path.joinpath(destination_folder_name)
                else:
                    # no output_directory specified, using source directory
                    destination_directory_path = source_directory_path.joinpath(destination_folder_name)
                destination_file_path = destination_directory_path.joinpath(basename)
                # Check if destination directory exists
                if destination_directory_path.is_dir():
                    sort_file(source=matching_path, destination=destination_file_path)
                else:
                    if verbose:
                        print('Creating folder: ' + destination_directory_path)
                    if dry_run:
                        # log, don't create
                        logwriter.writerow([datetime.datetime.now(), '', destination_directory_path, 'DRY-RUN: created directory'])
                    else:
                        destination_directory_path.mkdir()
                        logwriter.writerow([datetime.datetime.now(), '', destination_directory_path, 'created directory'])
                    sort_file(source=matching_path, destination=destination_file_path)

            except ValueError:
                print('Cannot parse', file_name)
        else:
            if verbose:
                print(f'Ignoring {basename} - does not start with {HERBARIUM_PREFIX}.')

print('Sort complete.')
print('Encountered files:', files_analyzed)
print('Sorted files:', files_sorted)
if dry_run:
    print('DRY-RUN: ending dry run.')
