#process.py

import argparse
from datetime import datetime
import csv
import os
import ast

FIELD_DELIMITER = ',' # delimiter used in output CSV
# set up argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True, \
    help="Path to the CSV file.")
ap.add_argument("-p", "--path", nargs='?', const=None, required=True, \
    help="Path used to replace the original batch path (when files are moved between analysis and processing).")
ap.add_argument("-f", "--folder", required=False, \
    choices=['f', 'l'], \
    help="Folder sequence. 'f' - folder first, 'l' - folder last")
#ap.add_argument("-o", "--output", required=False, \
#    help="Path to the directory where folder images are copied.")
args = vars(ap.parse_args())

class folder():
    def __init__(self, uuid=None, filename=None, model_name=None):
        self.uuid = uuid
        self.filename = filename
        self.model_name = model_name
        self.specimens = []
    def __str__(self):
        return 'Folder contains: ' + str(self.specimens)
    def add_specimen(self, image_name=None, uuid=None, barcodes=None):
        self.specimens.append({'image_name':image_name, 'uuid':uuid})

folder_list = []
local_path = os.path.dirname(os.path.realpath(__file__))
analysis_start_time = datetime.now()

with open(args["source"]) as csvfile:
    reader = csv.DictReader(csvfile)
    initial_folder = folder()
    current_folder = initial_folder
    print(initial_folder)
    folder_list.append(initial_folder)
    for row in reader:
        #TODO allow working path to be changed by user in case file folders are moved between analysis and processing
        if args["path"]:
            print(args["path"])
        else:
            print('No path')
        current_working_path = row['batch_path']
        image_classifications = row['image_classifications']
        original_basename = row['basename']
        original_filename, original_file_extension = os.path.splitext(original_basename)
        # Get all barcodes
        barcodes = ast.literal_eval(row['barcodes'])
        model_match_string = None
        model_name = None
        model_match_string = row['closest_model']
        if model_match_string:
            # assuming image is folder
            model_match = ast.literal_eval(model_match_string)
            [(model_name, model_similarity)] = model_match.items()
            current_folder.model_name = model_name
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
            #Assuming image is a folder 
            new_filename = None
            if model_name:
                if 'ambiguous' in row['image_classifications']:
                    model_name = 'folder'
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
                        current_folder.filename = new_filename
                        #TODO write folder JSON file, or create record in memory to write later
                else:
                    print('ALERT - original file not found')

analysis_end_time = datetime.now()
for folder in folder_list:
    print(folder)
print('Started:', analysis_start_time)
print('Completed:', analysis_end_time)
print('Duration:', analysis_end_time - analysis_start_time)