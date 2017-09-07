import argparse
import glob
from datetime import datetime 
import csv
import os
import shutil


FIELD_DELIMITER = ',' # delimiter used in output CSV


# set up argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True, \
    help="Path to the CSV file.")
#ap.add_argument("-o", "--output", required=False, \
#    help="Path to the directory where folder images are copied.")
args = vars(ap.parse_args())

#dest_file_path = os.path.join(renamed_dir_path, new_full_filename )
#TODO implement user provided file destination
local_path = os.path.dirname(os.path.realpath(__file__))
dest_directory = os.path.join(local_path, 'folder_images') 
if not os.path.exists(dest_directory):
    os.makedirs(dest_directory)

analysis_start_time = datetime.now()

with open(args["source"]) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['image_classifications']=='folder':
            source_path = row['image_path']
            print (source_path)
            basename = os.path.basename(source_path)
            print (basename)
            dest_file_path = (os.path.join(dest_directory, basename))
            shutil.copy2(source_path, dest_file_path)

analysis_end_time = datetime.now()
print('Started:', analysis_start_time)
print('Completed:', analysis_end_time)
print('Duration:', analysis_end_time - analysis_start_time)
