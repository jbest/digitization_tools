"""
Powersort organizes files based on file type and sorting rules which are
designated in an external configuration file. File types are Archival image files
such as DNG, CR2, etc and Web files are JPEGs. The script searches for files based
on file extensions and source paths which are in the config file. Files matching the
expected naming pattern are sorted into a destination directory and sub-directories
which are created by the script. Files not matching the pattern are not moved.
Files that match the filename and path of existing files will not be moved.
Results are saved to a log file.
Author: Jason Best jbest@brit.org
"""

import configparser
from pathlib import Path
import argparse
import re
import shutil
import os
import pwd
import csv
import datetime
import itertools

# TODO Make dry run more useful - make it test destination perms and perms for each file to be moved

# set up argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", required=True, \
    help="Path to the configuration file to be used for processing images.")
ap.add_argument("-s", "--source", required=False, \
    help="Source directory - overrides source in config file")
ap.add_argument("-j", "--web_destination", required=False, \
    help="Destination web directory - overrides web destination in config file")
ap.add_argument("-r", "--archive_destination", required=False, \
    help="Destination archive/raw directory - overrides archive destination in config file")
ap.add_argument("-v", "--verbose", action="store_true", \
    help="Detailed output.")
ap.add_argument("-n", "--dry_run", action="store_true", \
    help="Simulate the sort process without moving files or creating directories.")
filetype_group = ap.add_mutually_exclusive_group()
filetype_group.add_argument("-w", "--web_only",help='Sort web files only', action='store_true')
filetype_group.add_argument("-a", "--archive_only", help='Sort archive files only', action='store_true')
args = vars(ap.parse_args())

print(args)

config = configparser.ConfigParser()
config_file = args["config"]
config_input = config.read(config_file)

if len(config_input)==0:
    raise ValueError('Failed to open config file: ' + config_file)

dry_run = args["dry_run"]
verbose = args["verbose"]
archive_only = args["archive_only"]
web_only = args["web_only"]

def move_file(source=None, destination_directory=None, filename=None, filetype=None):
    """
    Move files from the source to the destination directory.
    """
    destination = destination_directory.joinpath(filename)
    if destination.exists():
        if dry_run:
            now = datetime.datetime.now()
            writer.writerow({'timestamp': now, 'username': username, 'action': 'DRY_RUN-move', 'result': 'fail', \
                'filetype': filetype, 'source': source, 'destination': destination})
        if verbose:
            print('Filename exists, cannot move:', destination)
        #TODO change to exception
        move_success = False
        status = 'Filename exists'
        now = datetime.datetime.now()
        writer.writerow({'timestamp': now, 'username': username, 'action': 'move', 'result': 'fail', \
            'filetype': filetype, 'source': source, 'destination': destination})
        return {'move_success': move_success, 'status': status}
    else:
        if dry_run:
            print('DRY-RUN: Moved:', destination)
            status = 'DRY-RUN - simulated move'
            move_success = True
            now = datetime.datetime.now()
            writer.writerow({'timestamp': now, 'username': username, 'action': 'DRY_RUN-move', 'result': 'success', \
                'filetype': filetype, 'source': source, 'destination': destination})
        else:
            # Create directory path if it doesn't exist
            destination_directory.mkdir(parents=True, exist_ok=True)
            #TODO Log creation of directory? If so, will need to force exception and only log when no exception
            try:
                shutil.move(source, destination)
                status = 'success'
                details = None
                move_success = True
            except PermissionError:
                status = 'fail'
                details = 'PermissionError'
                move_success = False
            now = datetime.datetime.now()
            writer.writerow({'timestamp': now, 'username': username, \
                'action': 'move', 'result': status, 'details': details, \
                'filetype': filetype, 'source': source, 'destination': destination})
            if verbose:
                print('Move:', destination, status)
               
        return {'move_success': move_success, 'status': status}

