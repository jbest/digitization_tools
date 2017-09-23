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

with open(args["source"]) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if 'folder' in row['image_classifications']:
            #print(row['image_classifications'])
            darwin_core = DWC_TEMPLATE.copy()
            model_match_string = row['closest_model']
            if model_match_string:
                # assuming image is folder
                model_match = ast.literal_eval(model_match_string)
                [(model_name, model_similarity)] = model_match.items()
                print (model_name)
                if model_name == 'BRIT-VDB-AL':
                    #print('"dwc:stateProvince":"Alabama"')
                    darwin_core['dwc:stateProvince'] = 'Alabama'
                elif model_name == 'BRIT-VDB-TN':
                    #print('"dwc:stateProvince":"Tennessee"')
                    darwin_core['dwc:stateProvince'] = 'Tennessee'
                elif model_name == 'BRIT-VDB-NA':
                    #print('"dwc:stateProvince":""')
                    pass
                else:
                    #print('"dwc:stateProvince":""')
                    pass
            #print (darwin_core)
            print (json.dumps(darwin_core, indent=4))

analysis_end_time = datetime.now()
print('Started:', analysis_start_time)
print('Completed:', analysis_end_time)
print('Duration:', analysis_end_time - analysis_start_time)
