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
ap.add_argument("-p", "--path", nargs='?', const=None, required=False, \
    help="Path used to replace the original batch path (when files are moved between analysis and processing).")
ap.add_argument("-r", "--rename", action='store_true', \
    help="Switch to rename image files in place.")
ap.add_argument("-m", "--metadata", action='store_true', \
    help="Switch to generate metadata files.")
ap.add_argument("-v", "--verbose", action='store_true', \
    help="Switch to generate verbose messages.")
ap.add_argument("-f", "--folder", required=False, \
    choices=['f', 'l'], \
    help="Folder sequence. 'f' - folder first, 'l' - folder last")
#TODO add option to generate skeletal metadata in JSON and/or CSV
#ap.add_argument("-o", "--output", required=False, \
#    help="Path to the directory where folder images are copied.")
args = vars(ap.parse_args())

DWC_TEMPLATE = {'dwc:country':'United States of America','dwc:stateProvince':'',\
    'dwc:family':'', 'dwc:genus':'', 'dwc:specificEpithet':''}
FOLDER_IMAGE_EVENTS=[]
FOLDER_IMAGE_METADATA=[]

"""
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
"""

def compile_folder_metadata(model_name=None, image_event_id=None, original_filename=None, new_filename=None):
    metadata = DWC_TEMPLATE.copy()
    metadata['image_event_id'] = image_event_id
    metadata['original_filename'] = original_filename
    metadata['new_filename'] = new_filename
    # Determine region based on best histogram match, standardize model names
    #TODO add terms for institution code and collection code
    if model_name == 'BRIT-VDB-AL':
        #print('"dwc:stateProvince":"Alabama"')
        metadata['dwc:stateProvince'] = 'Alabama'
    elif model_name == 'BRIT-VDB-TN':
        #print('"dwc:stateProvince":"Tennessee"')
        metadata['dwc:stateProvince'] = 'Tennessee'
    elif model_name == 'BRIT-VDB-NA' or model_name == 'BRIT_VDB-NA': # Temp fix for incorrectly named model
        model_name = 'BRIT-VDB-NA'
        # don't populate DwC stateProvince because North America is not an appropriate value for this term
    else:
        model_name = 'folder'

    metadata['model_name'] = model_name
    #print(metadata)
    return metadata

def save_folder_metadata():
    pass

#folder_list = [] # for folder objects
local_path = os.path.dirname(os.path.realpath(__file__))
analysis_start_time = datetime.now()

if not args["rename"]:
    print('NOTICE: file rename disabled, use -r to enable file renaming.')
if not args["metadata"]:
    print('NOTICE: metadata creation disabled, use -m to enable metadata creation.')

with open(args["source"]) as csvfile:
    reader = csv.DictReader(csvfile)
    #initial_folder = folder()
    #current_folder = initial_folder
    #print(initial_folder)
    #folder_list.append(initial_folder)
    for row in reader:
        if args["path"]:
            current_working_path = os.path.abspath(args["path"])
            if not os.path.exists(current_working_path):
                print('ERROR - path does not exist:', current_working_path)
                exit()
            #print(current_working_path)
        else:
            current_working_path = row['batch_path']
            if not os.path.exists(current_working_path):
                print('ERROR - path does not exist:', current_working_path)
                exit()
        image_classifications = row['image_classifications']
        original_basename = row['basename']
        original_filename, original_file_extension = os.path.splitext(original_basename)
        # Get all barcodes
        barcodes_string = row['barcodes']
        if barcodes_string:
            barcodes = ast.literal_eval(barcodes_string)
        else:
            barcodes = None

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
<<<<<<< HEAD
            #TODO generate metadata for specimen
            # rename specimen image files
            if args["rename"]:
=======
            if os.path.exists(current_path):
                #print('Exists:', current_path)
                #print('Change:', new_path)
                if os.path.exists(new_path):
                    print('ALERT - file exists, can not overwrite:')
                    print(new_path)
                else:
                    try:
                        os.rename(current_path, new_path)
                    except OSError:
                        # Possible problem with character in new filename
                        print('ALERT - OSError. new_path:', new_path, 'current_path:', current_path )
                    except:
                        print("Unexpected error:", sys.exc_info()[0])
                        raise


        else:
            #Assuming image is a folder 
            new_filename = None
            if model_name:
                if 'ambiguous' in row['image_classifications']:
                    model_name = 'folder'
                new_filename = model_name + '_' + row['image_event_id']
                new_basename = new_filename+original_file_extension
                current_path = os.path.join(current_working_path, original_basename)
                new_path = os.path.join(current_working_path, new_basename)
                #print(new_basename)
>>>>>>> e3c7b0e59998987dcd0fa49b166f7cc8d18e5598
                if os.path.exists(current_path):
                    if os.path.exists(new_path):
                        print('ALERT - file exists, can not overwrite:')
                        print(new_path)
                    else:
                        os.rename(current_path, new_path)

        else:
            #Assuming image is a folder because no barcode
            image_event_id = row['image_event_id']

            if image_event_id in FOLDER_IMAGE_EVENTS:
                #FIXME This is causing JPG files to not be renamed
                print('Record already processed.')
            else:
                FOLDER_IMAGE_EVENTS.append(image_event_id)
                model_match_string = row['closest_model']
                if model_match_string:
                    model_match = ast.literal_eval(model_match_string)
                    [(model_name, model_similarity)] = model_match.items()
                    #current_folder.model_name = model_name
                #new_filename = None
                if model_name:
                    if 'ambiguous' in row['image_classifications']:
                        model_name = 'folder'
                    new_filename = model_name + '_' + image_event_id
                    new_basename = new_filename+original_file_extension
                    current_path = os.path.join(current_working_path, original_basename)
                    new_path = os.path.join(current_working_path, new_basename)
                    folder_metadata = compile_folder_metadata(model_name=model_name, image_event_id=image_event_id, original_filename=original_filename, new_filename=new_filename)
                    FOLDER_IMAGE_METADATA.append(folder_metadata)
                    #TODO write folder JSON file, or create record in memory to write later
                    # rename folder image files
                    if args["rename"]:
                        if os.path.exists(current_path):
                            #print('Exists:', current_path)
                            #print('Change:', new_path)
                            if os.path.exists(new_path):
                                #TODO Log alerts
                                print('ALERT - file exists, can not overwrite:')
                                print(new_path)
                            else:
                                os.rename(current_path, new_path)
                                #current_folder.filename = new_filename
                        else:
                            print('ALERT - original file not found')
                else:
                    print('ALERT - no model name, can not generate folder metadata')


if args["metadata"]:
    # Write folder metadata for batch
    with open('folder_metadata.csv', 'w') as f:
        fieldnames = ['dwc:country', 'dwc:stateProvince', 'dwc:family', 'dwc:genus', 'dwc:specificEpithet', 'image_event_id', 'original_filename', 'new_filename', 'model_name' ] 
        w = csv.DictWriter(f, fieldnames)
        w.writeheader()
        w.writerows(FOLDER_IMAGE_METADATA)

analysis_end_time = datetime.now()
"""
for folder in folder_list:
    print(folder)
"""
print('Started:', analysis_start_time)
print('Completed:', analysis_end_time)
print('Duration:', analysis_end_time - analysis_start_time)