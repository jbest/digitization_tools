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

#iterate JPG files in directory passed from args
directory_path = os.path.realpath(args["directory"])
pattern = args["pattern"]
files_analyzed = 0
print('Scanning directory:', directory_path, 'for files matching', pattern )
#TODO change image search to use INPUT_FILE_TYPES
for image_path in glob.glob(os.path.join(directory_path, pattern)): #this file search seems to be case sensitive
    files_analyzed += 1
    basename = os.path.basename(image_path)
    if basename.startswith(HERBARIUM_PREFIX):
        file_name, file_extension = os.path.splitext(basename)
        accession_id = file_name[len(HERBARIUM_PREFIX):]
        try:
            accession_number = int(accession_id)
            destination_folder = 'BRIT' + str(int(accession_number//FOLDER_INCREMENT*FOLDER_INCREMENT))
            destination_path = os.path.join(directory_path, destination_folder)
            if os.path.isdir(destination_path):
                destination_file = os.path.join(destination_path, basename)
                shutil.move(image_path, destination_file)
            else:
                print('Create folder: ' + destination_path)
                os.mkdir(destination_path)
                destination_file = os.path.join(destination_path, basename)
                shutil.move(image_path, destination_file)

        except ValueError:
            print('Can not parse', file_name)
    else:
        print('Ignoring', basename)
print('Sort complete.')