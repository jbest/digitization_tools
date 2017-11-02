import argparse
import glob
import re
import os
import shutil

HERBARIUM_PREFIX = 'BRIT'
FOLDER_INCREMENT = 1000

# set up argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True, \
    help="Path to the directory that contains the images to be sorted.")
ap.add_argument("-p", "--pattern", required=True, \
    help="Pattern of filenames to be sorted.")
args = vars(ap.parse_args())

def sort_file(source=None, destination=None):
    if os.path.exists(destination):
        print('Filename exists, can not move:', destination)
        return False
    else:
        shutil.move(source, destination)
        return True

#iterate JPG files in directory passed from args
source_directory_path = os.path.realpath(args["directory"])
pattern = args["pattern"]
files_analyzed = 0
print('Scanning directory:', source_directory_path, 'for files matching', pattern )
#TODO change image search to use INPUT_FILE_TYPES
for source_path in glob.glob(os.path.join(source_directory_path, pattern)): #this file search seems to be case sensitive
    files_analyzed += 1
    basename = os.path.basename(source_path)
    if basename.startswith(HERBARIUM_PREFIX):
        file_name, file_extension = os.path.splitext(basename)
        accession_id = file_name[len(HERBARIUM_PREFIX):]
        try:
            accession_number = int(accession_id)
            destination_folder_name = 'BRIT' + str(int(accession_number//FOLDER_INCREMENT*FOLDER_INCREMENT))
            destination_directory_path = os.path.join(source_directory_path, destination_folder_name)
            # Check if destination directory exists
            if os.path.isdir(destination_directory_path):
                destination_file_path = os.path.join(destination_directory_path, basename)
                sort_file(source=source_path, destination=destination_file_path)
            else:
                print('Creating folder: ' + destination_directory_path)
                os.mkdir(destination_directory_path)
                destination_file_path = os.path.join(destination_directory_path, basename)
                sort_file(source=source_path, destination=destination_file_path)

        except ValueError:
            print('Can not parse', file_name)
    else:
        print('Ignoring', basename)
print('Sort complete.')
print('Encountered files:', files_analyzed)