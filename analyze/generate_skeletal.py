import argparse
import glob
from datetime import datetime 
import csv
import os
import shutil
import ast
import json


FIELD_DELIMITER = ',' # delimiter used in output CSV
#FOLDER_REGIONS = {'BRIT-VDB-AL':'Alabama', 'BRIT-VDB-TN':'Tennessee', 'BRIT-VDB-NA':'North America'}
DWC_TEMPLATE = {'dwc:country':'United States of America','dwc:stateProvince':'',\
    'dwc:family':'', 'dwc:genus':'', 'dwc:specificEpithet':''}
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
dest_directory = os.path.join(local_path, 'folder_metadata') 
if not os.path.exists(dest_directory):
    os.makedirs(dest_directory)

analysis_start_time = datetime.now()

FOLDER_IMAGE_EVENTS=[]
FOLDER_IMAGE_METADATA=[]
batch_uuid = None
with open(args["source"]) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        batch_uuid = row['batch_id'] #This value will get reset for each row, assuming all rows are identical
        if 'folder' in row['image_classifications']:
            image_event_id = row['image_event_id']
            if image_event_id in FOLDER_IMAGE_EVENTS:
                #print('Folder image already processed:', image_event_id)
                pass
            else:
                FOLDER_IMAGE_EVENTS.append(image_event_id)
                darwin_core = DWC_TEMPLATE.copy()
                #darwin_core['image_name'] = row['basename']
                darwin_core['image_name'] = row['file_name']
                model_match_string = row['closest_model']
                model_name = None
                if model_match_string:
                    # assuming image is folder
                    image_event_id = row['image_event_id']
                    model_match = ast.literal_eval(model_match_string)
                    [(model_name, model_similarity)] = model_match.items()
                    if 'ambiguous' in row['image_classifications']:
                        model_name = 'folder'
                    print (model_name)
                    if model_name == 'BRIT-VDB-AL':
                        #print('"dwc:stateProvince":"Alabama"')
                        darwin_core['dwc:stateProvince'] = 'Alabama'
                    elif model_name == 'BRIT-VDB-TN':
                        #print('"dwc:stateProvince":"Tennessee"')
                        darwin_core['dwc:stateProvince'] = 'Tennessee'
                    elif model_name == 'BRIT-VDB-NA':
                        pass
                    else:
                        pass
                #print (darwin_core)
                print (row['image_event_id'])
                #print (json.dumps(darwin_core, indent=4))
                darwin_core['image_event_id'] = row['image_event_id']
                FOLDER_IMAGE_METADATA.append(darwin_core)

                new_filename = None
                if model_name:
                    if 'ambiguous' in row['image_classifications']:
                        model_name = 'folder'
                    new_filename = model_name + '_' + image_event_id + '.JSON'
                    with open(os.path.join(dest_directory, new_filename), 'w') as f:
                        json.dump(darwin_core, f, ensure_ascii=False, indent=4)
                else:
                    #TODO handle this better
                    print('No model name, no JSON file generated')
                #json_file = model_name + '_' + row['file_uuid']

# Write folder metadata for batch
with open('folder_metadata.csv', 'w') as f:
    fieldnames = [ 'image_name', 'dwc:country', 'dwc:stateProvince', 'dwc:family', 'dwc:genus', 'dwc:specificEpithet', 'image_event_id'] 
    w = csv.DictWriter(f, fieldnames)
    w.writeheader()
    w.writerows(FOLDER_IMAGE_METADATA)
"""
for record in FOLDER_IMAGE_METADATA:
    print(record)
"""

analysis_end_time = datetime.now()
print('Started:', analysis_start_time)
print('Completed:', analysis_end_time)
print('Duration:', analysis_end_time - analysis_start_time)
