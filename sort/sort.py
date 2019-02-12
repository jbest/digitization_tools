import argparse
import glob
import os
import shutil

DEFAULT_HERBARIUM_PREFIX = 'BRIT'
DEFAULT_FOLDER_INCREMENT = 1000
DEFAULT_NUMBER_PAD = 7
files_analyzed = 0
files_sorted = 0

# set up argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True, \
    help="Path to the directory that contains the images to be sorted.")
ap.add_argument("-p", "--pattern", required=True, \
    help="Pattern of filenames to be sorted - eg '*.jpg'")
ap.add_argument("-c", "--catalog_prefix", default=DEFAULT_HERBARIUM_PREFIX, \
    help="Prefix string for catalog numbers. Default is BRIT.")
ap.add_argument("-i", "--increment", default=DEFAULT_FOLDER_INCREMENT, \
    help="Increment for folder numbers.")
ap.add_argument("-l", "--length", default=DEFAULT_NUMBER_PAD, \
    help="Length for folder numbers, pre-padded with 0.")
args = vars(ap.parse_args())

HERBARIUM_PREFIX = args["catalog_prefix"]
FOLDER_INCREMENT = int(args["increment"])
PAD = int(args["length"])

def sort_file(source=None, destination=None):
    global files_sorted
    if os.path.exists(destination):
        print('Filename exists, can not move:', destination)
        return False
    else:
        shutil.move(source, destination)
        files_sorted += 1
        return True

#iterate files matching pattern in directory passed from args
source_directory_path = os.path.realpath(args["directory"])
pattern = args["pattern"]

print('Scanning directory:', source_directory_path, 'for files matching', pattern)

for source_path in glob.glob(os.path.join(source_directory_path, pattern)):
    files_analyzed += 1
    basename = os.path.basename(source_path)
    if basename.startswith(HERBARIUM_PREFIX):
        file_name, file_extension = os.path.splitext(basename)
        accession_id = file_name[len(HERBARIUM_PREFIX):]
        try:
            accession_number = int(accession_id)
            folder_number = int(accession_number//FOLDER_INCREMENT*FOLDER_INCREMENT)
            padded_folder_number = str(folder_number).zfill(PAD)
            #destination_folder_name = HERBARIUM_PREFIX + str(int(accession_number//FOLDER_INCREMENT*FOLDER_INCREMENT))
            destination_folder_name = HERBARIUM_PREFIX + padded_folder_number
            destination_directory_path = os.path.join(source_directory_path, destination_folder_name)
            destination_file_path = os.path.join(destination_directory_path, basename)
            # Check if destination directory exists
            if os.path.isdir(destination_directory_path):
                sort_file(source=source_path, destination=destination_file_path)
            else:
                print('Creating folder: ' + destination_directory_path)
                os.mkdir(destination_directory_path)
                sort_file(source=source_path, destination=destination_file_path)

        except ValueError:
            print('Can not parse', file_name)
    else:
        print('Ignoring', basename)
print('Sort complete.')
print('Encountered files:', files_analyzed)
print('Sorted files:', files_sorted)