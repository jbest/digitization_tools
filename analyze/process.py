#process.py

"""
compare differences in sort order:
-filename
-creation date
find duplicate barcodes
determine most likely image classification and use for filename

change filename, all names unique, no overwritten files
record changes
leave any problem files unchanged
flag folder images and record which folders contain which specimens
generate skeletal data files
"""

import argparse
import glob
from datetime import datetime 
import csv
import os
import shutil
import ast


FIELD_DELIMITER = ',' # delimiter used in output CSV


# set up argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True, \
    help="Path to the CSV file.")
#ap.add_argument("-o", "--output", required=False, \
#    help="Path to the directory where folder images are copied.")
args = vars(ap.parse_args())

local_path = os.path.dirname(os.path.realpath(__file__))

"""
dest_directory = os.path.join(local_path, 'folder_images') 
if not os.path.exists(dest_directory):
    os.makedirs(dest_directory)
"""
analysis_start_time = datetime.now()

with open(args["source"]) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        #TODO allow working path to be changed by user in case file folders are moved between analysis and processing
        current_working_path = row['batch_path']
        original_basename = row['basename']
        original_file_name, original_file_extension = os.path.splitext(original_basename)
        # Get all barcodes
        barcodes = ast.literal_eval(row['barcodes'])
        model_match_string = None
        model_name = None
        model_match_string = row['closest_model']
        if model_match_string:
            model_match = ast.literal_eval(model_match_string)
            [(model_name, model_similarity)] = model_match.items()
            #print(model_name)
        if barcodes:
            # Assumming all images with barcodes are specimens
            if len(barcodes) == 1:
                new_filename = barcodes[0]['data']
            else:
                new_filename = ''
                for barcode in barcodes:
                    #TODO don't add underscore for last barcode string
                    new_filename = new_filename + barcode['data'] + '_'
            new_basename = new_filename+original_file_extension
            #print (new_basename)
            current_path = os.path.join(current_working_path, original_basename)
            new_path = os.path.join(current_working_path, new_basename)
            if os.path.exists(current_path):
                #print('Exists:', current_path)
                #print('Change:', new_path)
                if os.path.exists(new_path):
                    print('ALERT - file exists, can not overwrite:')
                    print(new_path)
                else:
                    os.rename(current_path, new_path)
        else:
            #print('No barcode')
            new_filename = None
            if model_name:
                new_filename = model_name + '_' + row['file_uuid']
                new_basename = new_filename+original_file_extension
                current_path = os.path.join(current_working_path, original_basename)
                new_path = os.path.join(current_working_path, new_basename)
                #print(new_basename)
                if os.path.exists(current_path):
                    #print('Exists:', current_path)
                    #print('Change:', new_path)
                    if os.path.exists(new_path):
                        #TODO Log alerts
                        print('ALERT - file exists, can not overwrite:')
                        print(new_path)
                    else:
                        os.rename(current_path, new_path)
                else:
                    print('ALERT - original file not found')
        """
        if row['image_classifications']=='folder':
            source_path = row['image_path']
            print (source_path)
            basename = os.path.basename(source_path)
            print (basename)
            dest_file_path = (os.path.join(dest_directory, basename))
            shutil.copy2(source_path, dest_file_path)
        """

analysis_end_time = datetime.now()
print('Started:', analysis_start_time)
print('Completed:', analysis_end_time)
print('Duration:', analysis_end_time - analysis_start_time)

