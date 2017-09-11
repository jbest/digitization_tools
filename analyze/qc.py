"""
find records with 'ambiguous' image classifications
find records with multiple barcodes
find records with high (bad match) closest models
for each:
display image, prompt to fix


"""

import argparse
import glob
from datetime import datetime 
import csv
import ast

MODEL_MATCH_MAX = 1.0

# set up argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True, \
    help="Path to the CSV file.")
ap.add_argument("-f", "--folder", required=False, \
    choices=['f', 'l'], \
    help="Folder sequence. 'f' - folder first, 'l' - folder last")
#ap.add_argument("-o", "--output", required=False, \
#    help="Path to the directory where folder images are copied.")
args = vars(ap.parse_args())

#local_path = os.path.dirname(os.path.realpath(__file__))
analysis_start_time = datetime.now()

with open(args["source"]) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        model_match_string = None
        model_name = None
        model_similarity = None
        model_match_string = row['closest_model']
        if model_match_string:
            model_match = ast.literal_eval(model_match_string)
            [(model_name, model_similarity)] = model_match.items()
            if model_similarity > MODEL_MATCH_MAX:
                print('Poor model match:', model_similarity)
        if 'ambiguous' in row['image_classifications']:
            print ('AMBIG', row['image_path'])

analysis_end_time = datetime.now()

print('Started:', analysis_start_time)
print('Completed:', analysis_end_time)
print('Duration:', analysis_end_time - analysis_start_time)