def sort_files(path_matches=None, output_path=None, filetype=None):
    """
    Determine the appropriate destination for each file in path_matches.
    Call move_file to move into determined destination.
    """
    sorted_file_count = 0
    path_matched_file_count = 0
    unmatched_file_count = 0
    unmoved_file_count = 0
    for matching_path in path_matches:
        path_matched_file_count += 1
        basename = matching_path.name
        file_name = matching_path.stem
        file_extension = matching_path.suffix
        accession_match = accession_id_pattern.match(file_name)
        if accession_match:
            # Extract accession number
            accession_number = int(accession_match.group(1))
            # Determine what folder number the files should be moved to
            folder_number = int(accession_number//folder_increment*folder_increment)
            padded_folder_number = str(folder_number).zfill(number_pad)
            # zfill may be deprecated in future? Look into string formatting with fill
            # https://stackoverflow.com/a/339013
            # Prepend the collection prefix to the folder number
            destination_folder_name = collection_prefix + padded_folder_number
            # Determin destination path for file
            destination_path = output_path.joinpath(destination_folder_name)
            move_result = move_file(source=matching_path, \
                destination_directory=destination_path, filename=basename, filetype=filetype)
            if move_result['move_success']:
                sorted_file_count +=1
            else:
                unmoved_file_count +=1
        else:
            unmatched_file_count +=1
            print(f'Unable to match: {basename}')
            now = datetime.datetime.now()
            if dry_run:
                action = 'DRY_RUN-match'
            else:
                action = 'match'
            writer.writerow({'timestamp': now, 'username': username, 'action': action, 'result': 'fail', \
                'filetype': filetype, 'source': matching_path, 'destination': None})
    return {'sorted_file_count': sorted_file_count, \
    'path_matched_file_count': path_matched_file_count, \
    'unmatched_file_count': unmatched_file_count, \
    'unmoved_file_count': unmoved_file_count}

def scan_files(extensions=None):
    """
    Scan the source directory for files matching the provided extensions.
    """
    match_list = []
    for key, extension in extensions:
        ext_pattern = '*.' + extension
        # Scan for files
        print('Scanning directory:', source_directory_path, 'for files matching', ext_pattern)
        if recurse_subdirectories:
            # Using rglob
            path_matches = source_directory_path.rglob(ext_pattern)
        else:
            # Using glob
            path_matches = source_directory_path.glob(ext_pattern)
        match_list.append(path_matches)

    all_matches = itertools.chain(*match_list)
    return all_matches

# Get collection parameters and defaults
try:
    collection_prefix = config['Collection']['collection_prefix']
    folder_increment = config['Files']['folder_increment']
    number_pad = config['Files']['number_pad']
    # Set up paths and patterns
    source_directory_path = Path(config['Paths']['staging_path'])
    log_path = Path(config['Paths']['sort_log_destination_path']) 
    # Read multiple archive extensions
    archive_extensions = config.items("Archive_extensions")
    archive_output_path = Path(config['Paths']['archive_image_destination_path'])
    # Read multiple web extensions
    web_extensions = config.items("Web_extensions")
    web_output_path = Path(config['Paths']['web_image_destination_path'])
except KeyError as e:
    print('Missing key in configuration file:', e)
    quit()

# Use any configuration file overrides
# Use source path from command line
if args['source']:
    source_directory_path = Path(args['source'])
# Use web path from command line
if args['web_destination']:
    web_output_path = Path(args['web_destination'])
# Use archive path from command line
if args['archive_destination']:
    archive_output_path = Path(args['archive_destination'])

# Convert configuration strings to ints
try:
    folder_increment = int(folder_increment)
except ValueError:
    print(f'folder_increment: {folder_increment} can not be converted to integer.')
    quit()

try:
    number_pad = int(number_pad)
except:
    print(f'number_pad: {number_pad} can not be converted to integer.')
    quit()

# Check existence of source path
if source_directory_path:
    # test to ensure output_directory exists
    if source_directory_path.is_dir():
        print('source_directory_path:', source_directory_path)
    else:
        print(f'ERROR: directory {source_directory_path} does not exist.')
        print('Terminating script.')
        quit()
else:
    print(f'ERROR: no source directory provided.')
    quit() 

# Check ability to write to web directory
if not os.access(web_output_path, os.W_OK | os.X_OK):
    print(f'Unable to write to web directory: {web_output_path}')
    quit()

# Check ability to write to archive directory
if not os.access(archive_output_path, os.W_OK | os.X_OK):
    print(f'Unable to write to archive directory: {archive_output_path}')
    quit()

# Start scanning source directory
recurse_subdirectories = True

# TODO make regex pattern for extracting accession_id, make configurable in config file
#accession_id_pattern = re.compile('BRIT(\d*)')
pattern_string = collection_prefix + '(\d*)'
accession_id_pattern = re.compile(pattern_string)

# create CSV file for output
# Create log directory path if it does not exist
log_path.mkdir(exist_ok=True)
now = datetime.datetime.now()
log_filename = collection_prefix + '_' + str(now.strftime('%Y-%m-%dT%H%M%S'))
if dry_run:
    log_filename = log_filename + '_DRY-RUN'
log_filename = log_filename + '.csv'
log_file_path = log_path.joinpath(log_filename)
# get current username
try:
    username = pwd.getpwuid(os.getuid()).pw_name
except:
    print('ERROR - Unable to retrive username.')
    username = None

with open(log_file_path, 'w', newline='') as csvfile:
    fieldnames = ['timestamp', 'username', 'action', 'result', 'details', 'filetype', 'source', 'destination']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    web_file_count = 0
    web_sorted_file_count = 0
    web_unsorted_file_count = 0
    web_unmatched_file_count = 0
    archive_file_count = 0
    archive_sorted_file_count = 0
    archive_unsorted_file_count = 0
    archive_unmatched_file_count = 0

    # Scan archive files, only archive if specified
    if (not web_only and not archive_only) or archive_only:
        archive_path_matches = scan_files(extensions=archive_extensions)
        sort_result = sort_files(path_matches=archive_path_matches, output_path=archive_output_path, filetype='archive')
        archive_file_count = sort_result['path_matched_file_count']
        archive_unmatched_file_count = sort_result['unmatched_file_count']
        archive_sorted_file_count = sort_result['sorted_file_count']
        archive_unsorted_file_count = sort_result['unmoved_file_count']

    # Scan web files, only web if specified
    if (not web_only and not archive_only) or web_only:
        web_path_matches = scan_files(extensions=web_extensions)
        sort_result = sort_files(path_matches=web_path_matches, output_path=web_output_path, filetype='web')
        web_file_count = sort_result['path_matched_file_count']
        web_unmatched_file_count = sort_result['unmatched_file_count']
        web_sorted_file_count = sort_result['sorted_file_count']
        web_unsorted_file_count = sort_result['unmoved_file_count']

# Summary report
print('SORT COMPLETE')
print('Log file written to:', log_file_path)
print('ARCHIVE FILES:')
print('Found:', archive_file_count)
print('Sorted:', archive_sorted_file_count)
print('Unsorted:', archive_unsorted_file_count)
print('Unmatched pattern:', archive_unmatched_file_count)
print('WEB FILES:')
print('Found:', web_file_count)
print('Sorted:', web_sorted_file_count)
print('Unsorted:', web_unsorted_file_count)
print('Unmatched pattern:', web_unmatched_file_count)
